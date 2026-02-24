import os
from dotenv import load_dotenv

load_dotenv()

TDX_CLIENT_ID: str = os.getenv("TDX_CLIENT_ID", "")
TDX_CLIENT_SECRET: str = os.getenv("TDX_CLIENT_SECRET", "")
USE_MOCK: bool = os.getenv("USE_MOCK", "false").lower() == "true"

TDX_AUTH_URL = "https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
TDX_BASE_URL = "https://tdx.transportdata.tw/api/basic/v2/Bus"
CITY = "Kaohsiung"


def is_tdx_configured() -> bool:
    """檢查 TDX API 金鑰是否已設定"""
    return bool(TDX_CLIENT_ID and TDX_CLIENT_SECRET and
                TDX_CLIENT_ID != "your_client_id_here" and
                TDX_CLIENT_SECRET != "your_client_secret_here")
