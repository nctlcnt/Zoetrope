# Zoetrope 快速入门指南

## 🎯 项目简介

Zoetrope 是一个智能影视追踪系统，帮助您管理想看的内容，通过 AI 分析提供个性化推荐。

## 🌟 核心特性

### 1️⃣ 智能添加
添加电影/剧集/书籍，AI 自动分析吸引点

### 2️⃣ 个性化轮播
三个智能轮播：最新想看 | 即将下映 | 最近上映

### 3️⃣ 动态排序
基于多因素的智能优先级系统

### 4️⃣ 多源推荐
聚合不同来源的推荐意见

## 📱 界面预览

```
┌─────────────────────────────────────┐
│        🎬 Zoetrope                  │
├─────────────────────────────────────┤
│  最新想看 →                         │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
│  │🎥 │ │📺 │ │📖 │ │🎬 │  ←滑动   │
│  └───┘ └───┘ └───┘ └───┘          │
├─────────────────────────────────────┤
│  即将下映 →                         │
│  ┌───┐ ┌───┐ ┌───┐               │
│  │🎥 │ │📺 │ │🎬 │               │
│  └───┘ └───┘ └───┘               │
├─────────────────────────────────────┤
│  最近上映 →                         │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐          │
│  │🎥 │ │📺 │ │📖 │ │🎬 │          │
│  └───┘ └───┘ └───┘ └───┘          │
└─────────────────────────────────────┘
```

## 🚀 5分钟快速启动

### 步骤 1: 启动后端

```bash
# 克隆项目
git clone https://github.com/nctlcnt/Zoetrope.git
cd Zoetrope

# 使用快速启动脚本
chmod +x start.sh
./start.sh
```

或手动启动:

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件，添加 API keys (可选)
python run.py
```

后端将在 `http://localhost:8000` 运行

### 步骤 2: 配置 iOS 应用

编辑 `ios/Zoetrope/Services/APIService.swift`:

```swift
private let baseURL = "http://localhost:8000"
// 如果在真机测试，改为你的电脑 IP，如:
// private let baseURL = "http://192.168.1.100:8000"
```

### 步骤 3: 运行 iOS 应用

```bash
cd ios
open Zoetrope  # 在 Xcode 中打开
# 选择模拟器或真机，点击运行
```

## 📖 使用示例

### 添加一部电影

**iOS 应用中:**
1. 点击底部 "添加" 标签
2. 输入标题: "星际穿越"
3. 选择类型: 电影
4. 设置优先级: 高优先级
5. 想看原因: "诺兰导演的科幻力作"
6. 点击 "添加"

**API 方式:**
```bash
curl -X POST "http://localhost:8000/media" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "星际穿越",
    "media_type": "movie",
    "priority": "high",
    "reason_to_watch": "诺兰导演的科幻力作"
  }'
```

### 添加推荐来源

```bash
curl -X POST "http://localhost:8000/media/1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "source_name": "豆瓣电影",
    "recommendation_reason": "经典科幻，视觉震撼",
    "rating": 9.3
  }'
```

### 查看仪表盘

```bash
curl "http://localhost:8000/dashboard"
```

## 🔑 API Keys 配置 (可选)

### OpenAI (用于 AI 分析)
1. 访问 https://platform.openai.com/api-keys
2. 创建新的 API key
3. 在 `backend/.env` 中设置 `OPENAI_API_KEY=your-key`

### TMDB (用于电影数据)
1. 访问 https://www.themoviedb.org/settings/api
2. 申请 API key (免费)
3. 在 `backend/.env` 中设置 `TMDB_API_KEY=your-key`

**注意**: 不配置这些 keys 时，应用仍可正常使用，只是 AI 分析和自动数据获取功能会被禁用。

## 📊 优先级系统说明

### 三个优先级等级

- 🔴 **高优先级**: 急切想看的内容
- 🟠 **中优先级**: 一般感兴趣的内容
- 🟢 **低优先级**: 剧荒备选

### 自动提升规则

- 出现在 **3个或更多** 推荐来源 → 自动升级到 **高优先级**
- 出现在 **2个或更多** 推荐来源且当前为低优先级 → 升级到 **中优先级**

### 排序因素

系统综合以下因素计算优先级分数:
1. 用户设置的优先级 (权重最高)
2. 出现在推荐列表的次数
3. 添加时间 (新添加的内容会有加分)
4. 上映时间 (即将上映的内容会加分)
5. 下映时间 (即将下映的内容会大幅加分)
6. AI 分析质量
7. 评分

## 🎨 界面功能

### 首页 (Dashboard)
- **最新想看**: 最近添加的想看内容
- **即将下映**: 14天内将要下映的内容
- **最近上映**: 7天内新上映的内容
- 下拉刷新更新数据

### 列表页 (List)
- 查看所有收藏
- 按状态筛选: 想看/在看/看过/弃剧
- 按类型筛选: 电影/电视剧/小说/书籍
- 按优先级筛选

### 添加页 (Add)
- 输入标题
- 选择类型和优先级
- 添加想看原因
- 粘贴预告片链接
- 输入推荐文案

### 详情页 (Detail)
- 完整信息展示
- AI 分析结果
- 所有推荐来源
- 流媒体平台链接
- 预告片链接

## 🛠️ 故障排除

### 后端无法启动

```bash
# 检查 Python 版本 (需要 3.8+)
python --version

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### iOS 无法连接后端

1. 确保后端正在运行 (`http://localhost:8000`)
2. 检查 APIService.swift 中的 baseURL
3. 如果使用真机，将 localhost 改为电脑的 IP 地址
4. 确保手机和电脑在同一网络

### AI 功能不工作

1. 检查 `.env` 文件中是否配置了 `OPENAI_API_KEY`
2. 验证 API key 是否有效
3. 查看后端日志中的错误信息

## 📚 更多文档

- [架构文档](docs/ARCHITECTURE.md) - 系统架构详解
- [功能清单](docs/FEATURE_CHECKLIST.md) - 需求实现映射
- [API 示例](docs/API_EXAMPLES.md) - 完整的 API 使用示例
- [项目总结](docs/PROJECT_SUMMARY.md) - 项目实现总结

## 💡 提示和技巧

### 批量添加
使用 API 可以批量导入媒体项目:

```python
import requests

movies = [
    {"title": "盗梦空间", "media_type": "movie", "priority": "high"},
    {"title": "三体", "media_type": "novel", "priority": "high"},
    {"title": "权力的游戏", "media_type": "tv_show", "priority": "medium"}
]

for movie in movies:
    requests.post("http://localhost:8000/media", json=movie)
```

### 查看 API 文档
访问 `http://localhost:8000/docs` 查看交互式 API 文档 (Swagger UI)

### 数据库位置
SQLite 数据库文件位于 `backend/zoetrope.db`，可以使用任何 SQLite 工具查看

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 许可证

MIT License

---

**开始使用 Zoetrope，让 AI 帮你管理想看的内容！** 🎬
