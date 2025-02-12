# Apollo - Deep Research Agent 🚀

Apollo is an advanced AI-powered research agent that conducts comprehensive, multi-layered research on any given topic. It generates key questions, performs deep analysis, and compiles detailed reports by leveraging both OpenAI's GPT-4o and Google's Gemini Pro models.

## 🌟 Features

- **Intelligent Question Generation**: Automatically generates primary and follow-up questions to explore topics deeply
- **Multi-Model Analysis**: Utilizes both GPT-4 and Gemini Pro for comprehensive analysis
- **Automated Web Research**: Performs intelligent web searches and content extraction
- **Hierarchical Question Structure**: Creates tree-like question structures for thorough topic exploration
- **Smart Content Analysis**: Analyzes source credibility and content relevance
- **Detailed Report Generation**: Compiles comprehensive research reports with citations

## 🛠️ Technology Stack

- FastAPI for the backend framework
- OpenAI GPT-4 for question generation and report compilation
- Google Gemini Pro for content analysis
- Crawl4AI for web content extraction
- SerpAPI for search capabilities
- Pydantic for data validation
- AsyncIO for asynchronous operations

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key
- Google API key (for Gemini)
- SerpAPI key

## 🚀 Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/apollo.git
cd apollo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_gemini_key
SERP_API_KEY=your_serp_api_key
```

## 🏃‍♂️ Running the Application

1. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

2. The API will be available at `http://localhost:8000`

## 🔄 API Endpoints

### POST /research/

Conducts comprehensive research on a given topic.

Request body:

```json
{
  "topic": "JFK Assassination",
  "depth": 2,
  "max_questions": 5
}
```

Response:

```json
{
    "topic": "JFK Assassination",
    "main_questions": [...],
    "summary": "...",
    "detailed_analysis": "..."
}
```

## 📁 Project Structure

```
research_agent/
├── core/
│   ├── question_generator.py
│   ├── search_engine.py
│   ├── content_analyzer.py
│   └── report_compiler.py
├── models/
│   └── schemas.py
├── config/
│   └── settings.py
└── main.py
```

## 🔧 Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `GOOGLE_API_KEY`: Your Google API key for Gemini
- `SERP_API_KEY`: Your SerpAPI key for web searches

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Usage Example

```python
import requests

api_url = "http://localhost:8000/research/"
payload = {
    "topic": "Quantum Computing",
    "depth": 2,
    "max_questions": 5
}

response = requests.post(api_url, json=payload)
research_report = response.json()
```

## ⚙️ Core Components

1. **Question Generator**: Generates intelligent research questions using GPT-4
2. **Content Analyzer**: Analyzes web content using Gemini Pro
3. **Report Compiler**: Compiles comprehensive reports using both models
4. **Search Engine**: Performs targeted web searches for relevant content

## 🔒 Security

- API keys are managed through environment variables
- Input validation using Pydantic models
- Error handling for API requests
