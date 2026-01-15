# TMDB API 响应模型
# 参考 https://developer.themoviedb.org/reference/intro/getting-started

from typing import Optional
from pydantic import BaseModel, Field, computed_field


class TMDBGenre(BaseModel):
    """TMDB 类型"""
    id: int
    name: str


class TMDBMediaItem(BaseModel):
    """TMDB 搜索结果中的媒体项"""
    id: int = Field(..., description="TMDB ID")
    title: Optional[str] = Field(None, description="电影标题")
    name: Optional[str] = Field(None, description="电视剧标题")
    original_title: Optional[str] = Field(None, description="电影原始标题")
    original_name: Optional[str] = Field(None, description="电视剧原始标题")
    overview: Optional[str] = Field(None, description="简介")
    poster_path: Optional[str] = Field(None, description="海报路径")
    backdrop_path: Optional[str] = Field(None, description="背景图路径")
    release_date: Optional[str] = Field(None, description="电影上映日期")
    first_air_date: Optional[str] = Field(None, description="电视剧首播日期")
    vote_average: Optional[float] = Field(None, description="平均评分")
    vote_count: Optional[int] = Field(None, description="评分人数")
    popularity: Optional[float] = Field(None, description="热度")
    genre_ids: list[int] = Field(default_factory=list, description="类型ID列表")
    media_type: Optional[str] = Field(None, description="媒体类型 (movie/tv)")

    @computed_field
    @property
    def display_title(self) -> str:
        """获取显示标题，优先使用电影标题"""
        return self.title or self.name or "未知标题"

    @computed_field
    @property
    def display_date(self) -> Optional[str]:
        """获取显示日期，优先使用电影日期"""
        return self.release_date or self.first_air_date

    @computed_field
    @property
    def full_poster_url(self) -> Optional[str]:
        """获取完整海报URL"""
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    @computed_field
    @property
    def full_backdrop_url(self) -> Optional[str]:
        """获取完整背景图URL"""
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None


class TMDBSearchResponse(BaseModel):
    """TMDB 搜索响应"""
    page: int = Field(..., description="当前页码")
    results: list[TMDBMediaItem] = Field(default_factory=list, description="搜索结果")
    total_pages: int = Field(..., description="总页数")
    total_results: int = Field(..., description="总结果数")


class TMDBCastMember(BaseModel):
    """TMDB 演员信息"""
    id: int
    name: str
    character: Optional[str] = None
    profile_path: Optional[str] = None
    order: Optional[int] = None

    @computed_field
    @property
    def full_profile_url(self) -> Optional[str]:
        """获取完整头像URL"""
        if self.profile_path:
            return f"https://image.tmdb.org/t/p/w185{self.profile_path}"
        return None


class TMDBCrewMember(BaseModel):
    """TMDB 剧组成员信息"""
    id: int
    name: str
    job: Optional[str] = None
    department: Optional[str] = None
    profile_path: Optional[str] = None


class TMDBCredits(BaseModel):
    """TMDB 演职员表"""
    id: int
    cast: list[TMDBCastMember] = Field(default_factory=list)
    crew: list[TMDBCrewMember] = Field(default_factory=list)


class TMDBMovieDetails(BaseModel):
    """TMDB 电影详情"""
    id: int
    title: str
    original_title: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    release_date: Optional[str] = None
    runtime: Optional[int] = Field(None, description="时长(分钟)")
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    genres: list[TMDBGenre] = Field(default_factory=list)
    status: Optional[str] = Field(None, description="状态: Released, Post Production, etc.")
    tagline: Optional[str] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    imdb_id: Optional[str] = None

    # 可选的附加信息（需要 append_to_response）
    credits: Optional[TMDBCredits] = None

    @computed_field
    @property
    def full_poster_url(self) -> Optional[str]:
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None


class TMDBTVDetails(BaseModel):
    """TMDB 电视剧详情"""
    id: int
    name: str
    original_name: Optional[str] = None
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    first_air_date: Optional[str] = None
    last_air_date: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None
    genres: list[TMDBGenre] = Field(default_factory=list)
    status: Optional[str] = Field(None, description="状态: Returning Series, Ended, etc.")
    tagline: Optional[str] = None
    number_of_seasons: Optional[int] = None
    number_of_episodes: Optional[int] = None
    episode_run_time: list[int] = Field(default_factory=list, description="单集时长")
    in_production: Optional[bool] = None

    # 可选的附加信息
    credits: Optional[TMDBCredits] = None

    @computed_field
    @property
    def full_poster_url(self) -> Optional[str]:
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None


class TMDBReleaseDateResult(BaseModel):
    """TMDB 上映日期信息（用于获取中国地区上映日期）"""
    iso_3166_1: str = Field(..., description="国家/地区代码")
    release_dates: list[dict] = Field(default_factory=list)


class TMDBReleaseDatesResponse(BaseModel):
    """TMDB 上映日期响应"""
    id: int
    results: list[TMDBReleaseDateResult] = Field(default_factory=list)
