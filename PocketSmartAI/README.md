# PocketSmart AI

PocketSmart AI is a Generative AI powered budget and recommendation assistant.

The application supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional Jewelry Outfit Image
- Gemini AI
- Fallback recommendations
- User registration
- User login
- JWT authentication
- Recommendation history
- SQLite database
- FastAPI backend
- Jinja2 frontend
- Marketplace search links

---

## Project Structure

```text
PocketSmartAI/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── uploads/
├── tests/
│
└── app/
    ├── config.py
    ├── db.py
    ├── main.py
    ├── security.py
    ├── models/
    ├── routes/
    ├── services/
    ├── static/
    └── templates/