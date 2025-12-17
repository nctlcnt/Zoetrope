# Zoetrope Backend

智能影视追踪系统 - 后端服务

## 安装

```bash
pip install -r requirements.txt
```

## 配置

复制 `.env.example` 到 `.env` 并填入配置：

```bash
cp .env.example .env
```

需要的 API Keys:
- `OPENAI_API_KEY`: OpenAI API key
- `TMDB_API_KEY`: TMDB API key (https://www.themoviedb.org/settings/api)

## 运行

```bash
python run.py
```

服务将在 http://localhost:8000 启动

## API 文档

访问 http://localhost:8000/docs 查看自动生成的 API 文档

## 测试

```bash
pytest
```

## 数据库

使用 SQLite 作为默认数据库，数据文件：`zoetrope.db`

## 主要功能

1. **媒体管理**: CRUD 操作
2. **TMDB 集成**: 自动获取电影/电视剧信息
3. **AI 分析**: 使用 OpenAI 分析内容吸引力
4. **优先级排序**: 基于多个因素的智能排序
5. **轮播数据**: 为首页提供分类数据
