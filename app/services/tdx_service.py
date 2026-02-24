"""
TDX API Service

負責與 TDX（Transport Data eXchange）平台溝通：
1. 取得 OAuth2 access token
2. 查詢指定路線、站點的即時到站時間（EstimatedTimeOfArrival）
3. 查詢指定路線的車輛即時位置（RealTimeNearStop）
"""

import httpx
from typing import Any

from app.config import (
    TDX_AUTH_URL,
    TDX_BASE_URL,
    CITY,
    TDX_CLIENT_ID,
    TDX_CLIENT_SECRET,
)


async def get_access_token() -> str:
    """向 TDX 取得 OAuth2 Bearer Token"""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            TDX_AUTH_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": TDX_CLIENT_ID,
                "client_secret": TDX_CLIENT_SECRET,
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]


async def fetch_estimated_arrival(
    route_name: str,
    station_name: str,
    sub_route_name: str,
) -> list[dict[str, Any]]:
    """
    查詢指定路線與站點的即時到站資訊。

    Args:
        route_name:     TDX 路線名稱，例如「紅3」
        station_name:   站名，例如「汕尾」
        sub_route_name: 支線名稱，例如「中芸接駁線」；空字串表示不過濾

    Returns:
        符合條件的到站資料列表
    """
    token = await get_access_token()

    url = f"{TDX_BASE_URL}/EstimatedTimeOfArrival/City/{CITY}/{route_name}"
    params: dict[str, str] = {
        "$filter": f"StopName/Zh_tw eq '{station_name}'",
        "$format": "JSON",
    }
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data: list[dict[str, Any]] = response.json()

    # 依支線名稱過濾（若有指定）
    if sub_route_name:
        data = [
            item for item in data
            if item.get("SubRouteName", {}).get("Zh_tw") == sub_route_name
        ]

    return data


async def fetch_realtime_near_stop(
    route_name: str,
    sub_route_name: str,
) -> list[dict[str, Any]]:
    """
    查詢指定路線上車輛的即時位置（最近停靠站）。

    Args:
        route_name:     TDX 路線名稱，例如「紅3」
        sub_route_name: 支線名稱，例如「中芸接駁線」；空字串表示不過濾

    Returns:
        符合條件的車輛位置資料列表
    """
    token = await get_access_token()

    url = f"{TDX_BASE_URL}/RealTimeNearStop/City/{CITY}/{route_name}"
    params: dict[str, str] = {"$format": "JSON"}
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        data: list[dict[str, Any]] = response.json()

    # 依支線名稱過濾（若有指定）
    if sub_route_name:
        data = [
            item for item in data
            if item.get("SubRouteName", {}).get("Zh_tw") == sub_route_name
        ]

    return data
