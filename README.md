# ✈️ Boeing India Career Chatbot

A production-ready AI-powered chatbot designed to help engineering students in India learn about Boeing India careers, placements, internships, job roles, and career paths. Built with Streamlit, Google Gemini AI, and PostgreSQL.

## 🎯 Features

### Core Functionality
- **Multi-turn Conversations**: Intelligent context-aware conversations with memory across sessions
- **Personalized Experience**: Differentiate first-time vs returning users
- **Comprehensive Knowledge**: Information about Boeing India placements, internships, roles, career paths, and company insights
- **Real-time Updates**: Integration with APIs for latest data
- **Career Guidance**: Resume tips, interview prep, skill-building advice, and project suggestions

### User Features
- **Google OAuth Login**: Secure authentication
- **Chat History**: Full conversation history with persistent storage
- **Message Bookmarking**: Star important messages for later reference
- **Multi-session Memory**: Bot remembers context across sessions

### Admin Features
- **Analytics Dashboard**: View user statistics, query logs, and activity
- **Access Control**: Admin-only dashboard controlled by environment variable
- **Rate Limiting**: Prevent abuse with configurable limits

### Technical Features
- **LLM Integration**: Google Gemini API for conversational intelligence
- **Vector Search**: Semantic search using embeddings for knowledge retrieval
- **Database**: PostgreSQL/Supabase for persistent storage
- **Security**: Rate limiting, OAuth session management, secure secret handling
- **Deployment Ready**: Docker containerization for easy deployment

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (or use SQLite for development)
- Google Cloud account (for OAuth)
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ull0sm/ideal-sniffle.git
cd ideal-sniffle
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Set up Streamlit secrets**
```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml with your credentials
```

6. **Run the application**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Copy and configure environment file
cp .env.example .env
# Edit .env with your credentials

# Start services
docker-compose up -d

# View logs
docker-compose logs -f chatbot

# Stop services
docker-compose down
```

### Using Docker Only

```bash
# Build image
docker build -t boeing-chatbot .

# Run container
docker run -p 8501:8501 \
  --env-file .env \
  boeing-chatbot
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URI=postgresql://user:password@localhost:5432/boeing_chatbot

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
OAUTH_REDIRECT_URI=http://localhost:8501

# API Keys
GEMINI_API_KEY=your-gemini-api-key
LANGSEARCH_API_KEY=your-langsearch-api-key

# Admin
ADMIN_EMAILS=admin@example.com,admin2@example.com

# Security
SECRET_KEY=your-secret-key-change-in-production

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8501` (or your domain)
6. Copy Client ID and Client Secret to `.env`

### Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env` as `GEMINI_API_KEY`

## 📚 Project Structure

```
ideal-sniffle/
├── app.py                 # Main Streamlit application
├── config/
│   └── settings.py        # Configuration settings
├── models/
│   └── database.py        # Database models (SQLAlchemy)
├── utils/
│   ├── auth.py           # Authentication utilities
│   ├── database.py       # Database connection
│   ├── llm.py            # Gemini LLM integration
│   ├── knowledge.py      # Knowledge base & retrieval
│   ├── conversation.py   # Conversation management
│   ├── rate_limit.py     # Rate limiting
│   └── analytics.py      # Analytics utilities
├── .streamlit/
│   └── secrets.toml      # Streamlit secrets (not in git)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker container config
├── docker-compose.yml   # Docker Compose config
└── README.md           # This file
```

## 💡 Usage

### For Students

1. **Login**: Click "Login with Google" on the homepage
2. **Start Chatting**: Ask questions about Boeing India careers
3. **Bookmark Messages**: Click the star icon on helpful responses
4. **View History**: Access previous conversations from the sidebar

### Example Queries

- "Tell me about Boeing India's placement process"
- "What internship opportunities are available at Boeing India?"
- "How should I prepare my resume for Boeing India?"
- "What skills do I need for a software engineer role at Boeing India?"
- "Can you suggest projects for aerospace engineering students?"

### For Admins

1. **Login** with an admin email (configured in `ADMIN_EMAILS`)
2. **Navigate** to Admin Dashboard from sidebar
3. **View** analytics, user statistics, and query logs

## 🔒 Security Features

- **OAuth Authentication**: Secure Google-based login
- **Rate Limiting**: Configurable per-minute and per-hour limits
- **Secrets Management**: Environment-based configuration
- **Session Management**: Secure user session handling
- **Input Validation**: Protection against malicious inputs

## 🧪 Testing

For development, you can use demo mode if OAuth is not configured:
1. Leave `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` empty in `.env`
2. Click "Continue in Demo Mode" on login page

## 📊 Database Schema

The application uses the following main tables:
- **users**: User profiles and authentication
- **conversations**: Chat conversations
- **messages**: Individual messages in conversations
- **bookmarks**: Starred/bookmarked messages
- **analytics**: Usage analytics and logs
- **knowledge_base**: Boeing India knowledge articles

## 🔄 Adding New Knowledge

To add more Boeing India information:

1. Edit `utils/knowledge.py`
2. Add entries to `boeing_knowledge` list in `initialize_knowledge_base()`
3. Restart the application

Or programmatically:
```python
from utils.knowledge import retriever

retriever.add_knowledge(
    title="New Topic",
    content="Detailed information...",
    source="source.com",
    category="category_name"
)
```

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub
2. Connect repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in Streamlit Cloud dashboard
4. Deploy

### Cloud Platforms

The application is containerized and can be deployed to:
- AWS (ECS, Fargate, EC2)
- Google Cloud (Cloud Run, GKE, Compute Engine)
- Azure (Container Instances, AKS)
- Heroku
- DigitalOcean App Platform

## 🤝 Contributing

This is a demonstration project. Feel free to fork and customize for your needs.

## 📝 License

MIT License - feel free to use this project for your own purposes.

## 📧 Support

For issues or questions, please open an issue on GitHub.

## 🎓 Target Audience

This chatbot is specifically designed for:
- Engineering students in India
- Students interested in Boeing India careers
- Students preparing for campus placements
- Students seeking internship opportunities

## ⚡ Performance

- **Response Time**: < 3 seconds average
- **Concurrent Users**: Supports multiple users simultaneously
- **Rate Limits**: Configurable (default: 10/min, 100/hour per user)
- **Uptime**: Designed for 24/7 operation

## 🔮 Future Enhancements

Potential improvements:
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Voice input/output
- [ ] Mobile app
- [ ] Integration with job portals
- [ ] Resume analysis feature
- [ ] Mock interview simulator
- [ ] Referral tracking system

---

Built with ❤️ for engineering students aspiring to join Boeing India