"""Authentication utilities for Google OAuth."""

import streamlit as st
from google.oauth2 import id_token
from google.auth.transport import requests
from typing import Optional, Dict
import time

from config.settings import settings
from models.database import User
from utils.database import get_db


class AuthManager:
    """Manage authentication and user sessions."""
    
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        
    def verify_google_token(self, token: str) -> Optional[Dict]:
        """Verify Google OAuth token and return user info."""
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.client_id
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
                
            return {
                'google_id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo.get('name', ''),
            }
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return None
    
    def get_or_create_user(self, user_info: Dict) -> User:
        """Get existing user or create new one."""
        with get_db() as db:
            user = db.query(User).filter(User.email == user_info['email']).first()
            
            if not user:
                user = User(
                    email=user_info['email'],
                    name=user_info['name'],
                    google_id=user_info['google_id'],
                    is_first_time=True
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            else:
                # Update last login
                from datetime import datetime
                user.last_login = datetime.utcnow()
                db.commit()
                db.refresh(user)
            
            return user
    
    def is_admin(self, email: str) -> bool:
        """Check if user is an admin."""
        return email in settings.ADMIN_EMAILS
    
    def init_session_state(self):
        """Initialize session state variables."""
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'conversation_id' not in st.session_state:
            st.session_state.conversation_id = None
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    def login(self, user_info: Dict):
        """Log in user."""
        user = self.get_or_create_user(user_info)
        st.session_state.user = user
        st.session_state.authenticated = True
        
        # Log analytics
        self._log_login(user)
    
    def logout(self):
        """Log out user."""
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.conversation_id = None
        st.session_state.messages = []
    
    def _log_login(self, user: User):
        """Log login event to analytics."""
        from models.database import Analytics
        
        with get_db() as db:
            analytics = Analytics(
                user_id=user.id,
                event_type='login',
                event_data={'timestamp': time.time()}
            )
            db.add(analytics)
            db.commit()


auth_manager = AuthManager()
