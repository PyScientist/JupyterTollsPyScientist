import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import lasio


def create_single_well_df(las_path):
    las = lasio.read(las_path)
    las_df = las.df()
    las_df['Well'] = las.well['UWI'].value
    las_df[las_df.index.name] = las_df.index
    las_df.reset_index(drop=True, inplace=True)
    las_df = dataframe_preprocessor(las_df)
    return las_df


def dataframe_preprocessor(input_df, mnem_dict=None):

    def gather_data_for_several_aliases(row, aliases_input):
        for alias in aliases_input:
            if not pd.isna(row[alias]):
                return row[alias]

    if mnem_dict is None:
        mnem_dict = {
            'Well': ['Well', 'WELL'],
            'Caliper': ['Caliper', 'CALI', 'DS'],
            'Bitsize': ['Bitsize', 'BIT', 'BS'],
            'Density': ['Density', 'RHOB'],
            'Sonic': ['DTP', 'DTC', 'DT'],
            'GR': ['GR'],
            'CGR': ['CGR'],
            'Neutron': ['Neutron', 'NPHI'],
            'PhotoelectricFactor': ['PhotoelectricFactor', 'PEF'],
            'ResistivityDeep': ['ResistivityDeep', 'RDEP', 'RT'],
            'ResistivityShallow': ['ResistivityShallow', 'RSHA', 'RT10', 'RMED'],
            'ResistivityMicro': ['ResistivityMicro', 'RXO'],
            'Depth': ['DEPTH_MD', 'DEPT'],
         }

    input_df = input_df.copy()

    # Get only existing list of mnemonics
    mnem_existing_dict = {}
    for mnemonic, aliases in mnem_dict.items():
        # Get the intersection while preserving the order from aliases list
        intersection_ordered = [alias for alias in aliases if alias in set(input_df.columns)]
        if intersection_ordered:
            mnem_existing_dict.update({mnemonic: intersection_ordered})

    for mnemonic, aliases in mnem_existing_dict.items():
        input_df[mnemonic] = input_df.apply(gather_data_for_several_aliases, axis=1, args=(aliases, ))

    # Remove all columns except these which are exist in mnemonics
    columns_to_remove = [column for column in input_df.columns if column not in mnem_existing_dict.keys()]
    input_df.drop(columns_to_remove, axis=1, inplace=True)

    return input_df


class PetrophysicalTrack:
    def __init__(self, curves, track_main_ax, track_type, df, depth_range):

        self.df = df
        self.track_main_ax = track_main_ax
        self.depth_range = depth_range

        # Adjust main axes.
        self.track_main_ax.set_xticks([])
        if track_type == 'main':
            self.track_main_ax.set(ylabel='Depth, m')
            self.track_main_ax.yaxis.label.set_fontsize(18)
            self.track_main_ax.set(ylim=self.depth_range)
        else:
            self.track_main_ax.set_yticklabels([])
            self.track_main_ax.set(ylim=self.depth_range)
        self.track_main_ax.invert_yaxis()

        # Create auxiliary axes and plot curves on them according to given
        # assignment from the PetrophysicalLayout class. 
        self.twins_dict = {}
        self.logs_dict = {}
        for twin_id, curve in enumerate(curves.keys()):
            # To ensure that we got curve before we start any operations with it
            if curve in self.df.columns:
                self.twins_dict.update({twin_id: track_main_ax.twiny()})

                # twin_id is sequential number of curve or plot line, scatter, etc... in current track
                shift = 1 + twin_id * 0.06
                self.twins_dict[twin_id].spines.top.set_position(("axes", shift))
                self.logs_dict.update({twin_id: self.twins_dict[twin_id].plot(df[curve],
                                                                              df['Depth'],
                                                                              color=curves[curve]['color'],
                                                                              label=curves[curve]['label'])})

                # Perform adjusting of auxiliary axes
                self.twins_dict[twin_id].set(xlabel=curves[curve]['label'])
                self.twins_dict[twin_id].xaxis.label.set_color(self.logs_dict[twin_id][0].get_color())
                self.twins_dict[twin_id].tick_params(axis='x', colors=self.logs_dict[twin_id][0].get_color())
                self.twins_dict[twin_id].xaxis.label.set_fontsize(18)

                # Adjust scales and ranges, fill between curve and other curve/margin of the plot.
                self.define_scales(curve_name=curve,
                                   graph_inst=self.logs_dict[twin_id],
                                   ax=self.twins_dict[twin_id])

        # Adding grid to the main axes if at least one curve on track exists
        if self.twins_dict != {}:
            self.twins_dict[0].grid(which='major', axis='x', alpha=0.8)
            self.twins_dict[0].grid(which='minor', axis='x', alpha=0.3)
        self.track_main_ax.grid(which='major', axis='y', alpha=0.8)
        self.track_main_ax.grid(which='minor', axis='y', alpha=0.3)

    def define_scales(self, curve_name, graph_inst, ax):
        # Adjust scale and ranges for particular curves.
        if curve_name in ['ResistivityDeep', 'ResistivityShallow', 'ResistivityMicro',
                          'sPI_RU', 'sPI_RU_predicted', 'PERM']:
            ax.set_xscale('log')
            ax.set_xlim(0.1, 10000)
        if curve_name in ['Density']:
            ax.set_xlim(1.95, 2.95)
            ax.invert_xaxis()
        if curve_name in ['Sonic']:
            ax.set_xlim(40, 100)
        if curve_name in ['Neutron']:
            ax.set_xlim(-0.15, 0.45)
        if curve_name in ['PhotoelectricFactor']:
            ax.set_xlim(1, 6)
        if curve_name in ['Caliper', 'Bitsize']:
            ax.set_xlim(8, 21)
        if curve_name in ['sPI_RU']:
            ax.set_xlim(0.002, 200)
        if curve_name in ['sPI_RU_predicted']:
            ax.set_xlim(0.002, 200)
        if curve_name in ['log_sPI_RU_predicted']:
            ax.set_xlim(np.log10(0.002), np.log10(200))

        # Add fill between curve and maximum/minimum value or between curves.
        if curve_name in ['sPI_RU']:
            ax.fill_betweenx(self.df['Depth'], self.df[curve_name], color='skyblue', alpha=0.4)

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


class PetrophysicalLayout:
    """This class serves as a base object for layout. To instantiate this class,
    a tracklist in the form of a dictionary must be provided. Additionally, a pandas
    DataFrame is required for initialization. The column names in the DataFrame must
    match the keys in the <<curves>> section of the dictionary."""

    base_tracks_description = [
        {'type': 'main',
         'curves': {'GR': {'type': 'continuous', 'color': 'magenta', 'label': 'Gamma Ray, gapi'},
                    'RGK_CGR': {'type': 'continuous', 'color': 'orange', 'label': 'Relative (K+Th), gapi'},
                    },
         },
        {'type': 'normal',
         'curves': {'Caliper': {'type': 'continuous', 'color': 'black', 'label': 'Caliper, in'},
                    'Bitsize': {'type': 'continuous', 'color': 'red', 'label': 'Bit-size, in'},
                    },
         },
        {'type': 'normal',
         'curves': {'Density': {'type': 'continuous', 'color': 'brown', 'label': 'Density log, g/cm3'},
                    'Sonic': {'type': 'continuous', 'color': 'green', 'label': 'Sonic log, us/ft'},
                    'Neutron': {'type': 'continuous', 'color': 'blue', 'label': 'Neutron log, v/v'},
                    'PhotoelectricFactor': {'type': 'continuous', 'color': 'purple', 'label': 'PE, b/e'},
                    },
         },
        {'type': 'normal',
         'curves': {'ResistivityDeep': {'type': 'continuous', 'color': 'black', 'label': 'Deep resistivity, ohm*m'},
                    'ResistivityShallow': {'type': 'continuous', 'color': 'red', 'label': 'Medium resistivity, ohm*m'},
                    'ResistivityMicro': {'type': 'continuous', 'color': 'orange', 'label': 'Micro resistivity, ohm*m'},
                    },
         },
        {'type': 'normal',
         'curves': {
             'log_sPI_RU_predicted': {'type': 'continuous', 'color': 'blue', 'label': 'log specific PI predicted'},
             'sPI_RU_predicted': {'type': 'continuous', 'color': 'red', 'label': 'specific PI predicted'},
             'sPI_RU': {'type': 'continuous', 'color': 'black', 'label': 'specific PI'},
             },
         },
        {'type': 'normal',
         'curves': {'POR': {'type': 'continuous', 'color': 'blue', 'label': 'Porosity, v/v'},
                    'PERM': {'type': 'continuous', 'color': 'red', 'label': 'Permeability, mD'},
                    },
         },
    ]

    def __init__(self, df, tracks_description=None, depth_range=(-9999.25, 100)):

        self.df = df

        if tracks_description is None:
            self.tracks_description = self.base_tracks_description
        else:
            self.tracks_description = tracks_description

        self.tracks_number = len(self.tracks_description)

        self.depth_range = depth_range
        self.integrity_test = None
        self.tracks_dict = {}

        if self.check_integrity_of_data():
            self.integrity_test = True
        else:
            self.integrity_test = False

        if self.integrity_test:
            self.fig, self.ax = plt.subplots(1, self.tracks_number, figsize=(20, 20))
            self.prepare_figure()

    def prepare_figure(self):
        """Prepare a figure using Matplotlib, assign a number of axes to plot tracks based
        on the provided dictionary, and propagate the data to the created axes."""

        df_dropped = self.df.dropna(thresh=3)
        # Set depth range if depth range is not specified by user.
        if self.depth_range == (-9999.25, 100):
            self.depth_range = (df_dropped['Depth'].min() - 15, df_dropped['Depth'].max() + 15)

        for track_id, track in enumerate(self.tracks_description):
            self.tracks_dict.update({track_id: PetrophysicalTrack(track['curves'],
                                                                  self.ax[track_id],
                                                                  track['type'],
                                                                  self.df,
                                                                  self.depth_range)})
        self.fig.suptitle(f"Layout of {self.df['Well'].unique()[0]}", fontsize=18, ha='left', x=0.0)
        self.fig.tight_layout()

    def check_integrity_of_data(self) -> bool:
        """This function checks data integrity before starting the program. It returns True if
        the data is complete or nearly complete, and False if any essential information is missing."""
        # Check if Depth exists
        if 'Depth' not in self.df.columns:
            print('There is no principal curve to plot. Pray ensure that the initial set doth contain <<Depth>>.')
            return False
        return True
