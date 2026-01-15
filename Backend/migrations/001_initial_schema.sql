-- Zoetrope 数据库迁移脚本
-- 在 Supabase SQL Editor 中运行此脚本创建所需的表

-- ========================================
-- 媒体类型枚举
-- ========================================
DO $$ BEGIN
    CREATE TYPE media_type AS ENUM ('movie', 'tv', 'novel', 'book', 'music');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ========================================
-- 媒体条目表
-- ========================================
CREATE TABLE IF NOT EXISTS media_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    type media_type NOT NULL DEFAULT 'movie',

    -- 外部数据源 ID
    tmdb_id INTEGER UNIQUE,
    imdb_id VARCHAR(20) UNIQUE,

    -- 时间信息
    release_date TIMESTAMP,
    end_date TIMESTAMP,

    -- 媒体信息
    poster_url VARCHAR(500),
    overview TEXT,

    -- 评分相关
    user_score FLOAT,
    priority_score FLOAT DEFAULT 0.0,
    sentiment_score FLOAT,

    -- 统计数据
    mention_count INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,

    -- 状态标记
    is_watched INTEGER DEFAULT 0,  -- 0: 未看, 1: 已看, 2: 在看
    is_hidden INTEGER DEFAULT 0,

    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_media_items_title ON media_items(title);
CREATE INDEX IF NOT EXISTS idx_media_items_tmdb_id ON media_items(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_media_items_priority ON media_items(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_media_items_created ON media_items(created_at DESC);

-- ========================================
-- 评论来源枚举
-- ========================================
DO $$ BEGIN
    CREATE TYPE comment_source AS ENUM ('user', 'ai', 'imported');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ========================================
-- 评论表
-- ========================================
CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    media_id INTEGER NOT NULL REFERENCES media_items(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    source comment_source NOT NULL DEFAULT 'user',
    sentiment_score FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_comments_media_id ON comments(media_id);
CREATE INDEX IF NOT EXISTS idx_comments_created ON comments(created_at DESC);

-- ========================================
-- 收集箱表
-- ========================================
CREATE TABLE IF NOT EXISTS inbox (
    id SERIAL PRIMARY KEY,
    raw_content TEXT NOT NULL,
    url VARCHAR(2048),
    processed BOOLEAN DEFAULT FALSE,
    processing_error TEXT,
    extracted_titles TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '7 days')
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_inbox_processed ON inbox(processed);
CREATE INDEX IF NOT EXISTS idx_inbox_expires ON inbox(expires_at);

-- ========================================
-- 更新时间戳触发器
-- ========================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为 media_items 添加更新触发器
DROP TRIGGER IF EXISTS update_media_items_updated_at ON media_items;
CREATE TRIGGER update_media_items_updated_at
    BEFORE UPDATE ON media_items
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- RLS 策略 (可选，根据需求启用)
-- ========================================
-- 如果需要启用 Row Level Security:
-- ALTER TABLE media_items ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE comments ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE inbox ENABLE ROW LEVEL SECURITY;

-- 允许所有操作的策略（开发阶段使用）:
-- CREATE POLICY "Allow all for media_items" ON media_items FOR ALL USING (true);
-- CREATE POLICY "Allow all for comments" ON comments FOR ALL USING (true);
-- CREATE POLICY "Allow all for inbox" ON inbox FOR ALL USING (true);

-- ========================================
-- 清理过期收集箱条目的函数
-- ========================================
CREATE OR REPLACE FUNCTION cleanup_expired_inbox()
RETURNS void AS $$
BEGIN
    DELETE FROM inbox WHERE expires_at < NOW();
END;
$$ LANGUAGE plpgsql;

-- 可以通过 Supabase 的 pg_cron 扩展定期调用此函数
-- SELECT cron.schedule('cleanup-inbox', '0 0 * * *', 'SELECT cleanup_expired_inbox()');
