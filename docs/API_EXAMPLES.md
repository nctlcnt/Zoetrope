# API 使用示例

## 基本 URL
```
http://localhost:8000
```

## 添加新的媒体项目

```bash
curl -X POST "http://localhost:8000/media" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "星际穿越",
    "media_type": "movie",
    "priority": "high",
    "reason_to_watch": "诺兰导演的科幻力作，探讨时间和空间的关系",
    "trailer_url": "https://www.youtube.com/watch?v=zSWdZVtXT7E",
    "recommendation_text": "豆瓣评分9.3，IMDB Top 250"
  }'
```

## 获取仪表盘数据

```bash
curl "http://localhost:8000/dashboard"
```

## Python 示例

```python
import requests

# 添加媒体
response = requests.post(
    "http://localhost:8000/media",
    json={
        "title": "三体",
        "media_type": "novel",
        "priority": "high",
        "reason_to_watch": "科幻巨作"
    }
)

media = response.json()
print(f"创建成功: {media['id']}")
```
