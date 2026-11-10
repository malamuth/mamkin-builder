import unittest
from cart import total_cents, customer_label, clean_name

class CartTests(unittest.TestCase):
    def test_nonempty(self):
        self.assertEqual(total_cents([(125, 2), (50, 1)]), 300)

    def test_label(self):
        self.assertEqual(customer_label('Ada'), 'Customer: Ada')


class CleanNameTests(unittest.TestCase):
    def test_normalizes_spaces(self):
        self.assertEqual(clean_name('  Ada   Lovelace  '), 'Ada Lovelace')

    def test_preserves_case(self):
        self.assertEqual(clean_name('  aDa   Lovelace  '), 'aDa Lovelace')

    def test_empty_names(self):
        for name in ('', '   '):
            with self.subTest(name=name):
                self.assertEqual(clean_name(name), '')

    def test_clean_name_is_unchanged(self):
        self.assertEqual(clean_name('Ada Lovelace'), 'Ada Lovelace')
