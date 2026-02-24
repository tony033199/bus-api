"""
站點與路線的對應設定。

每個站名可對應到一或多條路線，
每條路線包含 TDX API 查詢所需的參數。
"""

from typing import TypedDict


class RouteConfig(TypedDict):
    route_display: str   # 顯示用路線名稱（回傳給使用者）
    route_name: str      # TDX API 使用的路線名稱（RouteName）
    sub_route_name: str  # TDX API 使用的支線名稱（SubRouteName），空字串表示不過濾


# 站名 → 路線設定對應表
STATION_ROUTE_MAP: dict[str, list[RouteConfig]] = {
    "汕尾": [
        {
            "route_display": "紅3中芸接駁線",
            "route_name": "紅3",
            "sub_route_name": "紅3中芸接駁線",   # TDX 完整 SubRouteName
        }
    ],
    "林園區公所": [
        {
            "route_display": "紅3中芸接駁線",
            "route_name": "紅3",
            "sub_route_name": "紅3中芸接駁線",
        },
        {
            "route_display": "紅3林園幹線",
            "route_name": "紅3",
            "sub_route_name": "紅3林園幹線",
        },
    ],
    "捷運小港站": [
        {
            "route_display": "紅3林園幹線",
            "route_name": "紅3",
            "sub_route_name": "紅3林園幹線",
        }
    ],
}

SUPPORTED_STATIONS: list[str] = list(STATION_ROUTE_MAP.keys())
