# Full-Stack Calculator App with FastAPI & TiDB Cloud

A full-stack web calculator built with a decoupled architecture. A lightweight HTML5/CSS3/JavaScript client talks to a **FastAPI** backend that evaluates operations and stores an audit trail of every calculation in a managed **TiDB Cloud** (MySQL-compatible) database through **SQLAlchemy**.

---

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [API Reference](#api-reference)
- [License](#license)

---

## Architecture

```text
┌──────────────────┐        HTTP / JSON         ┌───────────────────┐
│                  │  POST /calculate           │                   │
│  Frontend Client │ ─────────────────────────> │  FastAPI Backend  │
│  (HTML/CSS/JS)   │ <───────────────────────── │  (Python 3.10+)   │
│                  │  GET /history              │                   │
└──────────────────┘                            └─────────┬─────────┘
                                                          │
                                              SQLAlchemy + PyMySQL
                                                    (TLS)
                                                          │
                                                          v
                                                ┌───────────────────┐
                                                │    TiDB Cloud     │
                                                │  (Managed MySQL)  │
                                                └───────────────────┘
```

---

## Features

- **Core arithmetic engine** – addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`) and exponentiation (`^`).
- **Division-by-zero protection** – the API validates input and responds with `400 Bad Request` for invalid operations.
- **Persistent cloud history** – each calculation (operands, operator, result and UTC timestamp) is saved to TiDB Cloud.
- **RESTful endpoints** – create a calculation, list recent history, and clear all history.
- **Interactive API docs** – Swagger UI and ReDoc are generated automatically by FastAPI.
- **Secure configuration** – database credentials are loaded from environment variables via `python-dotenv`.

---

## Tech Stack

| Layer          | Technology                                      |
| -------------- | ----------------------------------------------- |
| Backend        | FastAPI, Uvicorn                                |
| ORM / Driver   | SQLAlchemy, PyMySQL, Cryptography               |
| Validation     | Pydantic                                        |
| Database       | TiDB Cloud (Serverless, MySQL-compatible)       |
| Frontend       | HTML5, CSS3, JavaScript (Fetch API)             |

---

## Project Structure

```text
.
├── .gitignore               # Excludes secrets, caches and virtual environments
├── README.md                # Project documentation
│
├── Backend/
│   ├── .env                 # Database credentials (untracked)
│   ├── database.py          # SQLAlchemy engine, connection pooling, session factory
│   ├── main.py              # FastAPI app, CORS middleware and routes
│   ├── models.py            # Database table definitions
│   ├── schemas.py           # Pydantic request/response schemas
│   └── requirements.txt     # Python dependencies
│
└── Frontend/
    └── index.html           # Calculator UI and asynchronous API client
```

---

## Getting Started

### Prerequisites

- Python **3.10** or higher
- A MySQL-compatible database: either a local MySQL instance or a free [TiDB Cloud](https://tidbcloud.com/) Serverless cluster
- Git

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd "Calculator App with API"
   ```

2. **Create a virtual environment** inside the backend directory

   ```bash
   cd Backend
   python -m venv .venv
   ```

3. **Activate the virtual environment**

   - Windows (PowerShell):

     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

   - Linux / macOS:

     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**

   Create a `.env` file inside the `Backend/` directory:

   ```ini
   DATABASE_URL=mysql+pymysql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>?ssl_verify_cert=true&ssl_verify_identity=true
   ```

   | Placeholder  | Description                                                      |
   | ------------ | ---------------------------------------------------------------- |
   | `<USER>`     | Database username                                                |
   | `<PASSWORD>` | Database password (URL-encode special characters)                |
   | `<HOST>`     | Cluster hostname (shown in the TiDB Cloud **Connect** dialog)    |
   | `<PORT>`     | Port number (TiDB Cloud Serverless uses `4000`)                  |
   | `<DATABASE>` | Target database name (e.g. `test`)                               |

---

## Running the Application

### 1. Start the FastAPI server

From the `Backend/` directory, with the virtual environment active:

```bash
uvicorn main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.

| Resource          | URL                              |
| ----------------- | -------------------------------- |
| Swagger UI        | http://127.0.0.1:8000/docs       |
| ReDoc             | http://127.0.0.1:8000/redoc      |

### 2. Launch the client

Open `Frontend/index.html` directly in any modern browser, or serve it with a simple HTTP server:

```bash
cd ../Frontend
python -m http.server 3000
```

Then visit <http://localhost:3000>.

> Make sure the API base URL used in `index.html` points to your running backend (by default `http://127.0.0.1:8000`).

---

## API Reference

| Method   | Endpoint     | Description                                                          |
| -------- | ------------ | -------------------------------------------------------------------- |
| `POST`   | `/calculate` | Evaluates an arithmetic operation and stores the record.             |
| `GET`    | `/history`   | Returns recent calculation records, newest first.                    |
| `DELETE` | `/history`   | Deletes all calculation records from the database.                   |

### `POST /calculate`

**Request body**

```json
{
  "num1": 15,
  "num2": 3,
  "operation": "/"
}
```

**Supported operations:** `+`, `-`, `*`, `/`, `^`

**Response** – `201 Created`

```json
{
  "id": 1,
  "num1": 15.0,
  "num2": 3.0,
  "operation": "/",
  "result": 5.0,
  "timestamp": "2026-10-09T07:10:00Z"
}
```

**Error responses**

| Status | Meaning                                                        |
| ------ | -------------------------------------------------------------- |
| `400`  | Invalid operation, such as division by zero.                   |
| `422`  | Request body failed validation (missing or wrongly typed fields). |

### `GET /history`

Returns a JSON array of past calculations, newest first.

### `DELETE /history`

Removes every stored calculation record.

---


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
