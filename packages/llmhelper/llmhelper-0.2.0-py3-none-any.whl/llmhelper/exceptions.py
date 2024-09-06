__all__ = [
    "ParseJsonResponseError",
    "ChatError",
    "GetTextEmbeddingsError",
    "GetRerankScoresError",
]


class ParseJsonResponseError(RuntimeError):
    """LLM输出不能解析为json数据。"""

    def __init__(self):
        super().__init__("LLM输出不能解析为json数据。")


class ChatError(RuntimeError):
    """大模型对话失败。"""

    def __init__(self):
        super().__init__("大模型对话失败。")


class GetTextEmbeddingsError(RuntimeError):
    """获取文本向量失败。"""

    def __init__(self):
        super().__init__("获取文本向量失败。")


class GetRerankScoresError(RuntimeError):
    """获取rerank得分失败。"""

    def __init__(self):
        super().__init__("获取rerank得分失败。")
