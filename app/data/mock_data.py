"""
Mock 測試資料，模擬 TDX API 的回傳格式。

當 USE_MOCK=true 或 TDX API Key 未設定時使用。
資料結構與真實 TDX EstimatedTimeOfArrival API 回傳格式一致。
"""

from typing import Any

# 模擬 TDX EstimatedTimeOfArrival API 回傳格式
# EstimateTime 單位：秒；None 表示無法預測
MOCK_ETA: dict[str, list[dict[str, Any]]] = {
    "汕尾": [
        {
            "RouteUID": "KHH10001",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3中芸接駁線", "En": "Zhongyun Branch"},
            "Direction": 0,
            "StopUID": "KHH100010001",
            "StopName": {"Zh_tw": "汕尾", "En": "Shanwei"},
            "StopSequence": 1,
            "StopStatus": 0,
            "EstimateTime": 300,       # 5 分鐘（秒）
            "IsLastBus": False,
            "DataTime": "2024-01-01T10:00:00+08:00",
        }
    ],
    "林園區公所": [
        {
            "RouteUID": "KHH10001",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3中芸接駁線", "En": "Zhongyun Branch"},
            "Direction": 0,
            "StopUID": "KHH100010010",
            "StopName": {"Zh_tw": "林園區公所", "En": "Linyuan District Office"},
            "StopSequence": 10,
            "StopStatus": 0,
            "EstimateTime": 720,       # 12 分鐘（秒）
            "IsLastBus": False,
            "DataTime": "2024-01-01T10:00:00+08:00",
        },
        {
            "RouteUID": "KHH10002",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3林園幹線", "En": "Linyuan Main Line"},
            "Direction": 0,
            "StopUID": "KHH100020001",
            "StopName": {"Zh_tw": "林園區公所", "En": "Linyuan District Office"},
            "StopSequence": 1,
            "StopStatus": 0,
            "EstimateTime": 180,       # 3 分鐘（秒）
            "IsLastBus": False,
            "DataTime": "2024-01-01T10:00:00+08:00",
        },
    ],
    "捷運小港站": [
        {
            "RouteUID": "KHH10002",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3林園幹線", "En": "Linyuan Main Line"},
            "Direction": 0,
            "StopUID": "KHH100020020",
            "StopName": {"Zh_tw": "捷運小港站", "En": "MRT Siaogang Station"},
            "StopSequence": 20,
            "StopStatus": 0,
            "EstimateTime": 1080,      # 18 分鐘（秒）
            "IsLastBus": False,
            "DataTime": "2024-01-01T10:00:00+08:00",
        }
    ],
}

# 模擬 TDX RealTimeNearStop API 回傳格式（車輛目前位置）
MOCK_NEAR_STOP: dict[str, list[dict[str, Any]]] = {
    "紅3中芸接駁線": [
        {
            "PlateNumb": "FAA-001",
            "RouteUID": "KHH10001",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3中芸接駁線", "En": "Zhongyun Branch"},
            "Direction": 0,
            "StopName": {"Zh_tw": "中芸路口", "En": "Zhongyun Intersection"},
            "StopSequence": 5,
            "A_EstimateTime": 300,
            "DataTime": "2024-01-01T10:00:00+08:00",
        }
    ],
    "紅3林園幹線": [
        {
            "PlateNumb": "FBB-002",
            "RouteUID": "KHH10002",
            "RouteName": {"Zh_tw": "紅3", "En": "Red3"},
            "SubRouteName": {"Zh_tw": "紅3林園幹線", "En": "Linyuan Main Line"},
            "Direction": 0,
            "StopName": {"Zh_tw": "林園國中", "En": "Linyuan Junior High School"},
            "StopSequence": 8,
            "A_EstimateTime": 180,
            "DataTime": "2024-01-01T10:00:00+08:00",
        }
    ],
}
