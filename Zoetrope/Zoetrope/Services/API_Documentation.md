# Zoetrope API 文档

> 本文档记录项目中使用的所有外部 API 接口

---

## 目录

1. [TMDB API](#1-tmdb-api)
2. [豆瓣 API](#2-豆瓣-api)
3. [AI API](#3-ai-api)
4. [自建后端 API](#4-自建后端-api)

---

## 1. TMDB API

> The Movie Database API - 用于获取电影/电视剧信息

### 基本信息
- **官网**: https://www.themoviedb.org/
- **API 文档**: https://developer.themoviedb.org/docs
- **Base URL**: `https://api.themoviedb.org/3`

### 已使用接口

| 接口 | 方法 | 用途 | 状态 |
|------|------|------|------|
| `/search/movie` | GET | 搜索电影 | 待实现 |
| `/search/tv` | GET | 搜索电视剧 | 待实现 |
| `/movie/{id}` | GET | 获取电影详情 | 待实现 |
| `/tv/{id}` | GET | 获取电视剧详情 | 待实现 |

### 请求示例

```bash
# 搜索电影
curl "https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query=沙丘&language=zh-CN"
```

### 响应示例

```json
{
  "results": [
    {
      "id": 693134,
      "title": "沙丘2",
      "release_date": "2024-02-27",
      "poster_path": "/xxx.jpg"
    }
  ]
}
```

---

## 2. 豆瓣 API

> 用于获取中文媒体信息（备选方案）

### 基本信息
- **官网**: https://www.douban.com/
- **说明**: 豆瓣官方 API 已关闭，需要使用第三方方案

### 替代方案
- [ ] 爬虫方案
- [ ] 第三方 API 服务
- [ ] 手动维护数据库

---

## 3. AI API

> 用于文本分析、摘要生成、情感分析等

### 3.1 OpenAI API

- **官网**: https://openai.com/
- **API 文档**: https://platform.openai.com/docs
- **Base URL**: `https://api.openai.com/v1`

| 接口 | 方法 | 用途 | 状态 |
|------|------|------|------|
| `/chat/completions` | POST | 文本分析/摘要生成 | 待实现 |

### 3.2 Claude API

- **官网**: https://anthropic.com/
- **API 文档**: https://docs.anthropic.com/
- **Base URL**: `https://api.anthropic.com/v1`

| 接口 | 方法 | 用途 | 状态 |
|------|------|------|------|
| `/messages` | POST | 文本分析/摘要生成 | 待实现 |

---

## 4. 自建后端 API

> Zoetrope 后端服务 API

### 基本信息
- **Base URL**: `待定`
- **认证方式**: `待定`

### 接口列表

| 接口 | 方法 | 用途 | 状态 |
|------|------|------|------|
| `/api/media` | GET | 获取媒体列表 | 待实现 |
| `/api/media` | POST | 添加媒体条目 | 待实现 |
| `/api/media/{id}` | GET | 获取媒体详情 | 待实现 |
| `/api/media/{id}` | PUT | 更新媒体信息 | 待实现 |
| `/api/inbox` | POST | 添加到收集箱 | 待实现 |
| `/api/analyze` | POST | AI 分析内容 | 待实现 |

---

## 更新日志

| 日期 | 更新内容 |
|------|----------|
| 2026-01-06 | 创建文档 |

