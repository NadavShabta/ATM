# ATM System - REST API

## Project Overview
This project implements a server-side ATM system that provides essential banking functionalities, including:
- Retrieving account balance via a GET request.
- Withdrawing funds via a POST request.
- Depositing funds via a POST request.

The system is designed with a structured, modular architecture using Flask and SQLAlchemy, leveraging SQLite in-memory mode for fast and ACID-compliant transactions. The API is deployed on **Heroku**, ensuring accessibility and ease of testing.

---

## Tech Stack
- **Backend Framework:** Flask (Python)
- **Database:** SQLite (In-Memory) using SQLAlchemy ORM
- **Deployment:** Heroku
- **Concurrency Handling:** Python `threading.Lock()`, SQLAlchemy row-level locking (`WITH FOR UPDATE`)
- **Testing:** Pytest

---

## Deployment
The API is deployed on Heroku and accessible at:

**Live API URL:**  
[https://atm-441f2ec56b85.herokuapp.com/](https://atm-441f2ec56b85.herokuapp.com/)

---

## Project Structure
The project follows a structured three-layered architecture:
- **`app/routes/`** – Defines API endpoints using Flask Blueprint.
- **`app/services/`** – Implements business logic for transactions and account management.
- **`app/data_access/`** – Handles database interactions using SQLAlchemy.
- **`app/models.py`** – Defines the database schema for accounts and transactions.
- **`app/utils.py`** – Includes validation, error handling, and logging utilities.
- **`config/config.py`** – Contains application configuration settings.
- **`db_setup.py`** – Initializes the database and populates sample accounts.
- **`run.py`** – The entry point for running the application.
- **`requirements.txt`** – Lists all required dependencies.
- **`Procfile`** – Configures deployment for Heroku.
- **`tests/`** – Contains unit tests for API and database operations.
- **`README`** – Documentation explaining the project.

---

## Setup & Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/NadavShabta/ATM-System.git
cd ATM-System 
```

### Step 2: Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
Copy
pip install -r requirements.txt
```
### Step 4: Run the Application
```bash
Copy
python run.py
```
```
The API will be available at `http://127.0.0.1:5000/`.

```



## API Endpoints

### 1️⃣ Retrieve Account Balance

- **Endpoint:** `GET /accounts/{account_number}/balance`
- **Description:** Fetches the current balance of the account.
- **Example Request:**
```bash
curl -X GET "http://127.0.0.1:5000/accounts/10001/balance"
```

- **Response:**
```json
{
    "success": true,
    "data": {
        "account_number": "10001",
        "balance": 5000.0
    },
    "code": 200
}
```
- **Error Cases:**
  - 404 Not Found – Account does not exist.
  - 400 Bad Request – Invalid account format.

---

### 2️⃣ Withdraw Money

- **Endpoint:** `POST /accounts/{account_number}/withdraw`
- **Description:** Withdraws a specified amount from the account.
- **Request Body:**
```json
{
    "amount": 100.0
}
```
- **Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/accounts/10001/withdraw" -H "Content-Type: application/json" -d '{"amount": 100.0}'
```
- **Response:**
```json
{
    "success": true,
    "data": {
        "account_number": "10001",
        "new_balance": 4900.0
    },
    "code": 200
}
```
- **Error Cases:**
  - 400 Bad Request – Invalid amount format.
  - 404 Not Found – Account does not exist.
  - 400 Bad Request – Insufficient funds.

---

### 3️⃣ Deposit Money

- **Endpoint:** `POST /accounts/{account_number}/deposit`
- **Description:** Deposits a specified amount into the account.
- **Request Body:**
```json
{
    "amount": 200.0
}
```
- **Example Request:**
```bash
curl -X POST "http://127.0.0.1:5000/accounts/10001/deposit" -H "Content-Type: application/json" -d '{"amount": 200.0}'
```
- **Response:**
```json
{
    "success": true,
    "data": {
        "account_number": "10001",
        "new_balance": 5200.0
    },
    "code": 200
}
```
- **Error Cases:**
  - 400 Bad Request – Invalid amount format.
  - 404 Not Found – Account does not exist.

---

## Approach and Design Decisions

### 1️⃣ API Framework Choice: Flask vs. FastAPI

The choice between **Flask** and **FastAPI** was based on various factors:

| Criteria              | Flask  | FastAPI |
|----------------------|--------|---------|
| **Performance**      | Sync-based, slightly slower | Async-based, significantly faster |
| **Ease of Use**      | Simple, widely used | Slightly steeper learning curve |
| **Community Support** | Large ecosystem | Growing but smaller community |
| **Built-in Validation** | Manual validation needed | Automatic data validation |
| **SQLAlchemy Integration**| Excellent support | Requires async drivers |

**Why Flask?**
- Flask’s synchronous nature aligns well with SQLAlchemy, which does not fully support async operations.
- Flask has a mature ecosystem and strong community support.
- Simplicity and flexibility make it an excellent fit for a transactional API.

---

### 2️⃣ Three-Layered Architecture

The system is structured into **three distinct layers**:
1. **API Layer (Flask Routes)**
   - Handles HTTP requests & responses.
   - Validates incoming data.
   - Formats JSON responses.
2. **Service Layer (Business Logic)**
   - Implements account operations.
   - Ensures concurrency safety.
   - Validates withdrawal and deposit rules.
3. **Data Access Layer (SQLAlchemy ORM)**
   - Manages transactions and database interactions.
   - Implements row-level locking for safe concurrent transactions.

This architecture ensures **scalability, reusability, and maintainability**.

---

### 3️⃣ Database Design: SQLite (In-Memory Mode)

Using **SQLite in-memory mode** offers:
- **ACID Compliance** – Ensures atomic, consistent, and durable transactions.
- **Relational Integrity** – Supports primary/foreign keys and constraints.
- **Faster Execution** – No disk writes; all operations occur in RAM.

This design was chosen due to **Heroku’s free-tier limitations** (no persistent database support). While **SQLite is not ideal for high concurrency**, I implemented additional **thread-based locking** to ensure transactional safety.

---

## Challenges Faced & Solutions

### 1️⃣ Handling Data Persistence on Heroku

**Problem:**  
Heroku resets data on each deployment since the free plan does not support persistent databases.  
**Solution:**  
- Using SQLite in-memory with SQLAlchemy ORM for transactions.
- Ensuring all data operations remain consistent within each session.

---

### 2️⃣ Handling Race Conditions in Concurrent Withdrawals

**Problem:**  
Multiple users withdrawing simultaneously can cause incorrect balances.  
**Solution:**  
- **Row-level locking (`WITH FOR UPDATE`)** to prevent concurrent modifications.
- **Global `threading.Lock()`** to control access to shared resources.
- **Retry mechanism** for failed transactions due to locking.

---

### 3️⃣ Error Handling and Response Standardization

Implemented structured error handling with:
- **400 Bad Request** – Invalid input.
- **404 Not Found** – Account does not exist.
- **405 Method Not Allowed** – Incorrect HTTP method.
- **415 Unsupported Media Type** – Missing JSON request body.
- **500 Internal Server Error** – Unexpected system failures.

---

## Running Tests

Unit tests ensure the correctness of:
- API response validation.
- Database transaction safety.
- Concurrent withdrawal handling.

Run all tests using:
```bash
pytest
```

---

## Conclusion

This ATM system provides:
✅ A modular and scalable architecture.  
✅ Secure transaction handling with race condition prevention.  
✅ Robust API with proper error handling.

**GitHub Repository:** [YOUR_GITHUB_REPO_URL]  
**Live API:** https://atm-441f2ec56b85.herokuapp.com/
