# Quotes Bot with RASA NLU

A chatbot that recommends inspirational quotes based on your mood using sentiment analysis.

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# OR (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Bot

**Option 1 - Windows:**

```bash
run_bot.bat
```

**Option 2 - Manual:**

```bash
# Terminal 1: Start action server
rasa run actions

# Terminal 2: Run chatbot
rasa shell
```

## Project Structure

```
Quotes-bot-with-RASA-NLU-/
├── actions.py              # Main action file
├── actions/                # Modular actions (recommended)
│   ├── config.py
│   ├── quote_recommender.py
│   └── sentiment_service.py
├── quotes/
│   └── quotes.json        # Quote database
├── data/                  # NLU training data
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── models/                # Trained models
├── tests/                 # Test files
├── Dockerfile
└── requirements.txt
```

## Usage

| Command                 | Response            |
| ----------------------- | ------------------- |
| `hello`                 | Greeting message    |
| `I'm sad` / `I'm happy` | Mood-based quote    |
| `motivate me`           | Inspirational quote |
| `bye`                   | Goodbye message     |

## Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest tests/ --cov
```

## Dependencies

- rasa==3.6.16
- rasa-sdk==3.6.2
- textblob==0.17.1
- vaderSentiment==3.3.2

## Troubleshooting

**Action server fails to start?**

- Check port 5055 is available
- Run: `pip install -r requirements.txt`

**Model not found?**

- Train new model: `rasa train`
- Models are in `models/` directory
