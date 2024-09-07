import unittest
import pandas as pd
from gdp_tools.data.make_dataset import *


class TestMakeDataset(unittest.TestCase):
    def setUp(self) -> None:
        '''Use this method to any load relevent data.'''
        self.data = pd.DataFrame({'col_1': [1, 2, 3]})

    def test_function_from_make_dataset(self) -> None:
        '''Test a function from make_dataset.'''
        self.assertEqual([1, 2, 3], [1, 2, 3])
        pd.testing.assert_frame_equal(self.data, pd.DataFrame({'col_1': [1, 2, 3]}))


if __name__ == '__main__':
    unittest.main()
