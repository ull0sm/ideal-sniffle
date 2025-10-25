#!/usr/bin/env python3
"""Simple demo of the chatbot's core components without external APIs."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.database import User, Conversation, Message
from utils.database import init_db, get_db
from datetime import datetime

def demo():
    """Run a simple demo of the chatbot components."""
    
    print("=" * 60)
    print("Boeing India Career Chatbot - Core Demo")
    print("=" * 60)
    print()
    
    # Initialize database
    print("1. Initializing database...")
    init_db()
    print("   ✓ Database initialized with SQLite")
    print()
    
    # Create a demo user
    print("2. Creating demo user...")
    with get_db() as db:
        # Check if user exists
        existing_user = db.query(User).filter(User.email == "demo@example.com").first()
        if existing_user:
            user_id = existing_user.id
            user_name = existing_user.name
            user_email = existing_user.email
            print("   ✓ Using existing demo user")
        else:
            user = User(
                email="demo@example.com",
                name="Demo Student",
                google_id="demo123",
                is_first_time=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            user_id = user.id
            user_name = user.name
            user_email = user.email
            print("   ✓ Created new demo user")
    
    print(f"   User: {user_name} ({user_email})")
    print()
    
    # Create a conversation
    print("3. Creating conversation...")
    with get_db() as db:
        conversation = Conversation(
            user_id=user_id,
            title="Boeing India Placement Questions"
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conv_id = conversation.id
        conv_title = conversation.title
        print(f"   ✓ Conversation created: '{conv_title}'")
    print()
    
    # Add messages
    print("4. Adding messages to conversation...")
    sample_messages = [
        {
            "role": "user",
            "content": "What is the placement process at Boeing India?"
        },
        {
            "role": "assistant",
            "content": "Boeing India conducts campus recruitment at premier engineering institutions. The process typically includes: 1) Online application, 2) Aptitude and technical assessment, 3) Technical interviews (2-3 rounds), 4) HR interview, and 5) Final offer. Eligible branches include Aerospace, Mechanical, Electronics, Computer Science, and related fields. The minimum CGPA requirement is usually 7.0 or above."
        },
        {
            "role": "user",
            "content": "What skills should I develop for a software engineering role at Boeing?"
        },
        {
            "role": "assistant",
            "content": "For software engineering at Boeing India, focus on: 1) Programming languages like C++, Python, and Java, 2) Embedded systems and avionics, 3) Data structures and algorithms, 4) Systems engineering concepts, 5) Version control (Git), 6) Understanding of aerospace software standards (DO-178C), and 7) Strong problem-solving skills. Building projects related to aerospace or embedded systems will also strengthen your profile."
        }
    ]
    
    with get_db() as db:
        for msg_data in sample_messages:
            message = Message(
                conversation_id=conv_id,
                role=msg_data["role"],
                content=msg_data["content"]
            )
            db.add(message)
            db.commit()
            
            role_label = "Student" if msg_data["role"] == "user" else "Chatbot"
            print(f"   ✓ {role_label}: {msg_data['content'][:60]}...")
    print()
    
    # Display conversation
    print("5. Displaying conversation:")
    print("-" * 60)
    with get_db() as db:
        messages = db.query(Message).filter(Message.conversation_id == conv_id).all()
        for msg in messages:
            role = "👤 Student" if msg.role == "user" else "🤖 Chatbot"
            print(f"\n{role}:")
            print(f"  {msg.content}")
    print()
    print("-" * 60)
    print()
    
    # Show statistics
    print("6. Statistics:")
    with get_db() as db:
        total_users = db.query(User).count()
        total_conversations = db.query(Conversation).count()
        total_messages = db.query(Message).count()
        
        print(f"   Total Users: {total_users}")
        print(f"   Total Conversations: {total_conversations}")
        print(f"   Total Messages: {total_messages}")
    print()
    
    print("=" * 60)
    print("Demo completed successfully!")
    print()
    print("The chatbot's database is working correctly.")
    print("To run the full application with AI features:")
    print("  1. Configure .env with API keys")
    print("  2. Run: streamlit run app.py")
    print("=" * 60)

if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
