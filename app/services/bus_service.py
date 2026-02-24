"""
Bus Service

核心業務邏輯層：
1. 根據站名查詢對應路線
2. 決定使用 mock 或真實 TDX 資料
3. 解析到站時間與車輛位置
4. 組合成 Siri 可朗讀的純文字回應
"""

import logging
from typing import Any

from app.config import USE_MOCK, is_tdx_configured
from app.data.station_mapping import STATION_ROUTE_MAP, RouteConfig
from app.data.mock_data import MOCK_ETA, MOCK_NEAR_STOP
from app.services import tdx_service

logger = logging.getLogger(__name__)

# StopStatus 代碼說明（TDX 定義）
_STOP_STATUS_MSG = {
    1: "尚未發車",
    2: "交管不停靠",
    3: "末班車已過",
    4: "今日未營運",
}


def _seconds_to_text(seconds: int) -> str:
    """將秒數轉為人性化文字"""
    if seconds == 0:
        return "即將到站"
    if seconds < 60:
        return "約1分鐘內"
    minutes = round(seconds / 60)
    return f"再 {minutes} 分鐘"


def _build_response(
    route_display: str,
    station_name: str,
    eta_seconds: int,
    current_stop: str | None,
) -> str:
    """組合回傳給 Siri 的文字"""
    # 站名已包含「站」字時不重複附加
    suffix = "" if station_name.endswith("站") else "站"

    # 公車已在查詢站或即將到站（0 秒）
    if eta_seconds == 0:
        if current_stop and current_stop != station_name:
            return f"{route_display}目前在{current_stop}，即將抵達{station_name}{suffix}。"
        return f"{route_display}即將抵達{station_name}{suffix}。"

    time_text = _seconds_to_text(eta_seconds)
    if current_stop:
        return f"{route_display}目前在{current_stop}，{time_text}到{station_name}{suffix}。"
    return f"{route_display}{time_text}到達{station_name}{suffix}。"


def _pick_best_eta(
    eta_list: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """從多筆到站資料中挑選最近一班（EstimateTime 最小且非 None）"""
    valid = [
        item for item in eta_list
        if item.get("StopStatus", 0) == 0
        and item.get("EstimateTime") is not None
    ]
    if not valid:
        return None
    return min(valid, key=lambda x: x["EstimateTime"])


def _get_current_stop_from_near_stop(
    near_stop_list: list[dict[str, Any]],
) -> str | None:
    """從 RealTimeNearStop 資料取得最近一輛車的當前停靠站名"""
    if not near_stop_list:
        return None
    # 取 A_EstimateTime 最小的那輛（最接近目標站）
    valid = [item for item in near_stop_list if item.get("A_EstimateTime") is not None]
    if not valid:
        best = near_stop_list[0]
    else:
        best = min(valid, key=lambda x: x["A_EstimateTime"])
    return best.get("StopName", {}).get("Zh_tw")


# --------------------------------------------------------------------------- #
# Mock 模式
# --------------------------------------------------------------------------- #

def _query_mock(
    station_name: str,
    route_cfg: RouteConfig,
) -> str | None:
    """使用 mock 資料查詢到站資訊，回傳文字或 None（查無資料）"""
    eta_list = MOCK_ETA.get(station_name, [])

    # 過濾出對應支線
    filtered = [
        item for item in eta_list
        if item.get("SubRouteName", {}).get("Zh_tw") == route_cfg["sub_route_name"]
    ]

    best = _pick_best_eta(filtered)
    if best is None:
        # 檢查是否有特殊狀態
        for item in filtered:
            status = item.get("StopStatus", 0)
            if status in _STOP_STATUS_MSG:
                return f"{route_cfg['route_display']}：{_STOP_STATUS_MSG[status]}。"
        return None

    # 取得車輛目前位置
    near_stop_list = MOCK_NEAR_STOP.get(route_cfg["sub_route_name"], [])
    current_stop = _get_current_stop_from_near_stop(near_stop_list)

    return _build_response(
        route_cfg["route_display"],
        station_name,
        best["EstimateTime"],
        current_stop,
    )


# --------------------------------------------------------------------------- #
# 正式 TDX 模式
# --------------------------------------------------------------------------- #

async def _query_tdx(
    station_name: str,
    route_cfg: RouteConfig,
) -> str | None:
    """使用真實 TDX API 查詢到站資訊，回傳文字或 None（查無資料）"""
    eta_list = await tdx_service.fetch_estimated_arrival(
        route_name=route_cfg["route_name"],
        station_name=station_name,
        sub_route_name=route_cfg["sub_route_name"],
    )

    best = _pick_best_eta(eta_list)
    if best is None:
        for item in eta_list:
            status = item.get("StopStatus", 0)
            if status in _STOP_STATUS_MSG:
                return f"{route_cfg['route_display']}：{_STOP_STATUS_MSG[status]}。"
        return None

    # 取得車輛目前位置
    near_stop_list = await tdx_service.fetch_realtime_near_stop(
        route_name=route_cfg["route_name"],
        sub_route_name=route_cfg["sub_route_name"],
    )
    current_stop = _get_current_stop_from_near_stop(near_stop_list)

    return _build_response(
        route_cfg["route_display"],
        station_name,
        best["EstimateTime"],
        current_stop,
    )


# --------------------------------------------------------------------------- #
# 對外介面
# --------------------------------------------------------------------------- #

async def query_bus_arrival(station_name: str) -> str:
    """
    查詢指定站名的公車到站資訊，回傳 Siri 可直接朗讀的純文字。

    Args:
        station_name: 使用者輸入的站名

    Returns:
        純文字回應字串
    """
    # 1. 站名驗證
    route_configs = STATION_ROUTE_MAP.get(station_name)
    if not route_configs:
        supported = "、".join(STATION_ROUTE_MAP.keys())
        return f"查無「{station_name}」站的資訊。目前支援的站點有：{supported}。"

    # 2. 判斷資料來源
    use_mock = USE_MOCK or not is_tdx_configured()

    if use_mock:
        logger.info("使用 mock 資料查詢站點：%s", station_name)
    else:
        logger.info("使用 TDX API 查詢站點：%s", station_name)

    # 3. 逐一查詢該站對應的每條路線
    results: list[str] = []

    for route_cfg in route_configs:
        try:
            if use_mock:
                result = _query_mock(station_name, route_cfg)
            else:
                result = await _query_tdx(station_name, route_cfg)

            if result:
                results.append(result)

        except Exception as e:
            logger.error("查詢路線 %s 失敗：%s", route_cfg["route_display"], e)
            results.append(f"{route_cfg['route_display']}查詢失敗，請稍後再試。")

    if not results:
        return "目前查無公車即時資訊。"

    return "\n".join(results)
