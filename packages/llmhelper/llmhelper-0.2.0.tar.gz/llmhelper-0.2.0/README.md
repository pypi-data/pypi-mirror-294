# llmhelper

LLM helper library.

## 安装

```shell
pip install llmhelper
```

## 工具集

- exceptions
  - ParseJsonResponseError
  - ChatError
  - GetTextEmbeddingsError
  - GetRerankScoresError
- base
  - get_llmhelper_config
  - set_llmhelper_default_config
  - set_llmhelper_config
  - get_default_llm
  - get_default_chat_model
  - get_default_embeddings_model
  - get_default_rerank_model
  - get_template_engine
  - get_llm_base_url
  - get_llm_api_url
- template
  - get_template_prompt_by_django_template_engine
  - get_template_prompt_by_jinjia2
  - get_template_prompt
- llm
  - get_messages
  - parse_json_response
  - chat
  - jsonchat
  - streaming_chat
- embeddings
  - OpenAIEmbeddings
  - get_text_embeddings
- rerank
  - get_rerank_scores

## 版本记录

### v0.1.0

- 版本首发。

### v0.2.0

- 添加embeddings模型操作支持。
- 添加rerank模型操作支持。
