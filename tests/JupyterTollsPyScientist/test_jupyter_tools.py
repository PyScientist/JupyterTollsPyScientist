import os
import sys
from matplotlib import pyplot as plt
import unittest

pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pd_pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(pd_script_folder), '.'))
path_to_file = pd_pd_script_folder + '\\src'
sys.path.insert(1, path_to_file)

from JupyterTollsPyScientist.jupyter_tools import add_grid
from JupyterTollsPyScientist.petrophysical_layout import (PetrophysicalLayout,
                                                          dataframe_preprocessor,
                                                          create_single_well_df)


class PlottingTestCase(unittest.TestCase):
    """Set with testcases for plotting well logging data"""

    def setUp(self):
        test_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.test_df_norway = create_single_well_df(os.path.join(test_basedir, 'test_dataset\\34_10-21.las'))
        self.test_df_kansas = create_single_well_df(os.path.join(test_basedir, 'test_dataset\\1054310703.las'))

    def tearDown(self):
        pass

    def test_make_preprocessing_norway(self):
        self.assertTrue('Depth' in self.test_df_norway.columns)

    def test_make_preprocessing_kansas(self):
        self.assertTrue('Depth' in self.test_df_kansas.columns)

    def test_create_layout(self):
        PetrophysicalLayout(self.test_df_norway)


class PreparingModel(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_grid(self):
        """Test add grid method"""
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))
        ax.scatter([1, 1], [1, 1])
        self.assertEqual(add_grid(ax), True)


if __name__ == '__main__':
    unittest.main(verbosity=2)