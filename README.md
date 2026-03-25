# Humanize AI

A Streamlit app to refine AI text into more natural writing, with local fallbacks when external APIs are unavailable.

## Run locally

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Optional API keys

You can provide keys in any of these places:
- Sidebar inputs (runtime)
- `.streamlit/secrets.toml`
- Environment variables

```toml
GEMINI_API_KEY = "your_key"
SAPLING_API_KEY = "your_key"
```

## Deploy (Streamlit Community Cloud)

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set `main.py` as the entry point.
4. Add optional secrets in App Settings → Secrets.
5. Deploy and verify `/` loads and both Humanizer + AI Detector tabs work.
