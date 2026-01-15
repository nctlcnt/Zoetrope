# Zoetrope

一个以用户为中心的媒体收藏推荐 APP，通过 AI 辅助和智能排序算法，帮助用户管理想看的电影、电视剧等内容。

## 功能特性

- **智能收藏**: 从 TMDB 搜索并添加电影/电视剧到个人收藏
- **轮播推荐**: 基于上映时间、热度、用户兴趣的智能推送
- **AI 分析**: 自动提取和生成评论总结
- **优先级排序**: 多维度评分系统（时间紧迫性、热度、用户偏好）
- **评论管理**: 论坛式的评论展示，支持从博文/榜单导入

## 技术架构

### Backend
| 组件 | 技术 |
|------|------|
| 框架 | Python 3.11+ / FastAPI |
| 数据库 | PostgreSQL |
| 缓存 | Redis |
| 向量数据库 | Chroma / Pinecone |
| AI | OpenAI API |
| 外部数据 | TMDB API |

### iOS App
| 组件 | 技术 |
|------|------|
| 语言 | Swift 5.9+ |
| UI 框架 | SwiftUI |
| 最低版本 | iOS 15.0 |

## 快速开始

### 前置要求
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Xcode 15+ (iOS 开发)

### Backend 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/Zoetrope.git
cd Zoetrope

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r Backend/requirements.txt

# 配置环境变量
cp Backend/.env.example Backend/.env
# 编辑 .env 填入 API 密钥等配置

# 启动开发服务器
uvicorn Backend.app:app --reload --port 8000
```

### iOS App

使用 Xcode 打开 `Zoetrope/Zoetrope.xcodeproj`，选择模拟器或真机运行。

## 项目结构

```
Zoetrope/
├── Backend/                # Python 后端服务
│   ├── app.py             # FastAPI 应用入口
│   ├── config.py          # 配置管理
│   ├── routers/           # API 路由层
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑层
│   └── database/          # 数据库连接
├── Zoetrope/              # iOS SwiftUI 应用
│   └── Zoetrope/
│       ├── Models/        # 数据模型
│       ├── Views/         # UI 视图
│       └── Services/      # 网络服务
├── Shared/                # 跨平台共享模型
├── CLAUDE.md              # Claude Code 开发指南
└── version_roadmap.md     # 版本路线图
```

## API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/tmdb/search` | TMDB 搜索 |
| GET | `/api/media` | 获取媒体列表 |
| POST | `/api/media` | 添加媒体 |
| GET | `/api/media/{id}` | 获取媒体详情 |
| POST | `/api/inbox` | 添加到收集箱 |

## 开发路线图

参见 [version_roadmap.md](./version_roadmap.md)

### 当前版本: 0.01
- TMDB 搜索功能
- 基础媒体添加流程
- 简单列表展示

### 计划功能
- URL/博文解析
- 关注博主自动抓取
- 书籍/小说支持
- 高级推荐算法

## 环境变量

| 变量 | 描述 | 必需 |
|------|------|------|
| `TMDB_API_KEY` | TMDB API 密钥 | 是 |
| `DATABASE_URL` | PostgreSQL 连接字符串 | 是 |
| `REDIS_URL` | Redis 连接字符串 | 否 |
| `AI_API_KEY` | OpenAI API 密钥 | 否 |

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT License
