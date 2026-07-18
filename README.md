# AI-Based Personal Finance & Investment Application (India)

## 🚀 Overview
A comprehensive, production-ready AI-powered personal finance and investment management application specifically designed for the Indian market (NSE stocks, INR currency).

## 🛠️ Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit (Multi-page app)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Charts**: Plotly
- **ML/DL**: LSTM/BiLSTM, XGBoost, Autoencoder, Reinforcement Learning (PPO)
- **AI Agents**: LangChain
- **Market Data**: yfinance (NSE)

## 📁 Project Structure
```
finance/
├── backend/                    # FastAPI backend
│   ├── api/                   # API endpoints
│   ├── crud/                  # CRUD operations
│   ├── schemas/               # Pydantic schemas
│   └── main.py               # FastAPI app
├── database/                   # Database layer
│   ├── models.py             # SQLAlchemy models
│   ├── connection.py         # MySQL connection
│   └── init_db.py            # Database initialization
├── ml_models/                  # ML/DL models
│   ├── lstm_forecasting.py   # Net worth forecasting
│   ├── xgboost_returns.py    # Investment returns prediction
│   ├── autoencoder_anomaly.py # Expense anomaly detection
│   └── rl_portfolio.py       # Portfolio allocation (RL)
├── agents/                     # LangChain AI agents
│   ├── market_data_agent.py
│   ├── risk_analysis_agent.py
│   ├── investment_advisor_agent.py
│   └── loan_optimization_agent.py
├── frontend/                   # Streamlit frontend
│   ├── pages/                # Multi-page app
│   │   ├── 1_income_expenses.py
│   │   ├── 2_ai_investment.py
│   │   ├── 3_financial_products.py
│   │   └── 4_summary_report.py
│   ├── components/           # Reusable components
│   └── utils/                # Helper functions
├── utils/                      # Shared utilities
│   ├── market_data.py        # Real-time market data fetching
│   ├── calculations.py       # Financial calculations
│   └── pdf_generator.py      # Monthly report PDF
├── config/                     # Configuration files
│   └── settings.py
├── app.py                      # Main Streamlit app
├── requirements.txt
└── README.md
```

## 🎯 Features

### 1️⃣ Income & Expenses
- Monthly salary tracking
- Other income sources
- Category-wise expense management
- Historical data entry support

### 2️⃣ AI Investment Suggestions
- Risk-based investment allocation (Low/Medium/High)
- ML-powered recommendations using:
  - LSTM for trend forecasting
  - XGBoost for return prediction
  - Reinforcement Learning for dynamic allocation
- Intelligent asset allocation: SIP, Mutual Funds, Stocks, FD, Savings, Insurance

### 3️⃣ Financial Products
- **Stock Market**: Real-time NSE stock tracking
- **SIP/Mutual Funds**: Monthly SIP with real-time returns
- **SWP**: Systematic Withdrawal Plan
- **Loans**: Home, Personal, Mortgage with EMI calculation
- **Insurance**: Term, Life, Health, Child, Retirement
- **Credit Cards**: Limit, outstanding, due date tracking
- **Lump Sum**: Fixed deposit calculator

### 4️⃣ Summary & Monthly Report
- Net worth calculation and history
- Interactive visualizations:
  - Investment allocation pie chart
  - Net worth growth line graph
  - Monthly investment bar chart
- Automated PDF report generation

## 🤖 AI/ML Components

### Machine Learning Models
1. **LSTM/BiLSTM**: 6-12 month net worth forecasting
2. **XGBoost**: Investment return prediction
3. **Autoencoder**: Expense anomaly detection
4. **Reinforcement Learning (PPO)**: Dynamic portfolio optimization

### AI Agents (LangChain)
1. **Market Data Agent**: Real-time market data analysis
2. **Risk Analysis Agent**: Risk profiling and assessment
3. **Investment Advisor Agent**: Personalized investment recommendations
4. **Loan Optimization Agent**: EMI and prepayment strategies

## 🗄️ Database Schema
- Users
- Income & Expenses (month-wise)
- Investments (monthly snapshots)
- Stocks
- Loans
- Insurance policies
- Credit cards
- Net worth history

## ⚙️ Installation

### Prerequisites
```bash
# Install MySQL
brew install mysql  # macOS
brew services start mysql

# Create database
mysql -u root -p
CREATE DATABASE finance_db;
CREATE USER 'finance_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON finance_db.* TO 'finance_user'@'localhost';
FLUSH PRIVILEGES;
```

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure database
# Edit config/settings.py with your MySQL credentials

# Initialize database
python database/init_db.py

# Run FastAPI backend
uvicorn backend.main:app --reload --port 8000

# Run Streamlit frontend (in another terminal)
streamlit run app.py
```

## 🚀 Usage

1. Access the application at `http://localhost:8501`
2. Navigate through the 4 main options:
   - Income & Expenses
   - AI Investment Suggestions
   - Financial Products
   - Summary & Monthly Report
3. Backend API available at `http://localhost:8000/docs`

## 📊 Monthly Automation
- Automatic asset value calculation
- Liability tracking
- Net worth snapshots
- Background scheduler for monthly updates

## 🔐 Security Considerations
- Environment variables for sensitive data
- Password hashing for user authentication
- SQL injection prevention via SQLAlchemy ORM
- Input validation with Pydantic schemas

## 🇮🇳 India-Specific Features
- Currency: Indian Rupees (₹)
- Stock Market: NSE (National Stock Exchange)
- Real-time Indian stock prices via yfinance (.NS suffix)
- Indian financial product categories

## 📝 Future Enhancements
- Multi-user support with authentication
- Mobile app integration
- Tax calculation (Indian tax slabs)
- Goal-based investment planning
- Real-time notifications

## 📄 License
MIT License

## 👨‍💻 Author
D Manasa Sowmya
Built as a professional fintech solution for personal finance management
