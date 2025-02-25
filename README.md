
# ATM System 

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

## Sample Accounts

When the application is initialized, the database is pre-populated with the following sample accounts.

| Account Number | Balance (USD) |
|---------------|--------------|
| 10001         | 1000.0       |
| 10002         | 2000.0       |
| 10003         | 3000.0       |
| 10004         | 4000.0       |
| 10005         | 5000.0       |
| 10006         | 6000.0       |
| 10007         | 7000.0       |
| 10008         | 8000.0       |
| 10009         | 9000.0       |
| 100000        | 10000.0      |

These accounts can be used for testing the API endpoints during development and demonstration purposes.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Deployment](#deployment)
4. [Project Structure](#project-structure)
5. [Setup & Installation](#setup--installation)
6. [API Endpoints](#api-endpoints)
7. [Approach and Design Decisions](#approach-and-design-decisions)
8. [Challenges Faced & Solutions](#challenges-faced--solutions)
9. [Running Tests](#running-tests)
10. [Conclusion](#conclusion)

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
in case you missed
When the application is initialized, the database is pre-populated with the following sample accounts.

| Account Number | Balance (USD) |
|---------------|--------------|
| 10001         | 1000.0       |
| 10002         | 2000.0       |
| 10003         | 3000.0       |
| 10004         | 4000.0       |
| 10005         | 5000.0       |
| 10006         | 6000.0       |
| 10007         | 7000.0       |
| 10008         | 8000.0       |
| 10009         | 9000.0       |
| 100000        | 10000.0      |

These accounts can be used for testing the API endpoints during development and demonstration purposes.


with curl
---

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


## with Postman


### 1️⃣ Retrieve Account Balance

- **Endpoint:** `GET /accounts/{account_number}/balance`
- **Description:** Fetches the current balance of the account.
- **Example Request using Postman:**
  - Open Postman and create a GET request.
  - Set the URL to: `http://127.0.0.1:5000/accounts/10001/balance`
  - Click "Send".
  
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

### 2️⃣ Withdraw Money

- **Endpoint:** `POST /accounts/{account_number}/withdraw`
- **Description:** Withdraws a specified amount from the account.
- **Example Request using Postman:**
  - Open Postman and create a POST request.
  - Set the URL to: `http://127.0.0.1:5000/accounts/10001/withdraw`
  - Go to the Body tab, select "raw", and set data type to JSON.
  - Enter the JSON payload: `{"amount": 100.0}`
  - Click "Send".
  
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

### 3️⃣ Deposit Money

- **Endpoint:** `POST /accounts/{account_number}/deposit`
- **Description:** Deposits a specified amount into the account.
- **Example Request using Postman:**
  - Open Postman and create a POST request.
  - Set the URL to: `http://127.0.0.1:5000/accounts/10001/deposit`
  - Go to the Body tab, select "raw", and set data type to JSON.
  - Enter the JSON payload: `{"amount": 200.0}`
  - Click "Send".
  
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

These instructions provide details on how to use Postman to interact with each API endpoint. Make sure you replace `{account_number}` with the actual account number when testing the endpoints.


---

## Approach and Design Decisions

### General Approach

I designed this ATM system with a focus on **modularity, scalability, and maintainability**. The system is built using a **three-layered architecture**, ensuring a clear **separation of concerns**. Each layer—**API, Service, and Data Access**—has a distinct responsibility, making the codebase easier to understand, test, and extend. This approach aligns with the **Separation of Concerns (SoC)** principle, which is crucial for building robust and scalable applications.

### Key Concepts

#### Three-Layered Architecture:

**API Layer (Flask Routes)**
- Handles HTTP requests and responses.
- Validates incoming data.
- Formats JSON responses.

**Service Layer (Business Logic)**
- Implements the core logic for account operations.
- Ensures concurrency safety.
- Validates withdrawal and deposit rules.

**Data Access Layer (SQLAlchemy ORM)**
- Manages database interactions.
- Implements row-level locking for safe concurrent transactions.
- Ensures data consistency.

**Separation of Concerns (SoC)**
- Each layer has a specific mission, ensuring that the code is modular and easy to maintain.
- This separation also makes it easier to test individual components in isolation.

**Database Design**
- I chose **SQLite in-memory mode** with SQLAlchemy ORM to simulate a relational database. This approach provides **ACID compliance**, ensuring atomicity, consistency, isolation, and durability for financial transactions.
- While SQLite is not ideal for high-concurrency applications, I implemented additional safeguards to handle race conditions effectively.

### Design Decisions

**1️⃣ API Framework Choice: Flask vs. FastAPI**

When choosing between Flask and FastAPI, I considered several factors:

| Criteria          | Flask                               | FastAPI                             |
|-------------------|------------------------------------|--------------------------------------|
| Performance       | Sync-based, slightly slower         | Async-based, significantly faster    |
| Ease of Use      | Simple, widely used                | Slightly steeper learning curve     |
| Community Support | Large ecosystem                   | Growing but smaller community        |
| Built-in Validation| Manual validation needed            | Automatic data validation           |
| SQLAlchemy Integration | Excellent support                 | Requires async drivers             |

**Why Flask?**

- Flask’s synchronous nature aligns well with SQLAlchemy, which does not fully support async operations.
- Flask has a mature ecosystem and strong community support, making it easier to find resources and troubleshoot issues.
- Its simplicity and flexibility make it an excellent fit for a transactional API like this ATM system.

**2️⃣ Separation of Concerns (SoC)**

I prioritized Separation of Concerns throughout the project. By dividing the system into three distinct layers (API, Service, and Data Access), I ensured that each component has a single responsibility. This approach not only makes the codebase easier to maintain but also simplifies testing and debugging.

**3️⃣ Database Design: SQLite (In-Memory Mode)**

The choice of SQLite in-memory mode was driven by the need for a lightweight, fast, and ACID-compliant database. While SQLite is not typically used for high-concurrency applications, I implemented additional safeguards to handle race conditions effectively. Key benefits of this design include:

- **ACID Compliance**: Ensures atomic, consistent, isolated, and durable transactions.
- **Relational Integrity**: Supports primary/foreign keys and constraints, making it suitable for financial transactions.
- **Faster Execution**: All operations occur in RAM, eliminating disk I/O overhead.

This design was chosen due to **Heroku’s free-tier limitations** (no persistent database support). While **SQLite is not ideal for high concurrency**, I implemented additional **thread-based locking** to ensure transactional safety.


---

### Challenges Faced & Solutions

**1️⃣ Handling Data Persistence on Heroku**

**Problem:**  
Heroku resets data on each deployment since the free plan does not support persistent databases. This posed a significant challenge for maintaining data consistency across deployments.

**Solution:**  
I opted for SQLite in-memory mode with SQLAlchemy ORM, which allows the system to function as a relational database without requiring persistent storage.

To ensure data consistency, I implemented session-based transactions, ensuring that all operations remain consistent within each session.

**2️⃣ Handling Race Conditions in Concurrent Withdrawals**

**Problem:**  
Multiple users withdrawing funds simultaneously can lead to incorrect balances, especially in a multi-threaded environment. SQLite, while lightweight, is not inherently designed for high-concurrency applications.

**Solution:**  
Row-level locking (`WITH FOR UPDATE`): I used SQLite’s row-level locking mechanism to prevent concurrent modifications to the same account.

Global `threading.Lock()`: To further enhance concurrency safety, I implemented a global lock object to control access to shared resources.

Retry Mechanism: In cases where transactions fail due to locking, I added a retry mechanism to ensure that the operation eventually succeeds.

**3️⃣ Error Handling and Response Standardization**

To ensure a robust and user-friendly API, I implemented structured error handling with clear and consistent responses. The system handles various error cases, including:

- **400 Bad Request**: Invalid input or insufficient funds.
- **404 Not Found**: Account does not exist.
- **405 Method Not Allowed**: Incorrect HTTP method.
- **415 Unsupported Media Type**: Missing or invalid JSON request body.
- **500 Internal Server Error**: Unexpected system failures.

Proper error handling and standardized responses contribute to a more reliable API by providing clear feedback to the clients using the ATM system.


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

  
**Live API:** https://atm-441f2ec56b85.herokuapp.com/
```bash
have fun!
```

