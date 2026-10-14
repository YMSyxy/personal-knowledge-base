def split_markdown(content: str, chunk_size: int = 500) -> list[str]:
    """
    简单的按段落切分：
    1. 按空行分段
    2. 段落合并，直到接近 chunk_size
    3. 返回 chunks 列表
    """
    if not content.strip():
        return []

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = f"{current}\n\n{para}" if current else para
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    return chunks