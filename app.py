"""Main Streamlit application for Boeing India Career Chatbot."""

import streamlit as st
from streamlit_oauth import OAuth2Component
from httpx_oauth.oauth2 import BaseOAuth2
import os
import time

# Import utilities
from config.settings import settings
from utils.database import init_db
from utils.auth import auth_manager
from utils.llm import chatbot
from utils.knowledge import retriever
from utils.conversation import conversation_manager
from utils.rate_limit import rate_limiter
from utils.analytics import analytics_manager


# Page configuration
st.set_page_config(
    page_title="Boeing India Career Chatbot",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0033A0;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E3F2FD;
    }
    .assistant-message {
        background-color: #F5F5F5;
    }
    .sidebar-info {
        padding: 1rem;
        background-color: #E8F4F8;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .bookmark-button {
        float: right;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


def initialize_app():
    """Initialize the application."""
    # Initialize database
    init_db()
    
    # Initialize session state
    auth_manager.init_session_state()
    
    # Initialize knowledge base (first time only)
    if 'kb_initialized' not in st.session_state:
        try:
            retriever.initialize_knowledge_base()
            st.session_state.kb_initialized = True
        except Exception as e:
            st.warning(f"Knowledge base initialization: {str(e)}")


def render_login_page():
    """Render the login page with Google OAuth."""
    st.markdown('<div class="main-header">✈️ Boeing India Career Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Your AI-powered guide to Boeing India careers, placements, and internships</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("👋 **Welcome, Engineering Students!**\n\nThis chatbot helps you explore:\n- Boeing India company insights\n- Placement processes\n- Internship opportunities\n- Job roles and career paths\n- Resume and interview tips\n- Skill-building recommendations")
        
        st.markdown("---")
        
        # OAuth configuration
        if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
            # Create OAuth2 client with explicit revocation endpoint auth method
            token_endpoint = "https://oauth2.googleapis.com/token"
            revoke_endpoint = "https://oauth2.googleapis.com/revoke"
            
            client = BaseOAuth2(
                settings.GOOGLE_CLIENT_ID,
                settings.GOOGLE_CLIENT_SECRET,
                "https://accounts.google.com/o/oauth2/v2/auth",
                token_endpoint,
                revoke_token_endpoint=revoke_endpoint,
                revocation_endpoint_auth_method="client_secret_post",
            )
            
            oauth2 = OAuth2Component(
                settings.GOOGLE_CLIENT_ID,
                settings.GOOGLE_CLIENT_SECRET,
                "https://accounts.google.com/o/oauth2/v2/auth",
                client=client,
            )
            
            result = oauth2.authorize_button(
                "Login with Google",
                settings.OAUTH_REDIRECT_URI,
                "email profile"
            )
            
            if result and 'token' in result:
                user_info = auth_manager.verify_google_token(result['token']['id_token'])
                if user_info:
                    auth_manager.login(user_info)
                    st.rerun()
        else:
            st.warning("⚠️ Google OAuth not configured. Using demo mode.")
            if st.button("Continue in Demo Mode", type="primary"):
                # Demo user for testing
                demo_user_info = {
                    'email': 'demo@example.com',
                    'name': 'Demo User',
                    'google_id': 'demo123'
                }
                auth_manager.login(demo_user_info)
                st.rerun()


def render_sidebar():
    """Render the sidebar with navigation and user info."""
    with st.sidebar:
        st.markdown("### 👤 User Profile")
        
        user = st.session_state.user
        st.write(f"**Name:** {user.name}")
        st.write(f"**Email:** {user.email}")
        
        if user.is_first_time:
            st.success("🎉 Welcome! This is your first visit!")
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 📚 Navigation")
        page = st.radio(
            "Select Page",
            ["💬 Chat", "⭐ Bookmarks", "📊 Admin Dashboard"] if auth_manager.is_admin(user.email) else ["💬 Chat", "⭐ Bookmarks"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Conversation history
        st.markdown("### 📝 Recent Conversations")
        conversations = conversation_manager.get_user_conversations(user, limit=5)
        
        for conv in conversations:
            if st.button(f"📄 {conv.title[:30]}...", key=f"conv_{conv.id}"):
                st.session_state.conversation_id = conv.id
                st.session_state.messages = conversation_manager.get_conversation_history(conv.id)
                st.rerun()
        
        if st.button("➕ New Conversation"):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("---")
        
        # Rate limit info
        remaining = rate_limiter.get_remaining_queries(user.id)
        st.markdown("### ⏱️ Query Limits")
        st.write(f"Per minute: {remaining['per_minute']}/{settings.RATE_LIMIT_PER_MINUTE}")
        st.write(f"Per hour: {remaining['per_hour']}/{settings.RATE_LIMIT_PER_HOUR}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            auth_manager.logout()
            st.rerun()
        
        return page


def render_chat_page():
    """Render the main chat interface."""
    st.markdown('<div class="main-header">💬 Boeing India Career Chat</div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    # Welcome message for first-time users
    if user.is_first_time:
        st.info("👋 Welcome to Boeing India Career Chatbot! I'm here to help you with placements, internships, job roles, and career guidance. Feel free to ask me anything!")
        
        # Update first-time status
        from utils.database import get_db
        with get_db() as db:
            db_user = db.query(type(user)).filter_by(id=user.id).first()
            if db_user:
                db_user.is_first_time = False
                db.commit()
                user.is_first_time = False
    
    # Create conversation if needed
    if st.session_state.conversation_id is None:
        conversation = conversation_manager.create_conversation(user)
        st.session_state.conversation_id = conversation.id
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        role = message['role']
        content = message['content']
        
        message_class = "user-message" if role == "user" else "assistant-message"
        icon = "👤" if role == "user" else "🤖"
        
        with st.container():
            col1, col2 = st.columns([0.95, 0.05])
            
            with col1:
                st.markdown(f'<div class="chat-message {message_class}">{icon} {content}</div>', unsafe_allow_html=True)
            
            with col2:
                # Bookmark button for assistant messages
                if role == "assistant":
                    # Get message from DB to bookmark
                    messages = conversation_manager.get_conversation_messages(st.session_state.conversation_id)
                    if idx < len(messages):
                        msg_id = messages[idx].id
                        is_bookmarked = conversation_manager.is_message_bookmarked(user, msg_id)
                        
                        if st.button("⭐" if is_bookmarked else "☆", key=f"bookmark_{idx}"):
                            if is_bookmarked:
                                conversation_manager.unbookmark_message(user, msg_id)
                            else:
                                conversation_manager.bookmark_message(user, msg_id)
                            st.rerun()
    
    # Chat input
    if prompt := st.chat_input("Ask me about Boeing India careers..."):
        # Check rate limit
        if not rate_limiter.check_rate_limit(user.id):
            st.error("⚠️ Rate limit exceeded. Please wait a moment before sending another message.")
            return
        
        # Add user message to session
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Save user message to DB
        conversation_manager.add_message(
            st.session_state.conversation_id,
            "user",
            prompt
        )
        
        # Update conversation title if this is the first message
        if len(st.session_state.messages) == 1:
            title = chatbot.generate_conversation_title(prompt)
            conversation_manager.update_conversation_title(st.session_state.conversation_id, title)
        
        # Get relevant context from knowledge base
        context = retriever.retrieve_context(prompt)
        
        # Generate response
        with st.spinner("Thinking..."):
            response = chatbot.generate_response(
                prompt,
                st.session_state.messages[:-1],  # Exclude current message
                context
            )
        
        # Add assistant message to session
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save assistant message to DB
        conversation_manager.add_message(
            st.session_state.conversation_id,
            "assistant",
            response,
            msg_metadata={"context_used": bool(context)}
        )
        
        # Log query
        conversation_manager.log_query(user, prompt, response)
        
        st.rerun()


def render_bookmarks_page():
    """Render the bookmarks page."""
    st.markdown('<div class="main-header">⭐ Your Bookmarked Messages</div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    bookmarks = conversation_manager.get_user_bookmarks(user)
    
    if not bookmarks:
        st.info("You haven't bookmarked any messages yet. Star important messages in your conversations to save them here!")
    else:
        for bookmark in bookmarks:
            with st.container():
                st.markdown(f"**Message** (saved on {bookmark.created_at.strftime('%Y-%m-%d %H:%M')})")
                st.markdown(f'<div class="chat-message assistant-message">🤖 {bookmark.message.content}</div>', unsafe_allow_html=True)
                
                if st.button("Remove Bookmark", key=f"remove_{bookmark.id}"):
                    conversation_manager.unbookmark_message(user, bookmark.message_id)
                    st.rerun()
                
                st.markdown("---")


def render_admin_dashboard():
    """Render the admin dashboard."""
    st.markdown('<div class="main-header">📊 Admin Dashboard</div>', unsafe_allow_html=True)
    
    # Stats overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_users = analytics_manager.get_total_users()
        st.metric("Total Users", total_users)
    
    with col2:
        total_convs = analytics_manager.get_total_conversations()
        st.metric("Total Conversations", total_convs)
    
    with col3:
        total_msgs = analytics_manager.get_total_messages()
        st.metric("Total Messages", total_msgs)
    
    st.markdown("---")
    
    # User stats
    st.subheader("👥 User Statistics")
    user_stats = analytics_manager.get_user_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("First-time Users", user_stats['first_time'])
    with col2:
        st.metric("Returning Users", user_stats['returning'])
    with col3:
        st.metric("Active (7 days)", user_stats['active_last_7_days'])
    
    st.markdown("---")
    
    # Recent queries
    st.subheader("🔍 Recent Queries")
    queries = analytics_manager.get_popular_queries(limit=20)
    
    if queries:
        for q in queries:
            st.text(f"[{q['timestamp'].strftime('%Y-%m-%d %H:%M')}] {q['query'][:100]}")
    else:
        st.info("No queries yet.")
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📈 Recent Activity")
    activity = analytics_manager.get_recent_activity(days=7)
    
    if activity:
        for a in activity[:20]:
            st.text(f"[{a['created_at'].strftime('%Y-%m-%d %H:%M')}] User {a['user_id']} - {a['event_type']}")
    else:
        st.info("No recent activity.")


def main():
    """Main application entry point."""
    initialize_app()
    
    # Check authentication
    if not st.session_state.authenticated:
        render_login_page()
        return
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if "Chat" in page:
        render_chat_page()
    elif "Bookmarks" in page:
        render_bookmarks_page()
    elif "Admin" in page:
        if auth_manager.is_admin(st.session_state.user.email):
            render_admin_dashboard()
        else:
            st.error("Access denied. Admin privileges required.")


if __name__ == "__main__":
    main()
