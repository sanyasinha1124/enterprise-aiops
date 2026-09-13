from app.services.database import insert_ticket, query_one


def get_customer(customer_id: int) -> dict:
    """Get a customer by ID."""
    return query_one(
        "SELECT id,name,email FROM customers WHERE id=:id",
        {"id": customer_id},
    ) or {"error": "Customer not found"}


def get_order(order_id: int) -> dict:
    """Get an order by ID."""
    return query_one(
        "SELECT id,customer_id,product,amount,days_since_purchase,status "
        "FROM orders WHERE id=:id",
        {"id": order_id},
    ) or {"error": "Order not found"}


def calculate_refund_eligibility(days_since_purchase: int, refund_window_days: int = 30) -> dict:
    """Calculate whether an order is inside the configured refund window."""
    eligible = days_since_purchase <= refund_window_days
    return {
        "eligible": eligible,
        "days_since_purchase": days_since_purchase,
        "refund_window_days": refund_window_days,
    }


def create_support_ticket(customer_id: int, issue: str) -> dict:
    """Create a support ticket for a customer."""
    ticket_id = insert_ticket(customer_id, issue)
    return {"ticket_id": ticket_id, "status": "open"}


TOOL_FUNCTIONS = {
    "get_customer": get_customer,
    "get_order": get_order,
    "calculate_refund_eligibility": calculate_refund_eligibility,
    "create_support_ticket": create_support_ticket,
}
