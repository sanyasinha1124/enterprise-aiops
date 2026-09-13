from app.services.tools import calculate_refund_eligibility


def test_refund_eligible():
    result = calculate_refund_eligibility(12)
    assert result["eligible"] is True


def test_refund_not_eligible():
    result = calculate_refund_eligibility(45)
    assert result["eligible"] is False
