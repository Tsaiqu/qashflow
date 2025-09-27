# Smart Budget Manager

The Smart Budget Manager is a FastAPI-based web application designed to help you track your income and expenses, gain insights into your spending habits, and make smarter financial decisions. It features a machine learning-powered category prediction system that automatically suggests categories for your transactions, making it easier than ever to manage your budget.

## Features

- **Transaction Tracking**: Record your income and expenses with ease.
- **ML-Powered Category Prediction**: Automatically suggests categories for new transactions based on their names.
- **Financial Summaries**: Get a clear overview of your financial health with summaries of your income and expenses.
- **Spending Analysis**: Analyze your spending by category to see where your money is going.
- **Monthly Breakdowns**: Track your financial progress with detailed monthly summaries.
- **Spending Forecasts**: Get a simple forecast of your spending for the next month based on your historical data.

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/smart-budget-manager.git
   cd smart-budget-manager
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Import sample data:**

   The repository includes a sample CSV file with transaction data to get you started. You can import it into the database by running:

   ```bash
   python import_csv.py data/transactions.csv
   ```

4. **Train the machine learning model:**

   To enable the category prediction feature, you need to train the model using the sample data:

   ```bash
   python ml/train.py
   ```

5. **Run the application:**

   ```bash
   uvicorn main:app --reload
   ```

   The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

- `GET /`: Returns a welcome message.
- `POST /transactions/`: Creates a new transaction.
- `GET /transactions/`: Lists all transactions.
- `GET /summary/`: Returns a summary of total income and expenses.
- `GET /summary/by_category`: Returns a summary of spending by category.
- `GET /summary/monthly`: Returns a monthly summary of income and expenses.
- `GET /forecast/spending`: Provides a spending forecast for the next month.
- `GET /predict_category`: Predicts the category of a transaction based on its name.

## Docker

You can also run the application using Docker. First, build the Docker image:

```bash
docker build -t smart-budget-manager .
```

Then, run the container:

```bash
docker run -p 8000:8000 smart-budget-manager
```