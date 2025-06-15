# 💳 Django Banking Application

A simple banking backend built with Django REST Framework. It supports user registration, automatic multi-currency bank account generation, account top-ups, user-to-user money transfers, and transaction history filtering.

## 🚀 Features

- 🔐 User Registration and Authentication
- 🏦 Automatic creation of  account: **GEL**
- 💸 Transfer money between users (same currency only)
- 💰 View balance per account
- 📜 View transactions with filters (sender, receiver, date, etc.)
- 📬 Swagger/OpenAPI documentation


## 📦 Tech Stack

- Python 3.9+
- Django 4+
- Django REST Framework
- SQLite (default, can be replaced with PostgreSQL)
- drf-yasg (Swagger UI for API)

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/banking-app.git
cd banking-app
```

### 2. Create Virtual Environment & Install Requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Run Server

```bash
python manage.py runserver
```

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register/` | Register new user |
| `POST` | `/api/login/` | Login with JWT |
| `POST` | `/api/transfer/` | Transfer money between users |
| `GET` | `/api/transactions/` | List transactions (with filters) |
| `GET` | `/api/transaction/?id=1` | Retrieve specific transaction |
| `GET` | `/api/balance/` | Get all account balances for user |

> Access Swagger docs at:  
> 📚 [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📌 TODOs

- Add support for currency exchange rates
- Add scheduled payments
- Add admin dashboard for account management

---

## 🧑‍💻 Author

- **Mirza Jijieshvili**  
  QA Engineer → Backend Developer  
  [LinkedIn](https://www.linkedin.com/in/mirza-jijieshvili/)

---

## 📄 License

This project is licensed under the MIT License.