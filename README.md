# ORBIT Health Monitor — hackathon prototype

A Streamlit prototype for astronaut self-monitoring during long-duration missions.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy free with Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py` and `requirements.txt` from this folder.
2. Visit https://share.streamlit.io/ and sign in with GitHub.
3. Choose **Create app**, select your repository, branch, and `app.py`.
4. Deploy. Your public app URL will look like `https://<app-name>.streamlit.app`.

Alternative: Railway can deploy the same repository; configure the start command:
`streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Important
This is a demonstration only. The dashboard starts with simulated values. The thresholds are illustrative, not NASA-approved clinical thresholds. Do not enter real personal health information or use it for medical decisions. A real system requires validated sensors, medical oversight, secure storage, privacy controls, and mission-specific clinical protocols.
