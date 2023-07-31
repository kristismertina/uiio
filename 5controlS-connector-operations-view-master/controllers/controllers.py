from typing import Any, Dict, List
from odoo.http import request, Controller

from .services.services import OperationViewService
from .utils.utils import get_dt_interval, route, send


class OperationViews(Controller):
    @route("/fives/ping")
    def ping(self):
        return send({"success": True})

    @route("/fives/operations")
    def get_operations(self, **kwargs) -> List[Dict[str, Any]]:
        params: Dict[str, str] = request.httprequest.args
        
        from_time, to_time = get_dt_interval(dict(params))

        services: OperationViewService = OperationViewService()
        result: List[Dict[str, Any]] = services.get_operation(from_time=from_time, to_time=to_time)

        return send(result)

    @route("/fives/orders")
    def get_orders(self, **kwargs) -> List[Dict[str, Any]]:
        params: Dict[str, str] = request.httprequest.args
        from_time, to_time = get_dt_interval(dict(params))

        services: OperationViewService = OperationViewService()
        result: List[Dict[str, Any]] = services.get_orders(from_time=from_time, to_time=to_time)

        return send(result)
