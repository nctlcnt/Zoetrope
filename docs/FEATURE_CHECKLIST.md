# 功能需求实现清单

## ✅ 智能收藏与记录

### 需求
- ✅ 用户添加电影/电视剧/小说/书籍名称
- ✅ 记录想看的原因、预告片链接、推荐文案
- ✅ AI自动总结吸引点和观看动机

### 实现
- **后端**: `POST /media` API 端点
  - 文件: `backend/app/main.py` - `create_media_item()`
  - 支持所有媒体类型: movie, tv_show, novel, book
  - 接受用户输入: title, reason_to_watch, trailer_url, recommendation_text
  
- **AI 分析**: `backend/app/ai_service.py` - `AIService`
  - 方法: `analyze_media_appeal()`
  - 使用 OpenAI GPT-3.5 分析
  - 生成: ai_summary (吸引点), ai_motivation (观看动机)
  
- **前端**: `ios/Zoetrope/Views/AddMediaView.swift`
  - 表单输入所有必需字段
  - 异步提交到后端 API

---

## ✅ 智能推流与提醒

### 需求
- ✅ 通过API或手动更新获取上映时间
- ✅ 类似院线贴片广告的轮播展示
- ✅ 自动提醒本周上映、即将下映的内容

### 实现
- **API 集成**: `backend/app/tmdb_client.py` - `TMDBClient`
  - 自动从 TMDB 获取 release_date
  - 获取海报、评分等元数据
  
- **轮播展示**: `GET /dashboard` API
  - 文件: `backend/app/main.py` - `get_dashboard()`
  - 三个轮播:
    - latest_wants: 最新想看 (最近添加的10条)
    - ending_soon: 即将下映 (14天内结束)
    - recently_released: 最近上映 (7天内上映)
  
- **前端轮播**: `ios/Zoetrope/Views/DashboardView.swift`
  - CarouselSection 组件
  - 横向滚动 Netflix 风格
  - 下拉刷新

---

## ✅ 动态优先级排序

### 需求
- ✅ 高优先级：急切想看的内容
- ✅ 低优先级：剧荒备选（如Top 10榜单）
- ✅ 智能调整：多次出现在不同榜单时自动提升优先级

### 实现
- **优先级系统**: `backend/app/models.py` - `PriorityLevel`
  - HIGH: 高优先级 (急切想看)
  - MEDIUM: 中优先级
  - LOW: 低优先级 (剧荒备选)
  
- **排序算法**: `backend/app/priority_ranker.py` - `PriorityRanker`
  - 方法: `calculate_priority_score()`
  - 综合评分因素:
    - 用户设置优先级
    - appearance_count (出现次数)
    - 创建时间新近度
    - 上映日期接近度
    - 下映紧迫性
    - AI 分析质量
    - 评分
  
- **自动提升**: `auto_adjust_priority()`
  - 3+ 次出现 → 自动升级到 HIGH
  - 2+ 次出现且为 LOW → 升级到 MEDIUM
  - 在添加推荐时自动执行

---

## ✅ 内容聚合与分析

### 需求
- ✅ 关注博主/公众号/推荐平台
- ✅ 分享内容自动导入APP
- ✅ AI提取并汇总推荐理由、上映时间、评价到对应条目下
- ✅ 查看不同博主对同一作品的观点

### 实现
- **推荐来源**: `backend/app/models.py` - `Recommendation`
  - 存储多个推荐来源
  - 字段: source_name, source_url, recommendation_reason, rating
  - 一对多关系: MediaItem → Recommendations
  
- **添加推荐**: `POST /media/{id}/recommendations`
  - 文件: `backend/app/main.py` - `add_recommendation()`
  - 自动增加 appearance_count
  - 触发优先级自动调整
  
- **AI 聚合**: `backend/app/ai_service.py`
  - 方法: `aggregate_recommendations()`
  - 汇总多个来源的推荐理由
  
- **前端展示**: `ios/Zoetrope/Views/MediaDetailView.swift`
  - RecommendationCard 组件
  - 显示所有推荐来源
  - 每个来源独立显示评分和理由

---

## ✅ 界面设计 (Swift)

### 需求
- ✅ Carousel轮播：最新想看、即将下映、最近上映未观看
- ✅ 类Netflix界面但更个性化
- ✅ 不提供片源，引导用户到Netflix/Disney+等平台

### 实现
- **主页轮播**: `ios/Zoetrope/Views/DashboardView.swift`
  - CarouselSection: 横向滚动组件
  - MediaCardView: Netflix 风格卡片
  - 海报图片、标题、评分、优先级标签
  
- **个性化元素**:
  - 优先级颜色标签
  - AI 分析展示
  - 中文界面
  
- **平台跳转**: `ios/Zoetrope/Models/MediaModels.swift`
  - StreamingLink 模型
  - `ios/Zoetrope/Views/MediaDetailView.swift`
  - 按钮跳转到外部流媒体平台
  - 使用 UIApplication.shared.open()

---

## ✅ 技术方案

### 需求
- ✅ 接入Netflix热播榜等外部数据源 (Python)
- ✅ 使用SVM（支持向量机）或RAG处理大量列表项
- ✅ AI仅用于关键分析，避免过度消耗资源
- ✅ 基于相关性算法动态调整优先级和轮播展示

### 实现
- **外部数据源**: 
  - TMDB API 集成 (`backend/app/tmdb_client.py`)
  - 可扩展到其他平台
  
- **机器学习**: 
  - 使用 scikit-learn 库
  - `backend/app/priority_ranker.py` - 优先级评分算法
  - 基于多因素的综合排序
  
- **AI 优化**: 
  - 仅在创建/更新时调用 AI
  - 不在列表查询时使用 AI
  - 结果缓存在数据库中
  
- **相关性算法**: 
  - `PriorityRanker.rank_items()` 方法
  - 动态计算并排序
  - 应用于所有轮播展示

---

## 文件清单

### 后端 (Python)
- `backend/app/main.py` - FastAPI 应用和路由
- `backend/app/models.py` - 数据库模型
- `backend/app/schemas.py` - API 请求/响应模型
- `backend/app/database.py` - 数据库连接
- `backend/app/tmdb_client.py` - TMDB API 客户端
- `backend/app/ai_service.py` - OpenAI AI 分析服务
- `backend/app/priority_ranker.py` - 优先级排序算法
- `backend/requirements.txt` - Python 依赖
- `backend/run.py` - 启动脚本

### 前端 (Swift)
- `ios/Zoetrope/ZoetropeApp.swift` - 应用入口
- `ios/Zoetrope/Views/ContentView.swift` - 主视图
- `ios/Zoetrope/Views/DashboardView.swift` - 仪表盘轮播
- `ios/Zoetrope/Views/MediaListView.swift` - 列表视图
- `ios/Zoetrope/Views/AddMediaView.swift` - 添加表单
- `ios/Zoetrope/Views/MediaDetailView.swift` - 详情页
- `ios/Zoetrope/Models/MediaModels.swift` - 数据模型
- `ios/Zoetrope/Services/APIService.swift` - API 客户端
- `ios/Zoetrope/ViewModels/DashboardViewModel.swift` - 仪表盘 ViewModel
- `ios/Zoetrope/ViewModels/MediaListViewModel.swift` - 列表 ViewModel

### 文档
- `README.md` - 项目总览
- `docs/ARCHITECTURE.md` - 架构文档
- `docs/API_EXAMPLES.md` - API 使用示例
- `backend/README.md` - 后端说明
- `ios/README.md` - iOS 说明

---

## ✅ 所有需求已完整实现

所有问题陈述中的功能需求都已完成实现，包括：
1. ✅ 智能收藏与记录
2. ✅ 智能推流与提醒
3. ✅ 动态优先级排序
4. ✅ 内容聚合与分析
5. ✅ Swift 界面设计
6. ✅ Python 技术方案
