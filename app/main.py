"""
高雄公車即時到站查詢 API

Endpoint:
    GET /bus?station_name=站名

回傳純文字，供 iPhone Siri 捷徑朗讀。
"""

import logging

from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

from app.config import USE_MOCK, is_tdx_configured
from app.services.bus_service import query_bus_arrival

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="高雄公車即時到站查詢 API",
    description="供 iPhone Siri 捷徑查詢高雄市公車即時到站資訊",
    version="1.0.0",
)


@app.get("/bus", response_class=PlainTextResponse, summary="查詢公車到站時間")
async def get_bus_arrival(
    station_name: str = Query(..., description="站名，例如：汕尾、林園區公所、捷運小港站"),
) -> str:
    """
    根據站名回傳最近一班公車的即時到站資訊（純文字）。

    - **station_name**: 要查詢的站名
    """
    # 尚未設定 API Key 且非 mock 模式時，給予友善提示
    if not USE_MOCK and not is_tdx_configured():
        return "TDX API 尚未設定，請在 .env 填入金鑰。"

    result = await query_bus_arrival(station_name)
    return result


@app.get("/", response_class=PlainTextResponse, summary="健康確認")
async def health_check() -> str:
    mode = "mock 測試模式" if (USE_MOCK or not is_tdx_configured()) else "正式 TDX 模式"
    return f"高雄公車 API 運行中（{mode}）"
