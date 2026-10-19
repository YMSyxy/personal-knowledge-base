from sqlalchemy.orm import Session

from modules.retrieve.service.search import search
from shared.llm import chat_completion


async def ask_question(db: Session, question: str, top_k: int = 3) -> dict:
    """问答入口：检索 -> 拼 Prompt -> 调 LLM -> 返回"""
    # 1. 检索
    search_result = search(db, question, top_k=top_k)
    chunks = search_result.get("results", [])

    if not chunks:
        return {
            "answer": "抱歉，知识库中没有找到与您问题相关的内容，我无法回答。",
            "sources": [],
        }

    # 2. 拼装 Prompt
    context_text = ""
    for i, chunk in enumerate(chunks):
        context_text += f"[{i + 1}] {chunk['content']}\n\n"

    prompt = f"""你是一个个人知识库助手。请严格根据下面提供的资料回答用户的问题。
如果资料中不包含答案，请直接回答"根据已有资料，我无法回答该问题"，不要编造。
回答时请尽量精简，并在答案末尾用 [1]、[2] 的形式标注引用了哪几条资料。

资料：
{context_text}

用户问题：{question}
"""

    # 3. 调用 LLM
    answer = await chat_completion(prompt)

    # 4. 返回结果
    sources = [
        {
            "chunk_id": c["chunk_id"],
            "document_id": c["document_id"],
            "content": c["content"],
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }