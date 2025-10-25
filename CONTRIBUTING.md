# Contributing to Boeing India Career Chatbot

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/ideal-sniffle.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes thoroughly
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Run setup script
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
streamlit run app.py
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small
- Comment complex logic

## Testing

Before submitting a PR:
1. Test the login flow
2. Test chat functionality
3. Test bookmarking
4. Test admin dashboard (if applicable)
5. Check for any console errors

## Adding New Features

### Adding Knowledge Base Content

Edit `utils/knowledge.py` and add entries to the `boeing_knowledge` list:

```python
{
    "title": "Your Topic Title",
    "content": "Detailed information...",
    "source": "source.com",
    "category": "category_name"
}
```

### Adding New Pages

1. Create render function in `app.py`
2. Add navigation option in sidebar
3. Implement page logic

### Modifying LLM Behavior

Edit the `SYSTEM_PROMPT` in `utils/llm.py` to change the chatbot's personality and behavior.

## Pull Request Guidelines

- Provide clear description of changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure no breaking changes to existing functionality
- Update documentation if needed

## Reporting Issues

When reporting issues, include:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome! Please:
- Check if the feature already exists
- Clearly describe the feature and use case
- Explain why it would be beneficial

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## Questions?

Open an issue or discussion on GitHub for any questions!

Thank you for contributing! 🎉
