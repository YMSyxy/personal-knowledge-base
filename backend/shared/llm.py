import httpx
from shared.config import LLM_API_KEY, LLM_BASE_URL


async def chat_completion(prompt: str) -> str:
    """调用 DeepSeek API 生成回答"""
    if not LLM_API_KEY:
        raise ValueError("未配置 LLM_API_KEY，请检查 backend/.env 文件")

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{LLM_BASE_URL}/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60.0,
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]