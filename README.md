# Rivyou Product Search Platform

A production-ready **Django REST Framework** backend application developed for the **Rivyou Backend Engineer Internship Assignment**.

The project provides secure JWT authentication, product management APIs, intelligent relevance-based product search, typo correction using RapidFuzz, CSV data import, and interactive Swagger documentation.

---

## Features

- JWT Authentication (Register, Login, Logout)
- Product CRUD APIs
- Category-wise Product Listing
- Intelligent Product Search
- Relevance-based Search Ranking
- RapidFuzz Typo Correction
- CSV Product Import Command
- Pagination Support
- Swagger (OpenAPI) Documentation
- Unit Tests
- SQLite Database (Development)

---

## Tech Stack

- Python 3.13
- Django
- Django REST Framework
- SQLite
- Simple JWT
- RapidFuzz
- drf-spectacular (Swagger/OpenAPI)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rivyou-assignment
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Import Product Dataset

```bash
python manage.py import_products products_data.csv
```

This command imports all unique products from the CSV file while automatically skipping duplicate records.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Server URL:

```
http://127.0.0.1:8000/
```

---

## Authentication

The project uses **JWT Authentication**.

All protected endpoints require the following header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

---

## API Endpoints

### Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive JWT tokens |
| POST | `/api/auth/logout/` | Logout and blacklist refresh token |

---

### Product APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/<id>/` | Retrieve a product |
| POST | `/api/products/` | Create a product |
| PUT | `/api/products/<id>/` | Update a product |
| DELETE | `/api/products/<id>/` | Delete a product |
| GET | `/api/products/category/<category_name>/` | List products by category |

---

### Search API

```
GET /api/products/search/?q=<query>
```

Example:

```
GET /api/products/search/?q=smartphone
```

Supports:

- Case-insensitive search
- Partial matching
- Pagination
- RapidFuzz typo correction

Example typo correction:

```
smartphne → smartphone
iphon → iphone
```

---

## Search Ranking

Search results are ranked according to the following priority:

1. Category Match (Highest Priority)
2. Tag Match
3. Product Name Match
4. Product Description Match

This ensures that products belonging to the searched category are always returned before products that only contain the search keyword in their tags, name, or description.

---

## Swagger Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

## Running Tests

Run the test suite:

```bash
pytest
```

The test suite covers:

- User Registration
- User Login
- User Logout
- Product CRUD Operations
- CSV Import
- Search Ranking Logic

---

## Project Structure

```
rivyou_search/
│
├── authentication/
├── products/
├── tests/
├── rivyou_search/
├── manage.py
├── products_data.csv
├── requirements.txt
├── README.md
├── Rivyou_Postman_Collection.json
└── pytest.ini
```

---

## Assignment Completion

- ✅ JWT Authentication
- ✅ User Registration
- ✅ User Login
- ✅ User Logout
- ✅ Product CRUD APIs
- ✅ Category API
- ✅ Search API
- ✅ Relevance-based Ranking
- ✅ RapidFuzz Typo Correction
- ✅ CSV Import Management Command
- ✅ Swagger Documentation
- ✅ Pagination
- ✅ Unit Tests
- ✅ Postman Collection

---

## License

This project was developed solely for the **Rivyou Backend Engineer Internship Assignment**.