# Quick Start Guide - Boeing India Career Chatbot

## For Development (Without Full Dependencies)

If you just want to test the structure without all external dependencies:

```bash
# Install core dependencies only
pip install streamlit sqlalchemy pydantic pydantic-settings python-dotenv

# Run verification
python3 verify.py

# The database and settings should work
```

## For Full Setup

```bash
# Run the automated setup script
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and credentials

# Run the app
streamlit run app.py
```

## Required API Keys and Credentials

### Google OAuth (Required for authentication)
1. Go to https://console.cloud.google.com/
2. Create/select a project
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add to `.env`:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`

### Google Gemini API (Required for AI)
1. Go to https://makersuite.google.com/app/apikey
2. Create an API key
3. Add to `.env` as `GEMINI_API_KEY`

### Database (Optional - defaults to SQLite)
- For production, use PostgreSQL/Supabase
- Set `DATABASE_URI` in `.env`
- Default: `sqlite:///./chatbot.db` (auto-created)

### Admin Access (Optional)
- Set `ADMIN_EMAILS` in `.env` (comma-separated)
- Example: `admin@example.com,admin2@example.com`

## Demo Mode

For testing without Google OAuth:
1. Leave `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` empty
2. Run `streamlit run app.py`
3. Click "Continue in Demo Mode"

## Docker Quick Start

```bash
# With Docker Compose (easiest)
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d

# Access at http://localhost:8501
```

## Verification

Run the verification script to check setup:
```bash
python3 verify.py
```

## Troubleshooting

**Issue**: "No module named 'X'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: "Database URI not configured"
- **Solution**: Set `DATABASE_URI` in `.env` or use default SQLite

**Issue**: "Google OAuth failed"
- **Solution**: Verify OAuth credentials or use demo mode

**Issue**: "Rate limit exceeded"
- **Solution**: Wait or adjust `RATE_LIMIT_PER_MINUTE` in `.env`

## Features Overview

### For Students
- ✈️ Chat about Boeing India careers
- 📚 Learn about placements and internships
- ⭐ Bookmark important messages
- 🔍 Search conversation history
- 💡 Get personalized career advice

### For Admins
- 📊 View analytics dashboard
- 👥 Monitor user activity
- 📈 Track popular queries
- 📝 Review conversation logs

## Default Credentials

**Demo Mode**:
- Email: demo@example.com
- Name: Demo User

**Admin Access**: Configure in `ADMIN_EMAILS` environment variable

## Next Steps

1. Configure your `.env` file
2. Run `streamlit run app.py`
3. Login with Google (or demo mode)
4. Start chatting!

## Documentation

- Full README: `README.md`
- Contributing: `CONTRIBUTING.md`
- Code structure: See "Project Structure" in README

## Support

Open an issue on GitHub for help!
