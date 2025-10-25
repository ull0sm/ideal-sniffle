"""Database models for the chatbot."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255))
    google_id = Column(String(255), unique=True, index=True)
    is_first_time = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    """Conversation model."""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    msg_metadata = Column(JSON)  # Store additional data like links, sources
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    bookmarks = relationship("Bookmark", back_populates="message", cascade="all, delete-orphan")


class Bookmark(Base):
    """Bookmark/starred messages model."""
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    note = Column(Text)  # Optional user note
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    message = relationship("Message", back_populates="bookmarks")


class Analytics(Base):
    """Analytics and logging model."""
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String(100), nullable=False)  # 'query', 'login', 'bookmark', etc.
    event_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(50))
    user_agent = Column(Text)


class KnowledgeBase(Base):
    """Knowledge base for embeddings and context."""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    content = Column(Text, nullable=False)
    source = Column(String(500))  # URL or API source
    category = Column(String(100))  # 'placement', 'internship', 'role', etc.
    kb_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
