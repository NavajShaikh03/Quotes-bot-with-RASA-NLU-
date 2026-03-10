# Quotes Bot with RASA NLU

A Rasa 3.x chatbot that responds to how you feel (`happy`, `sad`, or needing `motivation`) with a **random inspirational quote** every time.

## Quick Start

### ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/NavajShaikh03/Quotes-bot-with-RASA-NLU-.git
cd Quotes-bot-with-RASA-NLU-
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Bot

**Option 1 – One‑click (Windows):**

```bash
run_bot.bat
```

This will:

- Train a Rasa model (if needed)
- Start the action server on port 5055
- Start the Rasa server with API on port 5005
- Start the web chat UI on port 5500
- Open the chat UI in your browser

**Option 2 – Manual terminals:**

```bash
# Terminal 1: start action server
rasa run actions --port 5055

# Terminal 2: start Rasa server with API
rasa run --enable-api --cors "*" --port 5005

# (Optional) Terminal 3: start web UI
python web_integration/chat_ui.py  # opens http://localhost:5500
```

You can also chat directly in the console with:

```bash
rasa shell
```

## Project Structure

```
Quotes-bot-with-RASA-NLU-/
├── actions/                 # Modular custom actions (sentiment + quotes service)
│   ├── config.py
│   ├── quote_recommender.py
│   └── sentiment_service.py
├── quotes/
│   └── quotes.json          # Quote database (used by custom action)
├── data/                    # Rasa 3.x training data
│   ├── nlu.yml              # intents: greet, emotion_happy/sad/motivation, etc.
│   ├── rules.yml            # rules mapping intents → responses
│   └── stories.yml          # simple conversation stories
├── models/                  # Trained models
├── tests/                   # Unit tests
├── web_integration/         # Flask-based web chat UI
├── Dockerfile
├── README.md
└── requirements.txt
```

## 🧠 Technologies Used

- **Rasa 3.x (rasa, rasa-sdk)**: Intent classification, dialogue management, and rule-based responses.
- **Python 3.x**: Core implementation language for actions and configuration.
- **TextBlob & VADER Sentiment**: Sentiment analysis utilities (used in the custom actions module).
- **Flask + Flask-CORS**: Simple web server for the browser-based chat UI.
- **HTML, CSS, JavaScript**: Frontend chat interface in `web_integration/templates/index.html`.
- **Pytest + pytest-cov**: Unit testing and coverage reporting.

## Usage

Type messages like:

| Example message                   | What the bot does                |
| --------------------------------- | -------------------------------- |
| `hello`                           | Greets you and asks your mood   |
| `I am sad` / `sad`               | Random **sad‑comfort** quote     |
| `I am happy` / `happy`           | Random **happy/celebration** quote |
| `motivate me` / `I need motivation` | Random **motivation** quote    |
| `bye`                             | Random goodbye message           |

For each emotion (`happy`, `sad`, `motivation`) the bot picks **one quote at random** from multiple responses defined in `domain.yml`, so repeating the same emotion will usually give you a different quote.

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

**Rasa API or web UI not responding?**

- Check ports 5005 (Rasa) and 5500 (web UI) are free
- Make sure you started the servers as shown above

**Model not found?**

- Train a new model: `rasa train`
- Models are stored in the `models/` directory

## Author

Navaj Shaikh  
GitHub: https://github.com/NavajShaikh03

## Project Namespace

quotes_bot_with_rasa_nlu

## Acknowledgment

This project was built by Navaj Yasin Shaikh with assistance from AI tools and online documentation for learning and development support.

## License

MIT License

📄 This project is for educational purposes and learning.
