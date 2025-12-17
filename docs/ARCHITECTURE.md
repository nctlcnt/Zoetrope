# Zoetrope 架构文档

## 系统概述

Zoetrope 是一个智能影视追踪系统，帮助用户管理和发现想看的电影、电视剧、小说和书籍。系统采用前后端分离架构，后端使用 Python/FastAPI，前端使用 Swift/SwiftUI。

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    iOS App (Swift)                       │
│  ┌──────────┬──────────┬──────────┬──────────────────┐  │
│  │Dashboard │MediaList │AddMedia  │MediaDetail       │  │
│  │View      │View      │View      │View              │  │
│  └────┬─────┴────┬─────┴────┬─────┴────┬─────────────┘  │
│       │          │          │          │                │
│  ┌────▼──────────▼──────────▼──────────▼─────────────┐  │
│  │         ViewModels (MVVM)                          │  │
│  └────────────────────┬───────────────────────────────┘  │
│                       │                                  │
│  ┌────────────────────▼───────────────────────────────┐  │
│  │         APIService (REST Client)                   │  │
│  └────────────────────┬───────────────────────────────┘  │
└───────────────────────┼───────────────────────────────┘
                        │ HTTP/JSON
                        │
┌───────────────────────▼───────────────────────────────┐
│            FastAPI Backend (Python)                    │
│  ┌──────────────────────────────────────────────────┐ │
│  │  REST API Endpoints                              │ │
│  │  /media, /dashboard, /recommendations, etc.      │ │
│  └─────┬─────┬──────────┬──────────┬─────────────────┘ │
│        │     │          │          │                   │
│  ┌─────▼──┐ ┌▼────────┐ ┌▼────────┐ ┌▼──────────────┐ │
│  │TMDB    │ │AI       │ │Priority │ │Database       │ │
│  │Client  │ │Service  │ │Ranker   │ │Manager        │ │
│  └────────┘ └────┬────┘ └─────────┘ └────┬──────────┘ │
│                  │                        │            │
│            ┌─────▼────────┐        ┌──────▼─────────┐ │
│            │ OpenAI API   │        │ SQLite DB      │ │
│            └──────────────┘        └────────────────┘ │
│                  │                                     │
│            ┌─────▼────────┐                           │
│            │  TMDB API    │                           │
│            └──────────────┘                           │
└───────────────────────────────────────────────────────┘
```

## 核心功能模块

### 1. 智能收藏与记录

**功能描述:**
- 用户可以添加电影/电视剧/小说/书籍
- 记录想看的原因、预告片链接、推荐文案
- AI 自动总结吸引点和观看动机

**技术实现:**
- **后端**: `POST /media` API 端点
- **AI 分析**: 使用 OpenAI GPT-3.5 分析用户输入
- **数据丰富**: TMDB API 自动获取海报、评分、上映时间
- **数据库**: MediaItem 模型存储完整信息

### 2. 智能推流与提醒

**功能描述:**
- 通过 API 自动获取上映时间
- 类似院线贴片广告的轮播展示
- 自动提醒本周上映、即将下映的内容

**技术实现:**
- **数据源**: TMDB API 获取 release_date 和 end_date
- **轮播逻辑**: `/dashboard` 端点返回三个轮播
  - 最新想看: 按创建时间排序
  - 即将下映: 14天内结束的内容
  - 最近上映: 7天内上映的内容
- **UI**: SwiftUI CarouselSection 组件

### 3. 动态优先级排序

**功能描述:**
- 高优先级: 急切想看的内容
- 中优先级: 一般感兴趣的内容
- 低优先级: 剧荒备选
- 智能调整: 多次出现在不同榜单时自动提升优先级

**技术实现:**
- **算法**: `PriorityRanker` 类计算综合优先级分数
- **评分因素**:
  - 用户设置优先级 (0-100分)
  - 出现次数 (0-50分)
  - 添加时间新近度 (0-20分)
  - 上映日期接近度 (0-30分)
  - 下映紧迫性 (0-50分)
  - AI 分析质量 (0-10分)
  - 评分 (0-20分)
- **自动提升**:
  - 3+ 次出现 → 高优先级
  - 2+ 次出现且为低优先级 → 中优先级

### 4. 内容聚合与分析

**功能描述:**
- 支持多个推荐来源 (博主/公众号/推荐平台)
- AI 提取并汇总推荐理由
- 查看不同来源对同一作品的观点

**技术实现:**
- **数据模型**: Recommendation 表存储多个推荐来源
- **关联**: 一对多关系 (MediaItem → Recommendations)
- **AI 聚合**: `aggregate_recommendations()` 方法
- **展示**: iOS MediaDetailView 显示所有推荐

### 5. 界面设计

**功能描述:**
- Carousel 轮播展示
- 类 Netflix 界面但更个性化
- 不提供片源，引导到 Netflix/Disney+ 等平台

**技术实现:**
- **SwiftUI 组件**:
  - DashboardView: 主页轮播
  - CarouselSection: 横向滚动组件
  - MediaCardView: Netflix 风格卡片
- **导航**: NavigationLink 到详情页
- **平台跳转**: StreamingLink 模型 + UIApplication.shared.open()

## 数据模型

### MediaItem (媒体项目)
```python
- id: 主键
- title: 标题
- media_type: 类型 (movie/tv_show/novel/book)
- status: 状态 (want_to_watch/watching/watched/dropped)
- priority: 优先级 (high/medium/low)
- reason_to_watch: 想看原因
- trailer_url: 预告片链接
- recommendation_text: 推荐文案
- release_date: 上映时间
- end_date: 下映时间
- tmdb_id: TMDB ID
- poster_url: 海报 URL
- rating: 评分
- ai_summary: AI 总结的吸引点
- ai_motivation: AI 提取的观看动机
- appearance_count: 出现次数
```

### Recommendation (推荐来源)
```python
- id: 主键
- media_item_id: 关联的媒体项目
- source_name: 来源名称
- source_url: 来源链接
- recommendation_reason: 推荐理由
- rating: 评分
- review_date: 评论日期
```

### StreamingLink (流媒体链接)
```python
- id: 主键
- media_item_id: 关联的媒体项目
- platform: 平台名称 (Netflix/Disney+/etc)
- url: 链接
- available: 是否可用
```

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
- `GET /dashboard` - 获取主页轮播数据

## 技术栈

### 后端
- **Web 框架**: FastAPI (高性能异步框架)
- **ORM**: SQLAlchemy (数据库管理)
- **数据库**: SQLite (轻量级，适合单机应用)
- **AI**: OpenAI API (GPT-3.5)
- **机器学习**: Scikit-learn (优先级排序)
- **外部 API**: TMDB (电影/电视剧数据)

### 前端 (iOS)
- **UI 框架**: SwiftUI (现代化 iOS UI)
- **架构**: MVVM (Model-View-ViewModel)
- **网络**: URLSession + Async/Await
- **最低版本**: iOS 16.0+

## 部署方案

### 开发环境
```bash
# 后端
cd backend
pip install -r requirements.txt
python run.py

# iOS
open ios/Zoetrope 在 Xcode 中打开
```

### 生产环境
- **后端**: 使用 Docker 容器化部署
- **数据库**: 可切换到 PostgreSQL
- **前端**: 通过 TestFlight 或 App Store 分发

## 安全考虑

1. **API Keys**: 使用环境变量存储，不提交到代码库
2. **HTTPS**: 生产环境必须使用 HTTPS
3. **认证**: 未来可添加 JWT 认证
4. **输入验证**: Pydantic 模型自动验证输入

## 性能优化

1. **数据库索引**: title, tmdb_id, priority 等字段建立索引
2. **缓存**: TMDB API 响应可缓存
3. **分页**: 列表接口支持分页 (skip/limit)
4. **异步**: FastAPI 使用异步处理提高并发

## 未来扩展

1. **推送通知**: iOS 推送上映提醒
2. **社交功能**: 分享推荐给好友
3. **统计分析**: 观看历史、时间统计
4. **多平台**: Android/Web 版本
5. **协同过滤**: 基于用户行为的推荐算法
6. **数据导入**: 豆瓣/IMDB 数据导入
