# Boeing India Career Chatbot - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                          │
│                    (Streamlit Web App)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ Login Page   │  │ Chat Page    │  │ Admin Dashboard    │   │
│  │ - OAuth Flow │  │ - Messages   │  │ - Analytics        │   │
│  │ - Demo Mode  │  │ - Bookmarks  │  │ - Query Logs       │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│                         (app.py)                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Session Management  │  Rate Limiting  │  Auth Manager    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Auth Utils     │  │   LLM Utils      │  │  Knowledge Base  │
│  (utils/auth.py) │  │ (utils/llm.py)   │  │(utils/knowledge) │
│                  │  │                  │  │                  │
│ - Google OAuth   │  │ - Gemini API     │  │ - ChromaDB       │
│ - User Session   │  │ - Context Mgmt   │  │ - Embeddings     │
│ - Admin Check    │  │ - Prompt Eng.    │  │ - Vector Search  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │ Conversation Mgr │  │  Rate Limiter    │  │  Analytics   │ │
│  │ (conversation.py)│  │ (rate_limit.py)  │  │(analytics.py)│ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data Access Layer                          │
│                   (utils/database.py)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Session Management  │  Context Managers  │  Init DB      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL/    │  │    ChromaDB      │  │   Google APIs    │
│    Supabase      │  │  (Vector Store)  │  │  - OAuth         │
│                  │  │                  │  │  - Gemini        │
│ - Users          │  │ - Embeddings     │  │  - (Langsearch)  │
│ - Conversations  │  │ - Knowledge Base │  │                  │
│ - Messages       │  │ - Semantic       │  │                  │
│ - Bookmarks      │  │   Search         │  │                  │
│ - Analytics      │  │                  │  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## Data Flow

### 1. User Login Flow
```
User → Google OAuth → auth.py → User Model → Database → Session State
```

### 2. Chat Message Flow
```
User Input → app.py → Rate Limiter → knowledge.py (retrieve context)
    ↓
Gemini API ← llm.py ← Context + History
    ↓
Response → conversation.py → Save to DB → Display to User
```

### 3. Bookmark Flow
```
Star Click → conversation.py → Bookmark Model → Database → Update UI
```

### 4. Admin Dashboard Flow
```
Admin User → Check admin_emails → analytics.py → Queries DB → Display Stats
```

## Component Interactions

### Configuration Layer
```
config/settings.py
    ↓
- Loads environment variables (.env)
- Validates configuration
- Provides settings to all modules
```

### Database Models (models/database.py)
```
Base (SQLAlchemy)
    ├── User
    ├── Conversation
    ├── Message
    ├── Bookmark
    ├── Analytics
    └── KnowledgeBase
```

### Utility Modules
```
utils/
    ├── database.py     → Database connection & sessions
    ├── auth.py         → Authentication & user management
    ├── llm.py          → AI response generation
    ├── knowledge.py    → Vector search & context retrieval
    ├── conversation.py → Conversation & message management
    ├── rate_limit.py   → Request rate limiting
    └── analytics.py    → Usage statistics & reporting
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                 │
├─────────────────────────────────────────┤
│ 1. OAuth 2.0 Authentication             │
│    - Google identity verification       │
│    - Token-based sessions               │
├─────────────────────────────────────────┤
│ 2. Rate Limiting                        │
│    - Per-user request limits            │
│    - Configurable thresholds            │
├─────────────────────────────────────────┤
│ 3. Environment Secrets                  │
│    - API keys in .env                   │
│    - Streamlit secrets.toml             │
├─────────────────────────────────────────┤
│ 4. Database Security                    │
│    - SQLAlchemy ORM (SQL injection)     │
│    - Parameterized queries              │
├─────────────────────────────────────────┤
│ 5. Admin Access Control                 │
│    - Email-based authorization          │
│    - Environment variable config        │
└─────────────────────────────────────────┘
```

## Deployment Architecture

### Docker Deployment
```
┌──────────────────────────────────────────┐
│          Docker Compose                  │
├──────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐ │
│  │   Chatbot      │  │   PostgreSQL   │ │
│  │   Container    │  │   Container    │ │
│  │                │  │                │ │
│  │ - Streamlit    │  │ - Database     │ │
│  │ - Python App   │  │ - Persistence  │ │
│  │ - ChromaDB     │  │                │ │
│  │                │  │                │ │
│  │ Port: 8501     │  │ Port: 5432     │ │
│  └────────────────┘  └────────────────┘ │
└──────────────────────────────────────────┘
```

### Cloud Deployment Options
```
┌────────────────────────────────────────────────┐
│  Streamlit Cloud / AWS / GCP / Azure / Heroku  │
├────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────┐ │
│  │         Application Instance             │ │
│  │  - Streamlit App (app.py)                │ │
│  │  - Environment Variables                 │ │
│  └──────────────────────────────────────────┘ │
│                     │                          │
│  ┌─────────────────┼─────────────────┐        │
│  ▼                 ▼                 ▼        │
│  External DB    ChromaDB         Google APIs  │
│  (Supabase)     (Persistent)     (OAuth+AI)   │
└────────────────────────────────────────────────┘
```

## Key Design Patterns

### 1. Repository Pattern
```
Database Models ← → Utils (database.py) ← → Business Logic
```

### 2. Singleton Pattern
```
- settings (config/settings.py)
- auth_manager (utils/auth.py)
- chatbot (utils/llm.py)
- retriever (utils/knowledge.py)
- conversation_manager (utils/conversation.py)
```

### 3. Factory Pattern
```
get_db() → Creates database sessions as needed
```

### 4. Strategy Pattern
```
Knowledge retrieval strategies:
- Vector search (ChromaDB)
- Database queries (SQLAlchemy)
- API calls (Gemini, Langsearch)
```

## Performance Considerations

### Caching
```
- Session state for user data
- ChromaDB persistent storage
- Database connection pooling
```

### Optimization
```
- Lazy loading of models
- Batch operations where possible
- Efficient SQL queries with ORM
- Vector search indexing
```

### Scalability
```
- Stateless application design
- Database-backed sessions
- Horizontal scaling ready
- Docker containerization
```

## Monitoring & Logging

```
Analytics Table
    ├── Login events
    ├── Query logs
    ├── Bookmark actions
    └── System events

Admin Dashboard
    ├── User statistics
    ├── Query patterns
    ├── Activity timeline
    └── Usage metrics
```

---

**Architecture Status: Production-Ready ✅**

This architecture supports:
- High availability
- Horizontal scaling
- Easy maintenance
- Security best practices
- Modular extensibility
