"""Conversation management utilities."""

from typing import List, Dict, Optional
from datetime import datetime

from models.database import Conversation, Message, User, Bookmark, Analytics
from utils.database import get_db


class ConversationManager:
    """Manage conversations and messages."""
    
    def create_conversation(self, user: User, title: str = "New Conversation") -> Conversation:
        """Create a new conversation for a user."""
        with get_db() as db:
            conversation = Conversation(
                user_id=user.id,
                title=title,
                is_active=True
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            return conversation
    
    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """Get a conversation by ID."""
        with get_db() as db:
            return db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def get_user_conversations(self, user: User, limit: int = 10) -> List[Conversation]:
        """Get recent conversations for a user."""
        with get_db() as db:
            return db.query(Conversation)\
                .filter(Conversation.user_id == user.id)\
                .order_by(Conversation.updated_at.desc())\
                .limit(limit)\
                .all()
    
    def add_message(
        self, 
        conversation_id: int, 
        role: str, 
        content: str,
        metadata: Optional[Dict] = None
    ) -> Message:
        """Add a message to a conversation."""
        with get_db() as db:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                metadata=metadata or {}
            )
            db.add(message)
            
            # Update conversation timestamp
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            return message
    
    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        """Get all messages in a conversation."""
        with get_db() as db:
            return db.query(Message)\
                .filter(Message.conversation_id == conversation_id)\
                .order_by(Message.created_at.asc())\
                .all()
    
    def get_conversation_history(self, conversation_id: int) -> List[Dict[str, str]]:
        """Get conversation history in format for LLM."""
        messages = self.get_conversation_messages(conversation_id)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
    
    def update_conversation_title(self, conversation_id: int, title: str):
        """Update conversation title."""
        with get_db() as db:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if conversation:
                conversation.title = title
                db.commit()
    
    def bookmark_message(self, user: User, message_id: int, note: str = "") -> Bookmark:
        """Bookmark/star a message."""
        with get_db() as db:
            # Check if already bookmarked
            existing = db.query(Bookmark)\
                .filter(Bookmark.user_id == user.id, Bookmark.message_id == message_id)\
                .first()
            
            if existing:
                return existing
            
            bookmark = Bookmark(
                user_id=user.id,
                message_id=message_id,
                note=note
            )
            db.add(bookmark)
            db.commit()
            db.refresh(bookmark)
            return bookmark
    
    def unbookmark_message(self, user: User, message_id: int):
        """Remove bookmark from a message."""
        with get_db() as db:
            bookmark = db.query(Bookmark)\
                .filter(Bookmark.user_id == user.id, Bookmark.message_id == message_id)\
                .first()
            if bookmark:
                db.delete(bookmark)
                db.commit()
    
    def get_user_bookmarks(self, user: User) -> List[Bookmark]:
        """Get all bookmarks for a user."""
        with get_db() as db:
            return db.query(Bookmark)\
                .filter(Bookmark.user_id == user.id)\
                .order_by(Bookmark.created_at.desc())\
                .all()
    
    def is_message_bookmarked(self, user: User, message_id: int) -> bool:
        """Check if a message is bookmarked by user."""
        with get_db() as db:
            bookmark = db.query(Bookmark)\
                .filter(Bookmark.user_id == user.id, Bookmark.message_id == message_id)\
                .first()
            return bookmark is not None
    
    def log_query(self, user: User, query: str, response: str):
        """Log a query for analytics."""
        with get_db() as db:
            analytics = Analytics(
                user_id=user.id,
                event_type='query',
                event_data={
                    'query': query,
                    'response_length': len(response),
                    'timestamp': datetime.utcnow().isoformat()
                }
            )
            db.add(analytics)
            db.commit()


conversation_manager = ConversationManager()
