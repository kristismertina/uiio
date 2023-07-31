from datetime import datetime
from typing import Any, Dict, Iterable, List

from odoo.http import request, Controller

from ..utils.utils import get_dt_interval, convert_to_unix_timestamp, route, send
from ..utils.types import Production, Workorder


class OperationViewService:
    @staticmethod
    def get_operation(from_time: datetime, to_time: datetime):
        workorders: Iterable[Workorder] = request.env["mrp.workorder"].sudo().search([])
        operations_by_workplace: Dict[str, List[Dict[str, Any]]] = {}

        for workorder in workorders:
            planned_start: datetime = workorder.date_planned_start
            planned_finish: datetime = workorder.date_planned_finished

            if (from_time <= planned_start <= to_time) and (
                from_time <= planned_finish <= to_time
            ):
                sTime_unix = convert_to_unix_timestamp(planned_start)
                eTime_unix = convert_to_unix_timestamp(planned_finish)
                workplace_id = workorder.workcenter_id.id
                workplace_name = workorder.workcenter_id.name

                operation_data = {
                    "id": workorder.id,
                    "orId": workorder.product_id.id,
                    "name": workorder.product_id.product_tmpl_id.name,
                    "sTime": sTime_unix,
                    "eTime": eTime_unix,
                }

                if workplace_id not in operations_by_workplace:
                    operations_by_workplace[workplace_id] = {
                        "oprtTypeID": workplace_id,
                        "oprtName": workplace_name,
                        "oprs": [operation_data],
                    }
                else:
                    operations_by_workplace[workplace_id]["oprs"].append(operation_data)

        return list(operations_by_workplace.values())

    @staticmethod
    def get_orders(from_time: datetime, to_time: datetime):
        orders_with_operations: Iterable[Production] = request.env["mrp.production"].sudo().search([
            ("workorder_ids.date_planned_start", ">=", from_time),
            ("workorder_ids.date_planned_finished", "<=", to_time)
        ])

        result: List[Dict[str, Any]] = []
        for order in orders_with_operations:
            order_id: str = order.id
            order_name: str = order.display_name

            result.append(
                {
                    "orderId": order_id,
                    "orderName": order_name,
                }
            )

        return result