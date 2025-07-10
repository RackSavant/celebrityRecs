# Racksavant - Multi-Agent Fashion Recommendation System

A sophisticated fashion recommendation system built with multiple AI agents that work together to provide personalized fashion recommendations.

## Features

- Multi-agent architecture for specialized fashion tasks
- Style classification and analysis
- Conversational AI for natural interactions
- Visual search capabilities
- Personalized recommendations
- Modern UI built with Streamlit

## Project Structure

```
racksavant/
├── agents/               # AI agents implementing specific fashion tasks
├── core/                 # Core business logic and models
├── infrastructure/       # Infrastructure components and integrations
├── ui/                  # User interface components
└── tests/               # Test files
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your environment variables

4. Run the application:
```bash
streamlit run ui/streamlit_app.py
```

## Environment Variables

Copy `.env.example` to `.env` and configure the following variables:
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- PINECONE_API_KEY
- PINECONE_ENVIRONMENT
- ELASTICSEARCH_URL
