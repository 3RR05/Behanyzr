
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400..700&display=swap" rel="stylesheet">

<img src=App/Static/Images/Behanyzr.jpeg alt="It should be the logo showing here, guess it is a path problem" style="border-radius: 60px;" >


## 📊 Behanyzr - Behavior Drift Analyzer ~

 A web application that tracks and analyzes behavioral and sentiment shifts using data scraped from Reddit/NewsAPI (Able to scrap from other social media if make some changes in Utility modules).

<div style="background-color: rgba(235, 128, 71, 0.18); border-left: 5px solid rgba(239, 124, 30, 0.87); padding: 15px; border-radius: 15px;"><h2 style="margin-top:0">🥁 Disclaimer</h2>
 <strong>This project is designed to only show sentiment drifts as positive/neutral/negative by comparing it with previous time windows, not the actual emotional state of a text context, so a negative/positive drift increment in a source only means the improvement of the text's sentiment label that depends on the text-case manner (Also sarcasm or slangs affect the model to render neutral to the word which would significantly affect the overall analysis, future deep learning model enhancements will fix the issue drastically)</strong>
 </div>
    
## 🧩 Features and It's state ~

**🛠️ Data collection** : Scrape reddit posts and news articles, then load it on database

**🛠️ Sentiment analysis** : Track sentiment changes on texts over time(It only analyze the changes in sentiment as positive/negative rather than track whole texts emotional context because of Lexicon-based model)

**🛠️ Drift detection** : Identify significant behavioral drift using timeframes on the source

**🛠️ Vocabulary Evolution** : Able to show topics shifts (Right now, it could only show word comparison by comparing previous timeframe with current one and show words that are most used ~ But the library to figure important words is still under configuration)

**🛠️ Visualization** : Visualize all processed insights with charts to view the analyzed report

## ⚙️ Tools and Libraries  ~

- **Backend & Requests**: Flask, SQLAlchemy
- **Data Processing**: Pandas, NumPy
- **Lexicon-Model**: VADERSentiment
- **Visualization**: Matplotlib, Seaborn
- **Web Scraping**: BeautifulSoup, Requests
- **Database**: SQLite/PostgreSQL
- **Frontend Templating**: Bootstrap 5, Jinja2

## 📎 Use Cases

- Track brand sentiment evolution after product launches on social media (Like Reddit which is used in this project)
- Monitor community conversation trends 
- Analyze public opinion during any events (Like Geopolicts, Economy)
- Study topic emergence and decline (Able to see most used words which helps to understand approximately)
- Research social media behavior patterns

<div style="background-color: rgba(72, 72, 198, 0.18); border-left: 5px solid rgba(72,72,198,0.87); padding: 15px; border-radius: 15px;">This project uses VADERSentiment to analyze sentiment and calculate values according to the each word's intensifier and feature. (Rule-Based Model like VADERSentiment will assigns positive/negative/neutral labels for each word on a text rather than the whole context of the text which advanced Deep learning models could understand the text context, <strong>For Example:</strong> "i had been in hospital for 5 months, and it was painful, but i survived a major accident", where VADER will only assign values based on each word, so it count negative like painful, accident and coma as dominant and flag the overall text as negative, it assign negative regardless of the positive outcome of the text where a human could understand, but a DL model could able understand the context and flag it as positve ~ I do my best to work on that one later, this is my first time learning and implementing these logical modules)</div>

## 💽 Installation

### Prerequisites

- Python (V.3.8 or later)
- pip (Package Installer,which is used to install needed dependencies mentioned in `Req.txt`)

### ⛓️ Setup

1. **Clone the repo**
```bash
   git clone https://github.com/3RR05/Behanyzr.git
   cd Behanyzr # Or whatever name you want for your root directory
```

2. **Create virtual environment**
```bash
   # Isolate the dependencies, don't fall in "Dependencies Hell" 
   python -m venv venv 
   
   # For Windows
   venv\Scripts\activate
   
   # For Mac/Linux
   source venv/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r Req.txt # Sorry, Many things freezed on this one
```

4. **Set up environment variables**
```bash
   cp .env.example .env
   # Edit .env and add your SECRET_KEY & NEWS_API_KEY
```

5. **Initialize database**
```bash
   python Behanyzr.py init-db
```

6. **Run the application**
```bash
   python Behanyzr.py
```

7. **Open in browser**
```
   http://localhost:5000
```

## 🧱 Project Structure
```
Behanyzr/
├── App/
│   ├── __init__.py              # Flask app factory
│   ├── Config.py                # Configuration
│   ├── Model/                   # Database models
│   ├── Route/                   # Web & API routes
│   ├── Utils/                   # Core functionality
│   │   ├── scraper.py           # Reddit scraper
│   │   ├── scraper_news.py      # NewsAPI scraper
│   │   ├── prep.py              # Text cleaning
│   │   ├── sentiment.py         # Sentiment analysis
│   │   ├── drift_det.py         # Drift detection
│   │   └── visual.py            # Chart generation
│   ├── static/                  # Stock media
│   └── templates/               # HTML templates
├── Data/                        # Data storage (Future enhancement)
├── venv/                        # Virtual environment
├── .env                         # Environment variables
├── .gitignore
├── Req.txt
├── B_server.py                  # Render deployer
├── render.yaml                  # Render instruction
├── READTHIS.md
├── Behanyzr.py                  # Application entry
├── Test_analysis.py
├── Test_scraper.py
└── Test_visuals.py
```
## 🧪 Testing

```bash
# Test scraper
python Test_scraper.py

# Test analysis
python Test_analysis.py

# Test visualizations
python Test_visuals.py
```

## 💡 How It Works

### 1. Data Collection
- Web scraping (BeautifulSoup) or API calls (Requests)
- Store in SQLite database with timestamps

### 2. Text Processing
- Clean text (remove URLs, special characters)
- Tokenization and stop word removal
- Organize into time windows (hourly/daily/weekly)
<div style="background-color: rgba(72, 72, 198, 0.18); border-left: 5px solid rgba(72,72,198,0.87); padding: 15px; border-radius: 15px;">Currently the project uses VADERSentiment which don't need text cleaning, But still left some codes, so you can configure the module for your cleaning preferences and helps you to learn how the text cleaning works if you do the cleaning preprocess by yourself.</div>

### 3. Sentiment Analysis
- Rule-based model with weighted words
- Context handling (negations)
- Score normalization (-1 to 1)

### 4. Drift Detection
- Calculate sentiment changes between time windows
- Detect topic shifts
- Identify significant shifts (Threshold-based ~ Current threshold is ```0.2```)

### 5. Visualization
- Generate charts using Matplotlib/Seaborn
- Encode as base64 for web display
- Multiple chart types for comprehensive view

## ⚖️ Security & Ethics

- Respects `robots.txt` by limiting request and text rates
- User-Agent identification in requests
- Delays between requests (2 seconds)
- No authentication token storage in code (Might do in future)
- This project is for Educational purpose

## ⛓️‍💥 Limitations

- Sentiment analysis is rule-based (not deep learning)
- Free tier APIs have rate limits
- SQLite suitable for demo, not production scale (Might Use PostgreSQL on render)

## 🔮 Future Enhancements (If Possible)

- [ ] Advanced ML/DL sentiment models (BERT, Transformers)
- [ ] Real-time data streaming
- [ ] User authentication
- [ ] Export reports (PDF, CSV)
- [ ] Comparison across multiple sources
- [ ] Emotion detection (beyond sentiment)

## 🤝 Contribution

Contributions Blissfully Welcomes Here!, if you want to add/fix some things in this project:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/fishbone-cleared`) ~ Name whatever you like  
3. Commit changes (`git commit -m 'cleared the fishbone'`)
4. Push to branch (`git push origin feature/fishbone-cleared`)
5. Open a Pull Request

## 📃 License

This project is open-source and available under the [MIT License](LICENSE) ⚖️.

## 👨‍💻 Scribbler

<h1 style="font-family:'Pixelify Sans';font-size:50px;text-align:center;color:#934eed">3RR05</h1>

<h2 style="font-family:'Great Vibes'; text-align:center; letter-spacing:3px;color:#2aeb51"> ✨Gramercy For Thy Viewing/Forking Of This Creation✨<h2>
