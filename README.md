# 个人知识库管理系统 (personal-knowledge-base)

把散落的文档、笔记、链接丢进来，用自然语言提问，答案带出处。

## 解决什么问题

收藏夹吃灰、笔记散落各处，信息越攒越多却越没法用。
这个系统让你：随手丢进去 → 一句话问出来 → 知道答案从哪来。

## 功能演示

- 📄 **上传**：支持 `.md` 格式资料上传，自动切分入库。
- 🔍 **检索**：基于 jieba 分词的关键词召回。
- 🤖 **问答**：结合检索内容，调用 DeepSeek 大模型生成答案。
- 🔗 **溯源**：答案自带 `[1]` 角标，并展示原文切片来源。

## 技术栈

| 层 | 选型 |
|---|---|
| 前端 | React + Vite + TypeScript |
| 后端 | Python 3.11 + FastAPI |
| 数据库 | SQLite（开发阶段）→ PostgreSQL + pgvector（生产计划） |
| 检索 | 向量检索（计划中）+ 关键词检索（jieba） |
| LLM | DeepSeek API |
| Agent | 自研步进式状态机（计划中） |

## 如何本地运行

### 1. 环境准备
- Python 3.11+
- Node.js 18+
- 一个 DeepSeek API Key（[获取地址](https://platform.deepseek.com/)）

### 2. 启动后端
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows 用 .venv\Scripts\activate
pip install -r requirements.txt

# 配置环境变量：复制 .env.example 为 .env，并填入你的 API Key
cp .env.example .env

# 启动后端
uvicorn main:app --reload