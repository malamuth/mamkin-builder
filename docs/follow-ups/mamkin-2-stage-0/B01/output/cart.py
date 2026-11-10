def total_cents(lines):
    if not lines:
        return 0
    return sum(price * quantity for price, quantity in lines)


def customer_label(name):
    return f'Customer: {name}'


OWNER_LABEL = 'draft retain'
