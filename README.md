# AI Meeting Notes & Action Items Generator (Student Edition)

This is a complete, ready-to-run demo project that transcribes meeting audio,
retrieves supporting KB documents (RAG), summarizes into Key Points / Decisions /
Action Items, and can email the summary to a team.

The full project is packaged here. Quick start:

1. Create & activate a Python 3.11+ virtual environment.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set your SMTP creds (or use MailHog for dev).
4. Optionally run an Ollama server locally and pull a small instruct model:
   - `ollama pull llama3.1:8b-instruct`
   - Ollama typically listens at http://localhost:11434
5. `streamlit run app.py`

Files:
- app.py              -- Streamlit front-end
- utils/              -- helper modules (asr, rag, summarizer, emailer)
- kb/                 -- sample KB files for RAG
- requirements.txt    -- Python dependencies
- .env.example        -- sample environment variables
