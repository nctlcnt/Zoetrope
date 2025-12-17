# Zoetrope

智能影视追踪系统 - Smart Media Tracking System

Zoetrope 是一个智能的电影、电视剧、小说和书籍追踪应用，帮助用户管理想看的内容，提供个性化推荐和提醒。

## 功能特点

### 🎬 智能收藏与记录
- 添加电影/电视剧/小说/书籍
- 记录想看的原因、预告片链接、推荐文案
- AI 自动总结吸引点和观看动机

### 📺 智能推流与提醒
- 通过 TMDB API 自动获取上映时间
- 类似院线贴片广告的轮播展示
- 自动提醒本周上映、即将下映的内容

### 🎯 动态优先级排序
- **高优先级**：急切想看的内容
- **中优先级**：一般感兴趣的内容
- **低优先级**：剧荒备选（如 Top 10 榜单）
- **智能调整**：多次出现在不同榜单时自动提升优先级

### 📊 内容聚合与分析
- 支持多个来源的推荐（博主/公众号/推荐平台）
- AI 提取并汇总推荐理由、上映时间、评价
- 查看不同来源对同一作品的观点

### 🎨 界面设计
- **Carousel 轮播**：最新想看、即将下映、最近上映未观看
- 类 Netflix 界面但更个性化
- 不提供片源，引导用户到 Netflix/Disney+ 等平台

## 技术栈

### 后端 (Python)
- **FastAPI**: 高性能 Web 框架
- **SQLAlchemy**: ORM 数据库管理
- **OpenAI API**: AI 内容分析
- **Scikit-learn**: 机器学习优先级排序
- **TMDB API**: 电影/电视剧数据获取

### 前端 (Swift/SwiftUI)
- **SwiftUI**: 现代化 iOS 界面
- **Async/Await**: 异步网络请求
- **MVVM 架构**: 清晰的代码结构

## 快速开始

### 后端设置

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API keys
```

需要的 API Keys:
- `OPENAI_API_KEY`: OpenAI API key (用于 AI 分析)
- `TMDB_API_KEY`: TMDB API key (从 https://www.themoviedb.org/settings/api 获取)

3. **运行后端**
```bash
python run.py
```

后端将在 `http://localhost:8000` 运行

4. **查看 API 文档**
访问 `http://localhost:8000/docs` 查看自动生成的 API 文档

### iOS 应用设置

1. **更新 API 地址**
编辑 `ios/Zoetrope/Services/APIService.swift`，将 `baseURL` 改为你的后端地址

2. **使用 Xcode 打开项目**
```bash
open ios/Zoetrope
```

3. **运行应用**
在 Xcode 中选择模拟器或真机，点击运行

## API 端点

### 媒体管理
- `POST /media` - 创建媒体项目
- `GET /media` - 获取媒体列表（支持过滤）
- `GET /media/{id}` - 获取单个媒体详情
- `PATCH /media/{id}` - 更新媒体项目
- `DELETE /media/{id}` - 删除媒体项目

### 推荐管理
- `POST /media/{id}/recommendations` - 添加推荐来源

### 流媒体链接
- `POST /media/{id}/streaming-links` - 添加流媒体平台链接

### 仪表盘
- `GET /dashboard` - 获取主页轮播数据（最新想看、即将下映、最近上映）

## 项目结构

```
Zoetrope/
├── backend/                # Python 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py        # FastAPI 应用和路由
│   │   ├── models.py      # 数据库模型
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # 数据库连接
│   │   ├── tmdb_client.py # TMDB API 客户端
│   │   ├── ai_service.py  # AI 分析服务
│   │   └── priority_ranker.py  # 优先级排序算法
│   ├── requirements.txt
│   └── run.py
├── ios/                   # Swift iOS 应用
│   └── Zoetrope/
│       ├── Models/        # 数据模型
│       ├── Views/         # SwiftUI 视图
│       ├── ViewModels/    # 视图模型
│       ├── Services/      # API 服务
│       └── Utils/         # 工具类
└── README.md
```

## 核心功能说明

### AI 分析
当用户添加新的媒体项目时，系统会：
1. 从 TMDB 获取基本信息（海报、评分、上映日期）
2. 使用 OpenAI API 分析用户输入的理由和推荐文案
3. 生成吸引点总结和观看动机

### 优先级算法
优先级分数基于以下因素计算：
- 用户设置的优先级（高/中/低）
- 出现次数（在多个榜单中出现）
- 添加时间新近程度
- 上映日期接近程度
- 下映日期紧迫性
- AI 分析质量
- 评分

### 自动提升优先级
- 出现在 3+ 个榜单 → 自动升级到高优先级
- 出现在 2+ 个榜单且为低优先级 → 升级到中优先级

## 开发计划

- [ ] 添加通知推送功能
- [ ] 支持更多流媒体平台
- [ ] 添加社交分享功能
- [ ] 支持自定义轮播类别
- [ ] 添加观看历史统计
- [ ] 支持导入豆瓣/IMDB 数据

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！