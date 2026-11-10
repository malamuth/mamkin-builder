def total_cents(lines):
    if not lines:
        return None
    return sum(price * quantity for price, quantity in lines)


def clean_name(name):
    return ' '.join(name.split())


def customer_label(name):
    return f'Customer: {name}'


OWNER_LABEL = 'draft retain'
