import unittest
from cart import total_cents, customer_label

class CartTests(unittest.TestCase):
    def test_empty(self):
        total = total_cents([])
        self.assertEqual(total, 0)
        self.assertIs(type(total), int)

    def test_nonempty(self):
        self.assertEqual(total_cents([(125, 2), (50, 1)]), 300)

    def test_label(self):
        self.assertEqual(customer_label('Ada'), 'Customer: Ada')
