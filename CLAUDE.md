# Zoetrope - Claude Code 开发指南

## 项目概述

Zoetrope 是一个媒体收藏推荐 APP，通过 AI 辅助和智能排序算法帮助用户管理想看的电影、电视剧等内容。

## 技术栈

### Backend (Python)
- **框架**: FastAPI + Uvicorn
- **数据库**: PostgreSQL (asyncpg + SQLAlchemy) / Supabase
- **缓存**: Redis
- **AI**: OpenAI API (GPT-4o-mini, embeddings)
- **向量数据库**: Chroma (开发) / Pinecone / Weaviate / Milvus
- **外部 API**: TMDB

### Frontend (iOS)
- **语言**: Swift
- **框架**: SwiftUI
- **最低版本**: iOS 15+

## 项目结构

```
Zoetrope/
├── Backend/                 # Python 后端
│   ├── app.py              # FastAPI 入口
│   ├── config.py           # 配置管理
│   ├── routers/            # API 路由
│   │   ├── search.py       # 统一搜索
│   │   ├── media.py        # 媒体 CRUD
│   │   ├── comment.py      # 评论管理
│   │   ├── inbox.py        # 收集箱
│   │   └── tmdb.py         # TMDB 搜索
│   ├── models/             # 数据模型
│   │   ├── media.py
│   │   ├── comment.py
│   │   └── inbox.py
│   ├── services/           # 业务逻辑
│   │   ├── supabase.py     # Supabase 客户端
│   │   ├── ai.py           # AI 服务
│   │   ├── scoring.py      # 评分算法
│   │   ├── tmdb.py         # TMDB 客户端
│   │   ├── vector_db.py    # 向量检索
│   │   └── redis.py        # 缓存服务
│   ├── database/           # 数据库连接
│   └── migrations/         # SQL 迁移脚本
├── Zoetrope/               # iOS 前端
│   └── Zoetrope/
│       ├── Models/         # 数据模型
│       ├── Views/          # SwiftUI 视图
│       ├── Services/       # API 客户端
│       └── ContentView.swift
├── Shared/                 # 共享模型定义
└── version_roadmap.md      # 版本路线图
```

## 开发命令

### Backend
```bash
# 进入后端目录
cd Backend

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn Backend.app:app --reload --host 0.0.0.0 --port 8000

# 或从项目根目录
python -m uvicorn Backend.app:app --reload
```

### 环境变量
复制 `Backend/.env.example` 为 `Backend/.env` 并配置：
- `TMDB_API_KEY`: TMDB API 密钥
- `DATABASE_URL`: PostgreSQL 连接字符串 (支持 Supabase)
- `SUPABASE_URL`: Supabase 项目 URL
- `SUPABASE_SERVICE_KEY`: Supabase service_role 密钥
- `REDIS_URL`: Redis 连接字符串
- `AI_API_KEY`: OpenAI API 密钥

### Supabase 设置
1. 在 [Supabase](https://supabase.com) 创建项目
2. 从 Settings -> API 获取 URL 和 Keys
3. 从 Settings -> Database 获取连接字符串
4. 在 SQL Editor 运行 `Backend/migrations/001_initial_schema.sql`

## 代码规范

### Python
- 使用 Pydantic 进行数据验证
- 异步优先 (async/await)
- 类型注解必须完整
- 中文注释

### Swift
- 遵循 SwiftUI 最佳实践
- 使用 @Published 和 @StateObject 进行状态管理
- 错误处理使用 Result 类型

## 数据模型

### Media (媒体条目)
- `id`, `title`, `type` (movie/tv)
- `tmdb_id`, `release_date`, `poster_url`
- `user_score`, `priority_score`, `mention_count`

### Comment (评论)
- `id`, `media_id`, `content`
- `source` (user/ai/imported)
- `sentiment_score`

### Inbox (收集箱)
- `id`, `raw_content`, `url`
- `processed`, `expires_at`

## 当前开发阶段

参考 `version_roadmap.md` 了解当前版本目标和待办事项。

**0.01 版本目标**: 实现 TMDB 搜索添加媒体的基础流程
