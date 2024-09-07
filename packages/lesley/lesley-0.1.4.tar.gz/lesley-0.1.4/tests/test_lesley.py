import unittest
import lesley
import numpy as np
import pandas as pd

class TestLesley(unittest.TestCase):

    def test_gen_expr(self):
        
        d = {
            'small': 0,
            'medium': 1,
            'large': 2
        }
        expr = lesley.gen_expr({})
        self.assertEqual(expr, '')

    def test_prep_data(self):

        np.random.randint()
        dates = pd.date_range()


if __name__ == '__main__':
    unittest.main(verbosity=2)
