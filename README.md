# 个人知识库管理系统(personal-knowledge-base)
把自己收藏的散落的文档、笔记、链接丢进来，用自然语言提问，答案带出处。

## 解决什么问题
收藏夹吃灰、笔记散落各处，信息越攒越多却越没法用。
这个系统让你：随手丢进去 → 一句话问出来 → 知道答案从哪来。

## 技术栈
| 层 | 选型 |
|---|---|
| 前端 | React + Vite + TypeScript |
| 后端 | Python 3.11 + FastAPI |
| 数据库 | PostgreSQL 16 + pgvector |
| ORM | SQLAlchemy 2.0 |
| 检索 | 向量检索（pgvector）+ 关键词检索（tsvector） |
| LLM | DeepSeek API |
| Agent | 自研步进式状态机 |
| 测试 | pytest |
| CI/CD | GitHub Actions |

## 目录结构
```
personal-knowledge-base/
├── backend/
│   ├── modules/
│   │   ├── ingest/          # 知识收录：上传、切分、向量化
│   │   │   ├── controller/  # HTTP 接口
│   │   │   ├── service/     # 业务逻辑
│   │   │   ├── domain/      # 领域模型（Document, Chunk）
│   │   │   └── repository/  # 数据访问
│   │   ├── retrieve/        # 检索：向量 + 关键词混合召回
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   ├── domain/
│   │   │   └── repository/
│   │   ├── qa/              # 问答：生成答案 + 溯源
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   └── domain/
│   │   ├── agent/           # Agent 工作流
│   │   │   ├── controller/
│   │   │   ├── service/
│   │   │   └── tools/       # 桥接层，调其他模块
│   │   └── manage/          # 知识管理：分类、标签、更新
│   │       ├── controller/
│   │       ├── service/
│   │       ├── domain/
│   │       └── repository/
│   ├── shared/              # 公共工具
│   │   ├── db.py            # 数据库连接
│   │   ├── llm.py           # LLM 客户端
│   │   └── config.py        # 配置
│   ├── main.py              # FastAPI 入口
│   └── tests/               # 测试
├── frontend/
│   └── src/
│       ├── pages/           # 页面
│       ├── api/             # 调后端接口
│       └── components/      # 组件
├── README.md
└── .gitignore
```

## 如何本地运行

### 依赖
- Python 3.11+
- PostgreSQL 16 + pgvector 扩展
- Node.js 18+
- Docker

### 1. 启动数据库
用 Docker 起 PostgreSQL + pgvector：

```bash
docker run -d \
  --name pkb-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=pkb \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```
这会启动一个带 pgvector 扩展的 PostgreSQL，端口 5432。

### 2. 启动后端
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # 填入数据库连接、LLM API Key
uvicorn main:app --reload
```
后端跑在 http://localhost:8000
Swagger 文档：http://localhost:8000/docs

### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```
前端跑在 http://localhost:5173

## 项目文档
- 产品需求文档：见 [Issue #1](../../issues/1)
- 架构设计文档：见 [Issue #2](../../issues/2)
- 模块子 Issue：
  - [知识收录 #3](../../issues/3)
  - [检索 #4](../../issues/4)
  - [问答 #5](../../issues/5)
  - [Agent #6](../../issues/6)
  - [知识管理 #7](../../issues/7)

## 开发规范
- 不在 main 分支直接 commit
- 每个功能一个 PR，PR 关联 Issue
- 合并用 Squash Merge
- 保证 main 分支始终可编译运行

## License
MIT
