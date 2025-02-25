Here is your **README.md** file with a **Table of Contents** at the beginning:

```md
# ATM System - REST API

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Deployment](#deployment)
4. [Project Structure](#project-structure)
5. [Setup & Installation](#setup--installation)
6. [API Endpoints](#api-endpoints)
    - [Retrieve Account Balance](#1️⃣-retrieve-account-balance)
    - [Withdraw Money](#2️⃣-withdraw-money)
    - [Deposit Money](#3️⃣-deposit-money)
7. [Executing API Calls with Postman](#executing-api-calls-with-postman)
8. [Approach and Design Decisions](#approach-and-design-decisions)
9. [Challenges Faced & Solutions](#challenges-faced--solutions)
10. [Running Tests](#running-tests)
11. [Conclusion](#conclusion)

---

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
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python run.py
```
The API will be available at `http://127.0.0.1:5000/`.

---

## API Endpoints

### 1️⃣ Retrieve Account Balance
- **Endpoint:** `GET /accounts/{account_number}/balance`
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

---

### 2️⃣ Withdraw Money
- **Endpoint:** `POST /accounts/{account_number}/withdraw`
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

---

### 3️⃣ Deposit Money
- **Endpoint:** `POST /accounts/{account_number}/deposit`
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

---

## Executing API Calls with Postman
1. **Open Postman**.
2. Select the **request type** (GET or POST).
3. Enter the **API URL** (e.g., `https://atm-441f2ec56b85.herokuapp.com/accounts/10001/balance`).
4. If using **POST**, navigate to the **Body** tab:
   - Select **raw**.
   - Choose **JSON** format.
   - Enter the request JSON:
   ```json
   {
       "amount": 500
   }
   ```
5. Click **Send** and view the response.

---

## Approach and Design Decisions
### API Framework Choice: Flask vs. FastAPI
The decision was based on factors like ecosystem support, ease of use, and SQLAlchemy integration. Flask was chosen due to its simplicity and compatibility with synchronous SQLAlchemy.

### Three-Layered Architecture
1. **API Layer** - Handles HTTP requests & responses.
2. **Service Layer** - Implements business logic.
3. **Data Access Layer** - Manages database transactions.

### Database Choice: SQLite (In-Memory)
- **ACID-compliant**
- **Fast execution**
- **Eliminates the need for external database services**

---

## Challenges Faced & Solutions

### Handling Data Persistence on Heroku
**Problem:**  
Heroku’s free plan resets data on each deployment.  
**Solution:**  
- Used SQLite in-memory with SQLAlchemy ORM.
- Ensured transactional consistency within the session.

### Handling Race Conditions in Withdrawals
**Problem:**  
Simultaneous withdrawals could cause incorrect balances.  
**Solution:**  
- **Row-level locking (`WITH FOR UPDATE`)**
- **Python `threading.Lock()`**
- **Retry mechanisms for failed transactions**

### Error Handling Standardization
Implemented structured error responses:
- `400 Bad Request` – Invalid input.
- `404 Not Found` – Account does not exist.
- `405 Method Not Allowed` – Incorrect HTTP method.
- `415 Unsupported Media Type` – Missing JSON request body.
- `500 Internal Server Error` – Unexpected issues.

---

## Running Tests
To ensure correctness, run all unit tests using:
```bash
pytest
```

---

## Conclusion
This ATM system provides:
✅ A modular and scalable architecture.  
✅ Secure transaction handling with race condition prevention.  
✅ Robust API with structured error handling.  

**GitHub Repository:** [https://github.com/NadavShabta/ATM-System](https://github.com/NadavShabta/ATM-System)  
**Live API:** [https://atm-441f2ec56b85.herokuapp.com/](https://atm-441f2ec56b85.herokuapp.com/)
```

This markdown file includes a **Table of Contents** for easy navigation. Now you can copy and upload it directly as your `README.md` file to GitHub! 🚀

