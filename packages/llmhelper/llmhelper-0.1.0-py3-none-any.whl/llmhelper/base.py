import os
from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple
import re

import yaml
from zenutils import importutils
from openai import OpenAI

__all__ = [
    "set_llmhelper_config",
    "get_default_llm",
    "get_default_llm_model_name",
    "get_messages",
    "parse_json_response",
    "ParseJsonResponseError",
    "get_template_prompt_by_django_template_engine",
    "get_template_prompt_by_jinjia2",
    "get_template_prompt",
    "chat",
    "jsonchat",
    "streaming_chat",
]

LLMHELPER_CONFIG = {
    "template_engine": "llmhelper.base.get_template_prompt_by_django_template_engine",
}


def set_llmhelper_config(api_key=None, base_url=None, model=None, template_engine=None):
    if api_key:
        LLMHELPER_CONFIG["api_key"] = api_key
    if base_url:
        LLMHELPER_CONFIG["base_url"] = base_url
    if model:
        LLMHELPER_CONFIG["model"] = model
    if template_engine:
        LLMHELPER_CONFIG["template_engine"] = template_engine


def get_default_llm():
    """创建系统默认的OpenAI实例。"""
    api_key = LLMHELPER_CONFIG.get("api_key", os.environ.get("OPENAI_API_KEY"))
    base_url = LLMHELPER_CONFIG.get("base_url", os.environ.get("OPENAI_BASE_URL"))
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
    )


def get_default_llm_model_name():
    """获取系统默认的模型名称。"""
    return LLMHELPER_CONFIG.get(
        "model",
        os.environ.get(
            "OPENAI_MODEL",
            "qwen2-instruct",
        ),
    )


def get_messages(
    prompt: Union[str, List[Dict[str, str]]],
    histories: Optional[List[Tuple[str, str]]] = None,
    system_prompt: str = "You are helpful assistance.",
):
    """将文字版的prompt转化为messages数组。

    @parameter histories: 问答记录记录:
    ```
        histories = [
            ("question1", "answer1"),
            ("question2", "answer2"),
        ]
    ```
    """
    histories = histories or []
    history_messages = []
    for history in histories:
        history_messages.append({"role": "user", "content": history[0]})
        history_messages.append({"role": "assistant", "content": history[1]})

    if isinstance(prompt, str):
        result = [
            {"role": "system", "content": system_prompt},
        ]
        result += history_messages
        result += [
            {"role": "user", "content": prompt},
        ]
    else:
        result = prompt[:1] + history_messages + prompt[1:]
    return result


class ParseJsonResponseError(RuntimeError):
    """LLM输出不能解析为json数据。"""
    def __init__(self):
        super().__init__("LLM输出不能解析为json数据。")


def _fix_json_escape(match):
    return "\\" + match.group(0)


def parse_json_response(response_text):
    """把LLM输出解析为json数据。

    如果LLM响应的不是有效的json数据，则抛出`ParseJsonResponseError`异常。
    """
    # 标准json输出，并且没有其它多余输出
    if response_text.startswith("```json"):
        response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
    # s1: 尝试json反序列化
    try:
        return yaml.safe_load(response_text)
    except:
        pass
    # s2: 有多余输出，但有多个```json\nxxx\n```JSON块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # s3: 有多余输出，但有多个```\nxxx\n```代码块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # 复杂场景下，字符串没有转义，尝试修正
    response_text = re.sub('\\\\[^\\\\nrt\\"]', _fix_json_escape, response_text)
    # s4: 尝试json反序列化
    try:
        return yaml.safe_load(response_text)
    except:
        pass
    # s5: 有多余输出，但有多个```json\nxxx\n```JSON块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    # s6: 有多余输出，但有多个```\nxxx\n```代码块，将第一个有效的json块当成返回值
    json_blocks = re.findall("```json(.+?)```", response_text, re.MULTILINE)
    for json_block in json_blocks:
        try:
            return yaml.safe_load(json_block)
        except:
            pass
    raise ParseJsonResponseError()


def get_template_prompt_by_django_template_engine(
    template_name: str,
    prompt: str = None,
    **context,
):
    """使用django模板引擎生成最终提示词。"""
    from django.template.loader import render_to_string

    return render_to_string(
        template_name=template_name,
        context={
            "prompt": prompt,
            **context,
        },
    )


def get_template_prompt_by_jinjia2(
    template_name: str,
    prompt: str = None,
    **context,
):
    """使用jinja2模板引擎生成最终提示词。"""
    from jinja2 import Environment
    from jinja2 import FileSystemLoader

    environment = Environment(loader=FileSystemLoader("templates/"))
    tempalte = environment.get_template(template_name)
    return tempalte.render(prompt=prompt, **context)


def get_template_prompt(
    template_name: str,
    prompt: str = None,
    template_engine=None,
    **context,
):
    """根据提示词模板、用户问题和其它参数，生成最终的提示词。"""
    if template_engine:
        if callable(template_engine):
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(template_engine)
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
    else:
        template_engine = LLMHELPER_CONFIG.get("template_engine", None)
        if not template_engine:
            return get_template_prompt_by_django_template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        elif callable(template_engine):
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )
        else:
            template_engine = importutils.import_from_string(template_engine)
            return template_engine(
                template_name=template_name,
                prompt=prompt,
                **context,
            )


def chat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template_name: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """基于提示词模板的对话。"""
    if template_name:
        prompt = get_template_prompt(
            template_name,
            prompt=prompt,
            template_engine=template_engine,
            **context,
        )
    messages = get_messages(
        prompt=prompt,
        histories=histories,
        system_prompt=system_prompt,
    )
    llm = llm or get_default_llm()
    model = model or get_default_llm_model_name()
    result = llm.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=False,
    )
    return result.choices[0].message.content


def jsonchat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template_name: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """基于提示词模板的对话。"""
    response_text = chat(
        prompt=prompt,
        histories=histories,
        template_name=template_name,
        model=model,
        llm=llm,
        template_engine=template_engine,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        **context,
    )
    return parse_json_response(
        response_text=response_text,
    )


def streaming_chat(
    prompt: str = None,
    histories: Optional[List[Tuple[str, str]]] = None,
    template_name: Optional[str] = None,
    model: Optional[str] = None,
    llm: Optional[OpenAI] = None,
    template_engine=None,
    system_prompt="You are helpful assistance.",
    temperature=0.01,
    max_tokens: int = 6144,
    **context,
):
    """流式AI对话，返回响应文字内容。

    过滤掉空白块。
    """
    if template_name and isinstance(prompt, str):
        prompt = get_template_prompt(
            template_name,
            prompt=prompt,
            template_engine=template_engine,
            **context,
        )
    messages = get_messages(
        prompt=prompt,
        histories=histories,
        system_prompt=system_prompt,
    )
    llm = llm or get_default_llm()
    model = model or get_default_llm_model_name()
    result = llm.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
    )
    for chunk in result:
        empty_flag = False
        try:
            if not chunk.choices[0].delta.content:
                empty_flag = True
        except:
            pass
        if not empty_flag:
            yield chunk.model_dump()
