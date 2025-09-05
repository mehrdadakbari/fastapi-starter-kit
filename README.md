# FastAPI Starter Kit

⚡ A FastAPI starter kit with clean project layout, MongoDB integration, JWT authentication, user CRUD, and advanced logging configuration.

---

## Features

- 📂 **Clean project layout** — organized for scalability
- 📝 **Advanced logging** — color console + JSON format
- 👤 **User CRUD** — create, read, update, delete users
- 🔑 **JWT authentication** — secure login with access tokens
- 🍃 **MongoDB integration** — easy configuration and usage

---

## Project Structure

```bash
fastapi-starter-kit/
├── app/
│   ├── core/             # Core config (logging, settings, database)
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   └── __init__.py
│   ├── dtos/             # api responses
│   │   ├── user.py
│   ├── models/           # Database models
│   │   ├── user.py
│   ├── schemas/          # Pydantic schemas (DTOs)
│   │   ├── user.py
│   ├── repositories/
│   ├── routes/
│   ├── services/
│   ├── main.py           # FastAPI entry point
│   └── __init__.py
├── requirements.txt      # Python dependencies
└── README.md
```
