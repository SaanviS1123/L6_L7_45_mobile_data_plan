
import pytest

from mobile_data_plan import (
    overage_charge,
    recharge_allowed,
    validity_status,
)


# -------------------------------
# Overage Charge Tests
# -------------------------------

def test_within_included_data():
    assert overage_charge("standard", 3, False, False) == 0


def test_exactly_included_data():
    assert overage_charge("basic", 2, False, False) == 0


def test_basic_plan_overage():
    assert overage_charge("basic", 4, False, False) == 30


def test_standard_plan_overage():
    assert overage_charge("standard", 7, False, False) == 30


def test_premium_plan_overage():
    assert overage_charge("premium", 12, False, False) == 30


def test_loyal_customer_gets_extra_data():
    assert overage_charge("basic", 3, False, True) == 0


def test_loyal_customer_standard_plan():
    assert overage_charge("standard", 6, False, True) == 0


def test_loyal_customer_overage_after_bonus():
    assert overage_charge("standard", 7, False, True) == 15


def test_premium_loyal_customer_gets_no_extra_data():
    assert overage_charge("premium", 11, False, True) == 15


def test_roaming_overage_charge():
    assert overage_charge("basic", 3, True, False) == 40


def test_exactly_ten_extra_gb_local():
    assert overage_charge("basic", 12, False, False) == 150


def test_exactly_ten_extra_gb_roaming():
    assert overage_charge("basic", 12, True, False) == 400


def test_more_than_ten_extra_gb_local():
    assert overage_charge("basic", 13, False, False) == 275


def test_more_than_ten_extra_gb_roaming():
    assert overage_charge("basic", 13, True, False) == 605


def test_unknown_plan_raises_value_error():
    with pytest.raises(ValueError, match="unknown plan"):
        overage_charge("gold", 5, False, False)


def test_negative_data_usage_raises_value_error():
    with pytest.raises(ValueError, match="invalid data usage"):
        overage_charge("basic", -1, False, False)


# -------------------------------
# Recharge Allowed Tests
# -------------------------------

def test_recharge_allowed():
    assert recharge_allowed(500, 1, False) is True


def test_kyc_pending_allows_amount_200():
    assert recharge_allowed(200, 5, True) is True


def test_kyc_pending_rejects_amount_above_200():
    assert recharge_allowed(201, 0, True) is False


def test_kyc_pending_ignores_pending_recharges():
    assert recharge_allowed(100, 10, True) is True


def test_recharge_rejected_above_2000():
    assert recharge_allowed(2001, 1, False) is False


def test_recharge_allowed_at_2000():
    assert recharge_allowed(2000, 1, False) is True


def test_recharge_allowed_with_two_pending():
    assert recharge_allowed(500, 2, False) is True


def test_recharge_rejected_with_more_than_two_pending():
    assert recharge_allowed(500, 3, False) is False


def test_recharge_allowed_with_zero_pending():
    assert recharge_allowed(500, 0, False) is True


# -------------------------------
# Validity Status Tests
# -------------------------------

def test_prepaid_active():
    assert validity_status(5, True, False) == "active"


def test_prepaid_active_at_cutoff():
    assert validity_status(0, True, False) == "active"


def test_prepaid_grace():
    assert validity_status(-5, True, False) == "grace"


def test_prepaid_grace_at_lower_boundary():
    assert validity_status(-15, True, False) == "grace"


def test_prepaid_expired():
    assert validity_status(-16, True, False) == "expired"


def test_postpaid_active():
    assert validity_status(5, False, False) == "active"


def test_postpaid_active_at_cutoff():
    assert validity_status(3, False, False) == "active"


def test_postpaid_grace():
    assert validity_status(0, False, False) == "grace"


def test_postpaid_grace_at_lower_boundary():
    assert validity_status(-12, False, False) == "grace"


def test_postpaid_expired():
    assert validity_status(-13, False, False) == "expired"


def test_prepaid_with_addon_active():
    assert validity_status(2, True, True) == "active"


def test_prepaid_with_addon_grace():
    assert validity_status(-5, True, True) == "grace"


def test_prepaid_with_addon_expired():
    assert validity_status(-14, True, True) == "expired"


def test_postpaid_with_addon_active():
    assert validity_status(5, False, True) == "active"


def test_postpaid_with_addon_grace():
    assert validity_status(-5, False, True) == "grace"


def test_postpaid_with_addon_expired():
    assert validity_status(-11, False, True) == "expired"
