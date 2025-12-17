"""FastAPI application and routes"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from .database import get_db, init_db
from .models import MediaItem, Recommendation, StreamingLink, MediaStatus, PriorityLevel, MediaType
from .schemas import (
    MediaItemCreate,
    MediaItemUpdate,
    MediaItemResponse,
    RecommendationBase,
    StreamingLinkBase,
    DashboardResponse,
    CarouselResponse
)
from .tmdb_client import TMDBClient
from .ai_service import AIService
from .priority_ranker import PriorityRanker

app = FastAPI(
    title="Zoetrope API",
    description="Smart media tracking and recommendation system",
    version="0.1.0"
)

# CORS middleware for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify iOS app origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
tmdb_client = TMDBClient()
ai_service = AIService()
priority_ranker = PriorityRanker()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Zoetrope API", "version": "0.1.0"}


@app.post("/media", response_model=MediaItemResponse, status_code=status.HTTP_201_CREATED)
async def create_media_item(
    media: MediaItemCreate,
    db: Session = Depends(get_db)
):
    """Create a new media item"""
    
    # Create media item
    db_media = MediaItem(
        title=media.title,
        media_type=MediaType[media.media_type.upper()],
        priority=PriorityLevel[media.priority.upper()],
        reason_to_watch=media.reason_to_watch,
        trailer_url=media.trailer_url,
        recommendation_text=media.recommendation_text
    )
    
    # Enrich with TMDB data
    if media.media_type in ["movie", "tv_show"]:
        tmdb_data = tmdb_client.enrich_media_data(media.title, media.media_type)
        for key, value in tmdb_data.items():
            setattr(db_media, key, value)
    
    # Generate AI analysis
    ai_result = ai_service.analyze_media_appeal(
        title=media.title,
        media_type=media.media_type,
        reason_to_watch=media.reason_to_watch,
        recommendation_text=media.recommendation_text
    )
    db_media.ai_summary = ai_result.get("ai_summary")
    db_media.ai_motivation = ai_result.get("ai_motivation")
    
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    
    return db_media


@app.get("/media", response_model=List[MediaItemResponse])
async def list_media_items(
    status: str = None,
    media_type: str = None,
    priority: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List media items with optional filters"""
    
    query = db.query(MediaItem)
    
    if status:
        query = query.filter(MediaItem.status == MediaStatus[status.upper()])
    if media_type:
        query = query.filter(MediaItem.media_type == MediaType[media_type.upper()])
    if priority:
        query = query.filter(MediaItem.priority == PriorityLevel[priority.upper()])
    
    items = query.offset(skip).limit(limit).all()
    
    # Rank items by priority
    ranked_items = priority_ranker.rank_items(items)
    
    return ranked_items


@app.get("/media/{media_id}", response_model=MediaItemResponse)
async def get_media_item(media_id: int, db: Session = Depends(get_db)):
    """Get a specific media item"""
    
    media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    return media


@app.patch("/media/{media_id}", response_model=MediaItemResponse)
async def update_media_item(
    media_id: int,
    media_update: MediaItemUpdate,
    db: Session = Depends(get_db)
):
    """Update a media item"""
    
    media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    # Update fields
    update_data = media_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value:
            setattr(media, field, MediaStatus[value.upper()])
        elif field == "priority" and value:
            setattr(media, field, PriorityLevel[value.upper()])
        else:
            setattr(media, field, value)
    
    db.commit()
    db.refresh(media)
    
    return media


@app.delete("/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media_item(media_id: int, db: Session = Depends(get_db)):
    """Delete a media item"""
    
    media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    db.delete(media)
    db.commit()
    
    return None


@app.post("/media/{media_id}/recommendations", status_code=status.HTTP_201_CREATED)
async def add_recommendation(
    media_id: int,
    recommendation: RecommendationBase,
    db: Session = Depends(get_db)
):
    """Add a recommendation to a media item"""
    
    media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    db_recommendation = Recommendation(
        media_item_id=media_id,
        source_name=recommendation.source_name,
        source_url=recommendation.source_url,
        recommendation_reason=recommendation.recommendation_reason,
        rating=recommendation.rating,
        review_date=datetime.utcnow()
    )
    
    # Update appearance count
    media.appearance_count += 1
    
    # Auto-adjust priority based on appearance count
    new_priority = priority_ranker.auto_adjust_priority(media)
    media.priority = PriorityLevel[new_priority.upper()]
    
    db.add(db_recommendation)
    db.commit()
    
    return {"message": "Recommendation added successfully"}


@app.post("/media/{media_id}/streaming-links", status_code=status.HTTP_201_CREATED)
async def add_streaming_link(
    media_id: int,
    link: StreamingLinkBase,
    db: Session = Depends(get_db)
):
    """Add a streaming platform link"""
    
    media = db.query(MediaItem).filter(MediaItem.id == media_id).first()
    if not media:
        raise HTTPException(status_code=404, detail="Media item not found")
    
    db_link = StreamingLink(
        media_item_id=media_id,
        platform=link.platform,
        url=link.url,
        available=link.available
    )
    
    db.add(db_link)
    db.commit()
    
    return {"message": "Streaming link added successfully"}


@app.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(db: Session = Depends(get_db)):
    """
    Get dashboard with carousels:
    - Latest wants (recently added)
    - Ending soon (items with end_date in next 14 days)
    - Recently released (items released in last 7 days)
    """
    
    now = datetime.utcnow()
    
    # Latest wants - recently added items
    latest_query = db.query(MediaItem).filter(
        MediaItem.status == MediaStatus.WANT_TO_WATCH
    ).order_by(MediaItem.created_at.desc()).limit(10).all()
    latest_wants = priority_ranker.rank_items(latest_query)
    
    # Ending soon - items ending in next 14 days
    end_threshold = now + timedelta(days=14)
    ending_query = db.query(MediaItem).filter(
        MediaItem.end_date.isnot(None),
        MediaItem.end_date >= now,
        MediaItem.end_date <= end_threshold,
        MediaItem.status == MediaStatus.WANT_TO_WATCH
    ).all()
    ending_soon = priority_ranker.rank_items(ending_query)
    
    # Recently released - items released in last 7 days
    release_threshold = now - timedelta(days=7)
    released_query = db.query(MediaItem).filter(
        MediaItem.release_date.isnot(None),
        MediaItem.release_date >= release_threshold,
        MediaItem.release_date <= now,
        MediaItem.status == MediaStatus.WANT_TO_WATCH
    ).all()
    recently_released = priority_ranker.rank_items(released_query)
    
    return {
        "latest_wants": {
            "title": "最新想看",
            "items": latest_wants
        },
        "ending_soon": {
            "title": "即将下映",
            "items": ending_soon
        },
        "recently_released": {
            "title": "最近上映",
            "items": recently_released
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
