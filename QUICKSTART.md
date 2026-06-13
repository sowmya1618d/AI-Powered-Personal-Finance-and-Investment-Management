# 🚀 Quick Start Guide - AI Personal Finance Manager

## 📋 Prerequisites

- **Python 3.9+**
- **MySQL 8.0+**
- **macOS, Linux, or Windows with WSL2**
- **OpenAI API Key** (for LangChain agents - optional)

---

## 🔧 Installation

### 1. Clone/Download the Project
```bash
cd /Users/tejsai/Desktop/finance
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Install/start MySQL
- Create `finance_db` database
- Set up Python virtual environment
- Install all dependencies
- Initialize database tables
- Create required directories

### 3. Configure Environment

Edit `.env` file:
```bash
nano .env
```

Update with your credentials:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=finance_user
DB_PASSWORD=your_secure_password
DB_NAME=finance_db
OPENAI_API_KEY=your_api_key_here
DEBUG=True
```

---

## 🎬 Running the Application

### Terminal 1: Start FastAPI Backend
```bash
# Activate virtual environment
source venv/bin/activate

# Start API server
python -m uvicorn backend.main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Access API docs at: **http://localhost:8000/docs**

### Terminal 2: Start Streamlit Frontend
```bash
# Activate virtual environment
source venv/bin/activate

# Start Streamlit app
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

Access the app at: **http://localhost:8501**

---

## 📊 Using the Application

### 1️⃣ Income & Expenses Page
- **Path:** `localhost:8501/pages/1_income_expenses.py`
- **Features:**
  - Add monthly salary and other income
  - Track category-wise expenses
  - View expense history and trends
  - Detect spending anomalies using Autoencoder

### 2️⃣ AI Investment Suggestions
- **Path:** `localhost:8501/pages/2_ai_investment.py`
- **Features:**
  - Input your financial profile
  - Select risk level (Low/Medium/High)
  - Get AI-powered portfolio allocation
  - View expected returns using XGBoost predictions

### 3️⃣ Financial Products Hub
- **Path:** `localhost:8501/pages/3_financial_products.py`
- **Sub-pages:**
  - **Stock Market:** Track NSE stocks in real-time
  - **SIP/Mutual Funds:** Manage SIPs and lump sum investments
  - **Loans:** Home, Personal, Mortgage with auto EMI calculation
  - **Insurance:** Term, Life, Health, Child, Retirement policies
  - **Credit Cards:** Track limits, outstanding, due dates
  - **SWP:** Systematic withdrawal plans with loan linking
  - **Fixed Deposits:** FD maturity calculations

### 4️⃣ Summary & Monthly Reports
- **Path:** `localhost:8501/pages/4_summary_report.py`
- **Features:**
  - Net worth calculation and tracking
  - Investment allocation pie charts
  - Net worth growth line graphs
  - LSTM forecasting for next 6-12 months
  - PDF report generation

---

## 🤖 ML/DL Models

### LSTM Net Worth Forecasting
- **File:** `ml_models/lstm_forecasting.py`
- **Purpose:** Predict net worth 6-12 months into the future
- **Data Required:** 12+ months of historical data

### XGBoost Return Prediction
- **File:** `ml_models/xgboost_returns.py`
- **Purpose:** Predict investment returns based on features
- **Features:** Investment amount, duration, risk level, asset type

### Autoencoder Anomaly Detection
- **File:** `ml_models/autoencoder_anomaly.py`
- **Purpose:** Detect unusual expense patterns
- **Method:** Neural network autoencoder with reconstruction error

### RL Portfolio Optimization (PPO)
- **File:** `ml_models/rl_portfolio.py`
- **Purpose:** Dynamic portfolio allocation optimization
- **Algorithm:** Proximal Policy Optimization (PPO)

---

## 🤖 AI Agents (LangChain)

### Market Data Agent
- Real-time market analysis
- Stock recommendations
- Market sentiment analysis

### Risk Analysis Agent
- Risk profile assessment
- Personalized risk recommendations
- Investment strategy suggestions

### Investment Advisor Agent
- Personalized investment recommendations
- Asset allocation suggestions
- Goal-based planning

### Loan Optimization Agent
- Prepayment strategies
- EMI optimization
- Refinancing recommendations

---

## 🔌 API Endpoints

### Income Endpoints
```
POST   /api/income                    - Create income record
GET    /api/income/{user_id}         - Get all incomes
GET    /api/income/{user_id}/{month} - Get income for specific month
```

### Expense Endpoints
```
POST   /api/expense                  - Create expense
GET    /api/expense/{user_id}       - Get all expenses
GET    /api/expense/{user_id}/{month} - Get expenses for month
```

### Stock Endpoints
```
POST   /api/stock                    - Add stock
GET    /api/stock/{user_id}         - Get portfolio
PUT    /api/stock/{id}/price        - Update price
```

### SIP Endpoints
```
POST   /api/sip                      - Create SIP
GET    /api/sip/{user_id}           - Get SIPs
PUT    /api/sip/{id}/values         - Update values
```

### Loan Endpoints
```
POST   /api/loan                     - Create loan (EMI auto-calculated)
GET    /api/loan/{user_id}          - Get loans
PUT    /api/loan/{id}/outstanding   - Update outstanding
```

### Insurance Endpoints
```
POST   /api/insurance                - Create policy
GET    /api/insurance/{user_id}     - Get policies
```

### Net Worth Endpoints
```
GET    /api/net-worth/{user_id}            - Get history
GET    /api/net-worth/{user_id}/latest     - Get latest
POST   /api/net-worth/snapshot             - Calculate snapshot
```

For complete API docs, visit: **http://localhost:8000/docs**

---

## 📊 Database Schema

### Users Table
```sql
id, email, name, password_hash, created_at, updated_at
```

### Income Table
```sql
id, user_id, month, salary, other_income, other_income_source, total_income
```

### Expense Table
```sql
id, user_id, month, category, amount, description, is_anomaly
```

### Stock Table
```sql
id, user_id, company_name, symbol, quantity, purchase_price, purchase_date, 
current_price, current_value, last_updated
```

### SIP Table
```sql
id, user_id, fund_name, monthly_amount, start_date, expected_return_rate, 
total_invested, current_value, is_active
```

### Loan Table
```sql
id, user_id, loan_type, principal_amount, interest_rate, tenure_months, 
emi, outstanding_amount, start_date, is_active
```

### Insurance Table
```sql
id, user_id, insurance_type, policy_name, policy_number, premium_amount, 
premium_frequency, coverage_amount, tenure_years, start_date, 
maturity_date, is_active
```

### NetWorthHistory Table
```sql
id, user_id, month, total_assets, total_liabilities, net_worth, 
predicted_next_month, created_at
```

---

## 🔐 Security Notes

1. **Change default passwords** in .env file
2. **Use environment variables** for sensitive data
3. **Enable SQL injection protection** via SQLAlchemy ORM
4. **Validate all inputs** with Pydantic schemas
5. **Hash passwords** before storing (when adding authentication)
6. **Use HTTPS** in production
7. **Implement rate limiting** for API endpoints

---

## 🐛 Troubleshooting

### MySQL Connection Error
```bash
# Check if MySQL is running
brew services list

# Start MySQL if stopped
brew services start mysql

# Verify credentials in .env
```

### Port Already in Use
```bash
# Change ports in code or kill existing process
lsof -i :8000  # FastAPI
lsof -i :8501  # Streamlit
kill -9 <PID>
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +
```

### OpenAI API Errors
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Verify key in .env file
grep OPENAI_API_KEY .env
```

---

## 📈 Performance Tips

1. **Index frequently queried columns** in MySQL
2. **Cache API responses** using Redis (optional)
3. **Batch insert data** for large uploads
4. **Use LIMIT** in API queries to avoid overload
5. **Train ML models** with sufficient data (3+ months)
6. **Enable query logging** to identify slow queries

---

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
python -m uvicorn backend.main:app --reload
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 backend.main:app
```

### Docker Deployment
```bash
docker build -t finance-app .
docker run -p 8000:8000 -p 8501:8501 finance-app
```

### Cloud Deployment
- **Frontend:** Deploy Streamlit to Streamlit Cloud
- **Backend:** Deploy to Heroku, AWS, GCP, or DigitalOcean
- **Database:** Use managed MySQL services (AWS RDS, Azure Database)

---

## 📞 Support

For issues or questions:
1. Check existing GitHub issues
2. Review API documentation at `/docs`
3. Check application logs
4. Review console output for error messages

---

## 📝 Contributing

To add new features:
1. Create a new branch: `git checkout -b feature-name`
2. Make changes following the project structure
3. Test thoroughly before committing
4. Submit a pull request with description

---

## 📄 License

MIT License - Feel free to use for personal and commercial projects

---

**Happy investing! 📈**
