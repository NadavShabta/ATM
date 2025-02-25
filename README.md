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
# ATM System

## Table of Contents

{:toc}

---

## Project Overview

[Continue with the rest of your README content...]

---

## Tech Stack

[Continue with the rest of your README content...]

---

## Deployment

[Continue with the rest of your README content...]

---

## Project Structure

[Continue with the rest of your README content...]

---

## Setup & Installation

[Continue with the rest of your README content...]

---

## API Endpoints

[Continue with the rest of your README content...]

---

## Approach and Design Decisions

[Continue with the rest of your README content...]

---

## Challenges Faced & Solutions

[Continue with the rest of your README content...]

---

## Running Tests

[Continue with the rest of your README content...]

---

## Conclusion

[Continue with the rest of your README content...]

---

**Note:** The `{:toc}` is a Markdown extension to automatically generate a table of contents. However, not all Markdown parsers support this syntax. When using this in your `README.md`, ensure that the tool or platform you are using to render the Markdown supports this extension. If the platform does not support it, you can manually create the table of contents as you have done or use another Markdown extension or tool that supports automatic table of contents generation.

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
