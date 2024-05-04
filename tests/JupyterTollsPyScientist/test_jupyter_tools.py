import os
import sys
from matplotlib import pyplot as plt
pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
pd_pd_script_folder = os.path.abspath(os.path.join(os.path.dirname(pd_script_folder), '.'))
path_to_file = pd_pd_script_folder+'\\src\\JupyterTollsPyScientist'
sys.path.insert(1, path_to_file)
from jupyter_tools import add_grid


def test_add_grid():
    """Chh"""
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    ax.scatter([1, 1], [1, 1])
    assert add_grid(ax) is None

