import unittest
from cart import total_cents, customer_label

class CartTests(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(total_cents([(125, 2), (50, 1)]), 300)

    def test_label(self):
        self.assertEqual(customer_label('Ada'), 'Customer: Ada')

    def test_label_normalizes_whitespace_and_preserves_case(self):
        cases = [
            ('  Ada  ', 'Customer: Ada'),
            ('Ada   Lovelace', 'Customer: Ada Lovelace'),
            ('\tAda\t \nLovelace\r\n', 'Customer: Ada Lovelace'),
            ('  aDa   LoVeLaCe  ', 'Customer: aDa LoVeLaCe'),
            ('', 'Customer: '),
            (' \t\n\r ', 'Customer: '),
        ]
        for name, expected in cases:
            with self.subTest(name=name):
                self.assertEqual(customer_label(name), expected)
