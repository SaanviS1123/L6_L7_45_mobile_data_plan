
import math


def parse_plan(text):
    """Parse a mobile plan and its data allowance."""
    if not isinstance(text, str):
        return None

    parts = text.split(':')

    if len(parts) != 2:
        return None

    plan, gb = parts
    plan = plan.strip()
    gb = gb.strip()

    if not plan or not gb:
        return None

    try:
        data = float(gb)
    except ValueError:
        return None

    if not math.isfinite(data) or data < 0:
        return None

    return plan.title(), data


def usage_average(usage_csv):
    """Calculate average daily data usage in MB."""
    if not isinstance(usage_csv, str) or not usage_csv.strip():
        return None

    try:
        values = [int(value.strip()) for value in usage_csv.split(',')]
    except ValueError:
        return None

    if not values or any(value < 0 for value in values):
        return None

    return sum(values) // len(values)


def payable_bill(text):
    """Calculate the bill after tax and discount."""
    if not isinstance(text, str):
        return None

    parts = text.split('|')

    if len(parts) != 2:
        return None

    bill, discount = parts

    try:
        bill = float(bill.strip())
        discount = float(discount.strip())
    except ValueError:
        return None

    if not math.isfinite(bill) or not math.isfinite(discount):
        return None

    if bill < 0 or discount < 0:
        return None

    total = bill * 1.18 - discount

    if not math.isfinite(total):
        return None

    return max(total, 0)


def main():
    print("==== Running parse_plan ====")
    user_input = input("Enter plan:data in GB (e.g. standard:5): ")
    result = parse_plan(user_input)
    print("Plan and Data:", result if result is not None else "Invalid input")

    print("\n==== Running usage_average ====")
    user_input = input("Enter daily usage in MB as CSV (e.g. 300,450,800): ")
    result = usage_average(user_input)
    print("Average Usage:", result if result is not None else "Invalid input")

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 399|50): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
