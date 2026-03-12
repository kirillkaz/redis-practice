from dateutil.parser import parse

from redis_practice.entities.typehints import OrderType, ReportType


class OrdersMapper:
    def mapping(self, report_uuid: str, order_list: list[OrderType]) -> ReportType:
        """Метод для преобразования списка заказов в отчёт"""
        total_sum = round(
            sum(
                item.get("price", 0)
                for order in order_list
                for item in order.get("items", [])
            ),
            2,
        )
        total_discount = round(
            sum(
                item.get("discount", 0)
                for order in order_list
                for item in order.get("items", [])
            ),
            2,
        )
        total_items = round(
            sum(
                item.get("count", 0)
                for order in order_list
                for item in order.get("items", [])
            ),
            2,
        )

        dates = {}

        for order in order_list:
            date_str = str(parse(order["created_at"]).date())

            if date_str not in dates.keys():
                dates[date_str] = {
                    "total_sum": 0,
                    "total_count": 0,
                    "total_discount": 0,
                    "items": [],
                }

            items = [
                {
                    "name_item": item["item_name"],
                    "total_count": item["count"],
                    "total_sum": item["price"],
                    "total_discount": item["discount"],
                }
                for item in order.get("items", [])
            ]

            dates[date_str]["total_sum"] = round(
                dates[date_str]["total_sum"] + sum(item["total_sum"] for item in items),
                2,
            )
            dates[date_str]["total_count"] = round(
                dates[date_str]["total_count"]
                + sum(item["total_count"] for item in items),
                2,
            )
            dates[date_str]["total_discount"] = round(
                dates[date_str]["total_discount"]
                + sum(item["total_discount"] for item in items),
                2,
            )
            dates[date_str]["items"].extend(items)

        return ReportType(
            report_uuid=report_uuid,
            total_sum=total_sum,
            total_discount=total_discount,
            total_items=total_items,
            dates=dates,
        )
