"""AI service for content analysis and summarization"""

import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class AIService:
    """Service for AI-powered content analysis"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        if not self.client:
            print("Warning: OPENAI_API_KEY not set, AI features will be disabled")
    
    def analyze_media_appeal(
        self,
        title: str,
        media_type: str,
        reason_to_watch: Optional[str] = None,
        recommendation_text: Optional[str] = None,
        recommendations: Optional[list] = None
    ) -> dict:
        """
        Analyze media content and generate:
        - AI summary of appeal points
        - Viewing motivation
        """
        if not self.client:
            return {
                "ai_summary": None,
                "ai_motivation": None
            }
        
        # Build context from available information
        context_parts = [f"Media: {title} ({media_type})"]
        
        if reason_to_watch:
            context_parts.append(f"User's reason to watch: {reason_to_watch}")
        
        if recommendation_text:
            context_parts.append(f"Recommendation: {recommendation_text}")
        
        if recommendations:
            for rec in recommendations:
                if rec.recommendation_reason:
                    context_parts.append(f"Review from {rec.source_name}: {rec.recommendation_reason}")
        
        context = "\n".join(context_parts)
        
        prompt = f"""Based on the following information about a media item, provide:
1. A concise summary of the main appeal points (2-3 sentences)
2. The primary viewing motivation (1 sentence)

Information:
{context}

Please respond in JSON format:
{{
    "appeal_summary": "...",
    "viewing_motivation": "..."
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a media analyst who helps people understand why they want to watch movies, TV shows, and books."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Parse response
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "ai_summary": result.get("appeal_summary"),
                "ai_motivation": result.get("viewing_motivation")
            }
        except Exception as e:
            print(f"AI analysis error: {e}")
            return {
                "ai_summary": None,
                "ai_motivation": None
            }
    
    def aggregate_recommendations(self, recommendations: list) -> Optional[str]:
        """Aggregate multiple recommendations into a summary"""
        if not self.client or not recommendations:
            return None
        
        rec_texts = []
        for rec in recommendations:
            if rec.recommendation_reason:
                rec_texts.append(f"{rec.source_name}: {rec.recommendation_reason}")
        
        if not rec_texts:
            return None
        
        prompt = f"""Summarize the following recommendations into a cohesive overview (2-3 sentences):

{chr(10).join(rec_texts)}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a media analyst who summarizes recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Recommendation aggregation error: {e}")
            return None
