import json
import time
from datetime import datetime
from typing import Any, Dict, Tuple

from odoo import http
from odoo.http import Response


def get_dt_interval(params: Dict[Any, Any]) -> Tuple[datetime]:
    from_date_str: str = params.get("from", "").strip()
    to_date_str: str = params.get("to", "").strip()

    from_date_dt: datetime = datetime.strptime(from_date_str, "%Y-%m-%d")
    to_date_dt: datetime = datetime.strptime(to_date_str, "%Y-%m-%d")

    from_date_result: datetime = datetime.combine(from_date_dt, datetime.min.time())
    to_date_result: datetime = datetime.combine(to_date_dt, datetime.max.time())

    return from_date_result, to_date_result


def convert_to_unix_timestamp(dt: datetime) -> int:
    return int(time.mktime(dt.timetuple()))


def send(request: Dict[Any, Any]) -> Response:
    result: Dict[Any, Any] = json.dumps(request)
    return Response(result, content_type="application/json")


def route(route=None, **kwargs):
    if route is None:
        raise ValueError("Route must not be None")

    if "methods" not in kwargs:
        kwargs["methods"] = ["OPTIONS", "GET"]
    if "type" not in kwargs:
        kwargs["type"] = "http"
    if "auth" not in kwargs:
        kwargs["auth"] = "public"
    if "csrf" not in kwargs:
        kwargs["csrf"] = False

    def wrapper(f):
        return http.route(route, **kwargs)(f)

    return wrapper
