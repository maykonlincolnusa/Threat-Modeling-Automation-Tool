import os

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Threat Modeling Dashboard", layout="wide")
st.title("Threat Modeling Automation Dashboard")

api_port = os.getenv("API_GATEWAY_PORT", "8000")
api_url = f"http://api-gateway:{api_port}"

viewer_user = os.getenv("DASHBOARD_GATEWAY_USER", "viewer")
viewer_password = os.getenv("DASHBOARD_GATEWAY_PASSWORD", "viewer123")


def get_token() -> str | None:
    try:
        resp = requests.post(
            f"{api_url}/auth/token",
            json={"username": viewer_user, "password": viewer_password},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception:
        return None


def get_overview(token: str | None) -> dict:
    if not token:
        return {"assets_count": 0, "threats_count": 0, "ml_service": {"status": "auth_failed"}}

    try:
        resp = requests.get(
            f"{api_url}/v1/overview",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {"assets_count": 0, "threats_count": 0, "ml_service": {"status": "unavailable"}}


access_token = get_token()
overview = get_overview(access_token)

col1, col2, col3 = st.columns(3)
col1.metric("Assets", overview.get("assets_count", 0))
col2.metric("Threats", overview.get("threats_count", 0))
col3.metric("ML Service", overview.get("ml_service", {}).get("status", "unknown"))

st.subheader("Sample Threat Pipeline")
rows = [
    {"stage": "Discovery", "status": "ok"},
    {"stage": "Threat Classification", "status": "ok"},
    {"stage": "Mitigation Plan", "status": "pending"},
]
st.dataframe(pd.DataFrame(rows), use_container_width=True)
