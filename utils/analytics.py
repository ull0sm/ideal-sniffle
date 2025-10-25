"""Analytics utilities for admin dashboard."""

from typing import List, Dict
from datetime import datetime, timedelta
from sqlalchemy import func

from models.database import Analytics, User, Message, Conversation
from utils.database import get_db


class AnalyticsManager:
    """Manage analytics and reporting."""
    
    def get_total_users(self) -> int:
        """Get total number of users."""
        with get_db() as db:
            return db.query(User).count()
    
    def get_total_conversations(self) -> int:
        """Get total number of conversations."""
        with get_db() as db:
            return db.query(Conversation).count()
    
    def get_total_messages(self) -> int:
        """Get total number of messages."""
        with get_db() as db:
            return db.query(Message).count()
    
    def get_recent_activity(self, days: int = 7) -> List[Dict]:
        """Get recent user activity."""
        with get_db() as db:
            since = datetime.utcnow() - timedelta(days=days)
            
            analytics = db.query(Analytics)\
                .filter(Analytics.created_at >= since)\
                .order_by(Analytics.created_at.desc())\
                .limit(100)\
                .all()
            
            return [
                {
                    'user_id': a.user_id,
                    'event_type': a.event_type,
                    'event_data': a.event_data,
                    'created_at': a.created_at
                }
                for a in analytics
            ]
    
    def get_popular_queries(self, limit: int = 10) -> List[Dict]:
        """Get most common query patterns."""
        with get_db() as db:
            analytics = db.query(Analytics)\
                .filter(Analytics.event_type == 'query')\
                .order_by(Analytics.created_at.desc())\
                .limit(100)\
                .all()
            
            # Extract queries
            queries = []
            for a in analytics:
                if a.event_data and 'query' in a.event_data:
                    queries.append({
                        'query': a.event_data['query'],
                        'timestamp': a.created_at
                    })
            
            return queries[:limit]
    
    def get_user_stats(self) -> Dict:
        """Get user statistics."""
        with get_db() as db:
            total_users = db.query(User).count()
            first_time_users = db.query(User).filter(User.is_first_time == True).count()
            
            # Active users (logged in last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            active_users = db.query(User).filter(User.last_login >= week_ago).count()
            
            return {
                'total': total_users,
                'first_time': first_time_users,
                'returning': total_users - first_time_users,
                'active_last_7_days': active_users
            }
    
    def get_daily_queries(self, days: int = 7) -> List[Dict]:
        """Get daily query counts."""
        with get_db() as db:
            since = datetime.utcnow() - timedelta(days=days)
            
            results = db.query(
                func.date(Analytics.created_at).label('date'),
                func.count(Analytics.id).label('count')
            ).filter(
                Analytics.event_type == 'query',
                Analytics.created_at >= since
            ).group_by(
                func.date(Analytics.created_at)
            ).all()
            
            return [
                {'date': str(r.date), 'count': r.count}
                for r in results
            ]


analytics_manager = AnalyticsManager()
