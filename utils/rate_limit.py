"""Rate limiting utilities."""

import time
from typing import Dict
import streamlit as st

from config.settings import settings


class RateLimiter:
    """Simple rate limiter for user queries."""
    
    def __init__(self):
        """Initialize rate limiter."""
        if 'rate_limit_data' not in st.session_state:
            st.session_state.rate_limit_data = {}
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user has exceeded rate limit.
        
        Returns:
            True if user is within rate limit, False if exceeded
        """
        current_time = time.time()
        user_key = str(user_id)
        
        if user_key not in st.session_state.rate_limit_data:
            st.session_state.rate_limit_data[user_key] = {
                'minute': [],
                'hour': []
            }
        
        user_data = st.session_state.rate_limit_data[user_key]
        
        # Clean old timestamps
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        
        user_data['minute'] = [t for t in user_data['minute'] if t > minute_ago]
        user_data['hour'] = [t for t in user_data['hour'] if t > hour_ago]
        
        # Check limits
        if len(user_data['minute']) >= settings.RATE_LIMIT_PER_MINUTE:
            return False
        
        if len(user_data['hour']) >= settings.RATE_LIMIT_PER_HOUR:
            return False
        
        # Add current timestamp
        user_data['minute'].append(current_time)
        user_data['hour'].append(current_time)
        
        return True
    
    def get_remaining_queries(self, user_id: int) -> Dict[str, int]:
        """Get remaining queries for user."""
        user_key = str(user_id)
        
        if user_key not in st.session_state.rate_limit_data:
            return {
                'per_minute': settings.RATE_LIMIT_PER_MINUTE,
                'per_hour': settings.RATE_LIMIT_PER_HOUR
            }
        
        user_data = st.session_state.rate_limit_data[user_key]
        
        return {
            'per_minute': settings.RATE_LIMIT_PER_MINUTE - len(user_data['minute']),
            'per_hour': settings.RATE_LIMIT_PER_HOUR - len(user_data['hour'])
        }


rate_limiter = RateLimiter()
