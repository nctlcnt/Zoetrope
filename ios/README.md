# Zoetrope iOS App

智能影视追踪系统 - iOS 客户端

## 功能

- 📱 浏览轮播推荐（最新想看、即将下映、最近上映）
- ➕ 添加想看的电影/电视剧/书籍
- 📝 记录想看原因和推荐文案
- 🤖 查看 AI 生成的吸引点分析
- 🔗 快速跳转到流媒体平台

## 技术栈

- SwiftUI
- Async/Await
- MVVM 架构

## 配置

在 `Services/APIService.swift` 中更新后端地址：

```swift
private let baseURL = "http://your-backend-url:8000"
```

## 运行

1. 使用 Xcode 打开项目
2. 选择模拟器或真机
3. 点击运行

## 系统要求

- iOS 16.0+
- Xcode 15.0+
- Swift 5.9+

## 界面说明

### 首页 (DashboardView)
- 三个横向滚动轮播
- Netflix 风格卡片展示
- 下拉刷新

### 列表 (MediaListView)
- 所有收藏的媒体列表
- 按状态筛选
- 点击查看详情

### 添加 (AddMediaView)
- 输入标题和类型
- 设置优先级
- 添加想看原因和推荐文案

### 详情 (MediaDetailView)
- 完整信息展示
- AI 分析结果
- 推荐来源汇总
- 流媒体平台链接
