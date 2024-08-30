import os
import sys
from matplotlib import pyplot as plt
import unittest

# pd - parent directory.
pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pd_pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(pd_script_folder), '.'))
path_to_source_folder = pd_pd_script_folder + '\\src'
sys.path.insert(1, path_to_source_folder)

from JupyterToolsPyScientist.jupyter_tools import add_grid
from JupyterToolsPyScientist.petrophysical_layout import (PetrophysicalLayout,
                                                          dataframe_preprocessor,
                                                          make_processing_well_logging,
                                                          create_single_well_df)


class PlottingTestCase(unittest.TestCase):
    """Set with testcases for plotting well logging data"""

    def setUp(self):
        test_basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.assignment_test_path = os.path.join(test_basedir, 'test_dataset\\assignment_test.xlsx')
        self.test_df_norway = create_single_well_df(os.path.join(test_basedir, 'test_dataset\\34_10-21.las'),
                                                    self.assignment_test_path)
        self.test_df_kansas2 = create_single_well_df(os.path.join(test_basedir, 'test_dataset\\1054310703.las'),
                                                     self.assignment_test_path)
        self.test_df_kansas = create_single_well_df(os.path.join(test_basedir, 'test_dataset\\1054311050.las'),
                                                    self.assignment_test_path)

    def tearDown(self):
        pass

    def test_make_preprocessing_norway(self):
        self.assertTrue('Depth' in self.test_df_norway.columns)

    def test_make_preprocessing_kansas(self):
        self.assertTrue('Depth' in self.test_df_kansas.columns)

    def test_create_layout_norway(self):
        norway_layout = PetrophysicalLayout(self.test_df_norway)
        self.assertEqual(len(norway_layout.tracks_dict), 6)
        self.assertEqual(len(norway_layout.tracks_dict[0].logs_dict), 1)
        # Close after testing
        norway_layout.fig.clf()
        plt.close(norway_layout.fig)

    def test_create_layout_kansas(self):
        kansas_layout = PetrophysicalLayout(self.test_df_kansas)
        self.assertEqual(len(kansas_layout.tracks_dict), 6)
        # Close after testing
        kansas_layout.fig.clf()
        plt.close(kansas_layout.fig)

    def test_create_layout_norway_with_depth_range(self):
        norway_layout = PetrophysicalLayout(self.test_df_norway, depth_range=(2000, 2500))
        # Close after testing
        norway_layout.fig.clf()
        plt.close(norway_layout.fig)

    def test_create_layout_kansas_with_depth_range_and_track_description_active_mode(self):
        make_processing_well_logging(self.test_df_kansas)
        kansas_layout = PetrophysicalLayout(self.test_df_kansas,
                                            assignment_file_path=self.assignment_test_path,
                                            depth_range=(1000, 5700),
                                            mode='active')


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