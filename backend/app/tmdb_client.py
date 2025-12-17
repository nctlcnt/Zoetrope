"""TMDB API integration for fetching movie/TV data"""

import os
import requests
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class TMDBClient:
    """Client for TMDB API"""
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        if not self.api_key:
            print("Warning: TMDB_API_KEY not set in environment")
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        """Make a request to TMDB API"""
        if not self.api_key:
            return None
        
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"TMDB API error: {e}")
            return None
    
    def search_movie(self, title: str) -> Optional[Dict]:
        """Search for a movie by title"""
        data = self._make_request("/search/movie", {"query": title})
        if data and data.get("results"):
            return data["results"][0]
        return None
    
    def search_tv(self, title: str) -> Optional[Dict]:
        """Search for a TV show by title"""
        data = self._make_request("/search/tv", {"query": title})
        if data and data.get("results"):
            return data["results"][0]
        return None
    
    def get_movie_details(self, movie_id: int) -> Optional[Dict]:
        """Get detailed movie information"""
        return self._make_request(f"/movie/{movie_id}")
    
    def get_tv_details(self, tv_id: int) -> Optional[Dict]:
        """Get detailed TV show information"""
        return self._make_request(f"/tv/{tv_id}")
    
    def enrich_media_data(self, title: str, media_type: str) -> Dict[str, Any]:
        """Enrich media data from TMDB"""
        result = {}
        
        if media_type == "movie":
            movie = self.search_movie(title)
            if movie:
                result["tmdb_id"] = str(movie.get("id"))
                result["poster_url"] = f"{self.IMAGE_BASE_URL}{movie.get('poster_path')}" if movie.get('poster_path') else None
                result["rating"] = movie.get("vote_average")
                
                # Parse release date
                release_date_str = movie.get("release_date")
                if release_date_str:
                    try:
                        result["release_date"] = datetime.strptime(release_date_str, "%Y-%m-%d")
                    except ValueError:
                        pass
        
        elif media_type == "tv_show":
            tv = self.search_tv(title)
            if tv:
                result["tmdb_id"] = str(tv.get("id"))
                result["poster_url"] = f"{self.IMAGE_BASE_URL}{tv.get('poster_path')}" if tv.get('poster_path') else None
                result["rating"] = tv.get("vote_average")
                
                # Parse first air date
                first_air_date_str = tv.get("first_air_date")
                if first_air_date_str:
                    try:
                        result["release_date"] = datetime.strptime(first_air_date_str, "%Y-%m-%d")
                    except ValueError:
                        pass
        
        return result
