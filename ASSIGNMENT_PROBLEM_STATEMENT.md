# Backend Engineer Assignment - Rivyou Product Search Platform

**Position:** Back-End Developer Intern (Django)  

---

## Overview

You're building a **product search API** for Rivyou's discovery platform. The challenge? Users are searching for specific product categories (e.g., "smartphones"), but the data is messy: back covers and chargers might have "smartphone" tagged on them for marketing reasons. Your job is to build a backend that **returns the right product first**, not just any product that matches a keyword.

This assignment tests:
1. **Authentication** — Secure API access with login/logout
2. **Database operations** — Read and filter structured data efficiently
3. **Search logic** — Rank results by relevance (category match > tag match > description match)
4. **API design** — Clean, RESTful endpoints with proper error handling

---

## The Problem

### Background
You have a dataset of 1,000 products across three categories:
- **Smartphones** (330 units)
- **Chargers** (335 units)
- **Back Covers** (335 units)

**The Catch:** ~100 chargers and back covers have been tagged with "smartphone" for marketing purposes. When a user searches for "smartphone," your API should be smart enough to:
1. Rank **actual smartphones first**
2. Then show chargers/covers that mention smartphones only if needed
3. Avoid confusing the user with irrelevant products

### Data Schema
Each product record contains:
```
id              | product_name           | product_description              | category      | tags
1               | iPhone 15 Pro Variant 0 | High-performance flagship device | Smartphones   | 5g,camera,performance
...
450             | USB-C Charger Model 1   | Fast and reliable charging...    | Chargers      | fast-charging,portable,smartphone
```

**Download the dataset:** `products_data.csv` (included)

---

## Assignment Tasks

### Task 1: Authentication System
Build a simple JWT-based authentication layer.

**Endpoints:**
- `POST /api/auth/register` — Register a new user
  - Input: `{"username": "string", "email": "string", "password": "string"}`
  - Output: `{"id": "int", "username": "string", "token": "jwt"}`
  - Validation: Email format, password strength (minimum 8 chars)

- `POST /api/auth/login` — Login and get JWT token
  - Input: `{"username": "string", "password": "string"}`
  - Output: `{"token": "jwt", "user": {"id": "int", "username": "string"}}`
  - Error handling: Invalid credentials → 401

- `POST /api/auth/logout` — Logout (token invalidation)
  - Input: JWT token in header
  - Output: `{"message": "Logged out successfully"}`

**Requirements:**
- Hash passwords (use `django.contrib.auth.hashers` or `bcrypt`)
- Use JWT for stateless authentication
- Token expiry: 7 days
- All protected endpoints require valid JWT in `Authorization: Bearer <token>` header

---

### Task 2: Product Search API (The Core Challenge)

Build a **relevance-ranked search endpoint** that returns products intelligently.

**Endpoint:**
- `GET /api/products/search?q=<query>&limit=20` — Search products (Protected)
  - Input: 
    - `q` (string, required) — Search query
    - `limit` (int, optional, default=20) — Number of results
    - `category_filter` (string, optional) — Filter by category (e.g., "Smartphones")
  - Output: List of products ranked by relevance

**Relevance Ranking Logic** (Most Important):

Implement a **three-tier ranking system**:

1. **Tier 1 (Highest):** Products where `category` matches the query
   - Example: Query "smartphone" → All products with `category == "Smartphones"` ranked here
   - Sub-sort: By matching tags count (more tags = higher rank)

2. **Tier 2 (Medium):** Products where tags contain the query term (but category doesn't match)
   - Example: Query "smartphone" → Chargers/BackCovers with "smartphone" tag
   - Sub-sort: By tag match quality (exact tag match > partial match)

3. **Tier 3 (Lowest):** Products where product_name or description contains the query
   - Example: Query "pro" → Products like "iPhone 15 Pro" appear here

**Example Output:**
```json
{
  "query": "smartphone",
  "total_results": 430,
  "results": [
    {
      "id": 5,
      "product_name": "Samsung Galaxy S24 Variant 3",
      "category": "Smartphones",
      "tags": ["5g", "camera", "performance"],
      "relevance_score": 0.95,
      "rank_reason": "Category match"
    },
    {
      "id": 10,
      "product_name": "iPhone 15 Pro Variant 7",
      "category": "Smartphones",
      "tags": ["5g", "fast-charging", "battery"],
      "relevance_score": 0.93,
      "rank_reason": "Category match"
    },
    {
      "id": 450,
      "product_name": "USB-C Fast Charger Model 1",
      "category": "Chargers",
      "tags": ["fast-charging", "portable", "smartphone"],
      "relevance_score": 0.55,
      "rank_reason": "Tag match (smartphone)"
    }
  ]
}
```

**Requirements:**
- ✓ Must return Tier 1 results first, always
- ✓ Implement a relevance scoring system (0.0 to 1.0)
- ✓ Support case-insensitive search
- ✓ Partial matching (e.g., "phone" matches "smartphone")
- ✓ Return empty results gracefully
- ✓ Pagination support (optional but nice to have)

---

### Task 3: Additional CRUD Operations (Supporting)

**Endpoints:**
- `GET /api/products/:id` — Get a single product by ID (Protected)
- `GET /api/products/category/<category>` — List all products in a category (Protected)
- `POST /api/products` — Create a new product (Protected, Admin only - optional)
  - Input: `{"product_name": "string", "description": "string", "category": "string", "tags": ["array"]}`

---

## Technical Requirements

### Stack [Preferred]
- **Backend Framework:** Django + Django REST Framework
- **Database:** PostgreSQL (primary) + optional MongoDB for logs
- **Authentication:** JWT (use `djangorestframework-simplejwt` or similar)
- **Async:** Celery + Redis (or Django-RQ as simpler alternative)
- **API Documentation:** Django REST Swagger or similar

### Code Quality
- ✓ Clean, modular code with proper separation of concerns
- ✓ Error handling with meaningful HTTP status codes (400, 401, 404, 500)
- ✓ Input validation and sanitization
- ✓ Unit tests for search ranking logic (aim for >80% coverage on core logic)
- ✓ Database indexes on frequently queried fields (`category`, `tags`)

### Deployment
- Vercel or Demo during Interview

---

## Deliverables

1. **Django Project** with:
   - Complete app structure (`/api/users`, `/api/products`, `/api/analytics`)
   - Models, serializers, views, URLs
   - Authentication middleware
   - Search ranking algorithm

2. **Database Setup:**
   - Load `products_data.csv` into PostgreSQL via a Django management command
   - Create necessary indexes, if needed.

3. **Tests: OPTIONAL** 
   - test cases for search ranking
   - Authentication tests
   - Example: "Searching for 'smartphone' returns actual smartphones before chargers"

4. **Optional but Impressive:**
   - Implement fuzzy matching for typos ("smartphne" → "smartphone")
   - Add search history per user
   - Pagination with cursor-based optimization
   - Caching strategy for frequent searches

---

## Questions?

- Focus on **ranking logic** — this is the hardest and most important part
- Don't over-engineer; clean code beats fancy features
- If stuck on async, implement synchronous logging first, then refactor
- Reach out if the problem statement needs clarification

**Good luck!**
