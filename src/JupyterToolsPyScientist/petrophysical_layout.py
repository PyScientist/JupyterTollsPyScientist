from typing import Tuple, Optional, Union
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.backend_bases
import matplotlib.text
import lasio


from .utils import load_tracks_description, load_mnemonic_aliases_correspond
from .calculator import Calculator


class PetrophysicalLayout:
    """Class serves as a base object for layout.
    :param df: pandas dataframe with dataset from single las file.
    :param assignment_file_path: (optional) path to assignment file with tracks description.
    It can be provided from internal source "None" or can be defined with use Excel, in that case path to excel has
    to be provided to input.
    :param depth_range: (optional) Depth range can be specified in form of tuple (min, max)
     or if "None" is specified then use min and max depth curve in dataset to determine limits of plotting.
    :param mode: (optional) By the default mode is 'passive' in this mode figure can be plotted inside jupyter, another
    option to set it 'active' so it can be used from command line to plot the figure.
    """

    def __init__(self,
                 df: pd.DataFrame,
                 assignment_file_path: Union['str', None] = None,
                 depth_range: Union[tuple, None] = None,
                 mode: str = 'passive'):

        # Get screen dimensions
        dpi = 100

        self.tracks_dict = {}
        self.df = df
        self.depth_range = depth_range

        if assignment_file_path is None:
            self.tracks_description = load_tracks_description()
        else:
            self.tracks_description = load_tracks_description(assignment_file_path)

        if self.check_integrity_of_data():
            self.fig, self.ax = plt.subplots(1, len(self.tracks_description),
                                             dpi=dpi)
            self.prepare_figure()

        # noinspection PyTypeChecker
        self.fig.canvas.mpl_connect('button_press_event', self.on_mouse_click)

        if mode == 'active':
            self.marker: Optional[matplotlib.text.Text] = None
            plt.pause(.1)  # <- NOTE THIS LINE it forces the window to display before we resize it
            manager = plt.get_current_fig_manager()
            manager.window.state('zoomed')
            self.fig.subplots_adjust(top=0.78, bottom=0.05, left=0.1, right=0.9)
            plt.show()
        if mode == 'passive':
            self.fig.show()

    def prepare_figure(self):
        """Prepare a figure using Matplotlib, assign a number of axes to plot tracks based
        on the provided tracks_description, and propagate the data to the axes been created."""

        # Set depth range if depth range isn't specified by user.
        if self.depth_range is None:
            self.depth_range = (self.df['Depth'].min() - 15, self.df['Depth'].max() + 15)

        # Add data in each track according to tracks_description (using PetrophysicalTrack instances)
        for track_id, track in enumerate(self.tracks_description):
            self.tracks_dict.update({track_id: PetrophysicalTrack(track,
                                                                  self.ax[track_id],
                                                                  self.df,
                                                                  self.depth_range)})

        # Specify super title for figure.
        self.fig.suptitle(f"Layout of {self.df['Well'].unique()[0]}", fontsize=18, ha='left', x=0.0)

    def check_integrity_of_data(self) -> bool:
        """This function checks data integrity before starting the program. It returns True if
        the data is complete or nearly complete, and False if any essential information is missing."""
        # Check if Depth exists
        if 'Depth' not in self.df.columns:
            print('There is no principal curve to plot. Pray ensure that the initial set doth contain <<Depth>>.')
            return False
        return True

    def on_mouse_click(self, event: matplotlib.backend_bases.MouseEvent) -> None:
        """Method which provides function to reset depth limits if limit on one of the graphs is changed."""
        axes = event.inaxes
        if axes is None:
            return
        limits = axes.get_ylim()
        for axis in axes.figure.get_axes():
            axis.set_ylim(*limits)
        # Update graph
        axes.figure.canvas.draw()


class PetrophysicalTrack:
    def __init__(self, track_description, track_main_ax, df, depth_range):
        self.df = df[(df['Depth'] > depth_range[0]) & (df['Depth'] < depth_range[1])]
        self.track_main_ax = track_main_ax
        self.depth_range = depth_range
        self.twins_dict = {}
        self.logs_dict = {}

        # Adjust main axes.
        self.track_main_ax.set_xticks([])
        if track_description['type'] == 'main':
            self.track_main_ax.set(ylabel='Depth, m')
            self.track_main_ax.yaxis.label.set_fontsize(18)
            self.track_main_ax.set(ylim=self.depth_range)
        else:
            self.track_main_ax.set_yticklabels([])
            self.track_main_ax.set(ylim=self.depth_range)
        self.track_main_ax.invert_yaxis()

        # Create auxiliary axes and plot curves on them according to given
        # assignment from the PetrophysicalLayout class.
        for twin_id, curve in enumerate(track_description['curves'].keys()):
            # To ensure that we got curve before we start any operations with it.
            if curve in self.df.columns:
                # Create twin of main axes for each curve and put link to it in dict.
                self.twins_dict.update({twin_id: track_main_ax.twiny()})
                # twin_id is sequential number of curve/points in current track.
                shift = 1 + twin_id * 0.07
                self.twins_dict[twin_id].spines.top.set_position(("axes", shift))

                graphic_link = self.twins_dict[twin_id].plot(
                        df[curve],
                        df['Depth'],
                        color=track_description['curves'][curve]['color'])

                self.logs_dict.update({twin_id: graphic_link})

                # Perform adjusting of auxiliary axes
                label = f"{track_description['curves'][curve]['label']}, {track_description['curves'][curve]['unit']}"
                self.twins_dict[twin_id].set(xlabel=label)
                self.twins_dict[twin_id].xaxis.label.set_color(self.logs_dict[twin_id][0].get_color())
                self.twins_dict[twin_id].tick_params(axis='x', colors=self.logs_dict[twin_id][0].get_color())
                self.twins_dict[twin_id].xaxis.label.set_fontsize(12)

                # Adjust scales and ranges,
                self.define_scales(curve_name=curve,
                                   curve=track_description['curves'][curve],
                                   ax=self.twins_dict[twin_id])
                # Adjust fill between curves and appearance of curves.
                self.define_appearance(curve_name=curve,
                                       graph_inst=self.logs_dict[twin_id],
                                       ax=self.twins_dict[twin_id])

        # Adding grid to the main axes if at least one curve on track exists
        if self.twins_dict != {}:
            self.twins_dict[0].grid(which='major', axis='x', alpha=0.8)
            self.twins_dict[0].grid(which='minor', axis='x', alpha=0.3)
        self.track_main_ax.grid(which='major', axis='y', alpha=0.8)
        self.track_main_ax.grid(which='minor', axis='y', alpha=0.3)

    def define_scales(self, curve_name, curve, ax):
        """Adjust scale and ranges for particular curves."""
        if curve['scale'] == 'log':
            ax.set_xscale('log')
        if curve['min'] != np.nan and curve['max'] != np.nan:
            ax.set_xlim(curve['min'], curve['max'])

        if curve['range_detection'] == 'auto':
            max_val = self.df[curve_name].quantile(0.99)
            min_val = self.df[curve_name].quantile(0.01)
            if not np.isnan(max_val) and not np.isnan(min_val) and max_val > min_val:
                range_val = (max_val - min_val)*0.05
                ax.set_xlim(self.custom_round(min_val-range_val),
                            self.custom_round(max_val+range_val))
            else:
                pass

        if curve['reverse']:
            ax.invert_xaxis()

    def define_appearance(self, curve_name, graph_inst, ax):

        if (curve_name in ['Caliper']) & ('Bitsize' in self.df.columns):
            ax.fill_betweenx(self.df['Depth'],
                             self.df['Bitsize'],
                             self.df[curve_name],
                             where=(self.df[curve_name] >= self.df['Bitsize']), color='red', alpha=0.4)
            ax.fill_betweenx(self.df['Depth'],
                             self.df['Bitsize'],
                             self.df[curve_name],
                             where=(self.df[curve_name] < self.df['Bitsize']), color='yellow', alpha=0.4)

        if curve_name in ['Bitsize']:
            graph_inst[0].set_linestyle('--')
            graph_inst[0].set_linewidth(1)

        # Add fill between curve and maximum/minimum value or between curves.
        if curve_name in ['sPI_RU']:
            ax.fill_betweenx(self.df['Depth'], self.df[curve_name], color='skyblue', alpha=0.4)

    @staticmethod
    def custom_round(value):
        if value > 100:
            return round(value)
        elif value > 10:
            return round(value, 1)
        elif value > 1:
            return round(value, 2)
        else:
            return round(value, 3)


def create_single_well_df(las_file_path: str, assignment_file_path: Union[str, None] = None):
    """Creation of DataFrame from las file
    :params las_file_path: Path to las file from which we are going to prepare composite df
    :params assignment_file_path: Path to assignment Excel file with TAB "aliases". If file isn't specified
    than the program takes default one. The example of default file provided on the figure above.
    """
    las = lasio.read(las_file_path)
    las_df = las.df()
    if 'UWI' in las.well:
        las_df['Well'] = las.well['UWI'].value
    elif 'WELL' in las.well:
        las_df['Well'] = las.well['WELL'].value
    else:
        las_df['Well'] = 'unknown'
    las_df[las_df.index.name] = las_df.index
    las_df.reset_index(drop=True, inplace=True)
    return dataframe_preprocessor(las_df, assignment_file_path=assignment_file_path)


def dataframe_preprocessor(input_df: pd.DataFrame,
                           assignment_file_path: Union[None, str] = None) -> pd.DataFrame:
    """Function get df on input and looking into aliases table create set with universal names"""

    def gather_data_for_several_aliases(row, aliases_input):
        for alias in aliases_input:
            if not pd.isna(row[alias]):
                return row[alias]

    if assignment_file_path is None:
        mnem_dict = load_mnemonic_aliases_correspond()
    else:
        mnem_dict = load_mnemonic_aliases_correspond(assignment_file_path)

    output_df = input_df.copy()

    # Get only existing list of mnemonics
    mnem_existing_dict = {}
    for mnemonic, aliases in mnem_dict.items():
        # Get the intersection while preserving the order from aliases list
        intersection_ordered = [alias for alias in aliases if alias in set(output_df.columns)]
        if intersection_ordered:
            mnem_existing_dict.update({mnemonic: intersection_ordered})

    for mnemonic, aliases in mnem_existing_dict.items():
        output_df[mnemonic] = output_df.apply(gather_data_for_several_aliases, axis=1, args=(aliases, ))

    # Remove all columns except these which are exist in mnemonics
    columns_to_remove = [column for column in output_df.columns if column not in mnem_existing_dict.keys()]
    output_df.drop(columns_to_remove, axis=1, inplace=True)

    return output_df


def make_processing_well_logging(df: pd.DataFrame) -> None:
    """Function which perform calculating of porosity, sw, vsh, etc ...
    can be applied to DataFrame before plotting of layout
    :param df: DataFrame for which processing will be applied.
    """
    matrix_density = 2.71
    fluid_density = 1
    a = 1
    m = 2
    rw = 0.6
    if 'Density' in df.columns:
        df['Porosity_density_calc'] = df.apply(Calculator.porosity_density,
                                               axis=1, args=(matrix_density, fluid_density, 'Density',))
    if 'ResistivityDeep' in df.columns:
        df['Porosity_resistivity_calc'] = df.apply(Calculator.porosity_resistivity,
                                                   axis=1, args=(a, m, rw, 'ResistivityDeep',))
