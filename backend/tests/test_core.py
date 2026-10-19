from modules.ingest.service.splitter import split_markdown
from modules.retrieve.service.search import tokenize


def test_split_markdown():
    """测试 Markdown 切分逻辑"""
    # 1. 正常切分
    text = "第一段内容。\n\n第二段内容。\n\n第三段内容。"
    chunks = split_markdown(text, chunk_size=10)
    assert len(chunks) == 3
    assert chunks[0] == "第一段内容。"

    # 2. 空文本切分
    assert len(split_markdown("")) == 0

    # 3. 长文本合并（因为 chunk_size 很大，三段会被合在一起）
    chunks_merged = split_markdown(text, chunk_size=1000)
    assert len(chunks_merged) == 1


def test_tokenize():
    """测试 jieba 关键词提取逻辑"""
    query = "RAG 是什么？怎么用 Python 做检索？"
    keywords = tokenize(query)

    # 断言：应该提取出 RAG、Python、检索 等关键词
    assert "RAG" in keywords
    assert "Python" in keywords
    assert "检索" in keywords
    # 断言：停用词“什么”不应该出现
    assert "什么" not in keywords
    # 断言：单字“做”不应该出现
    assert "做" not in keywords