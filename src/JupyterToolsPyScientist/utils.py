import os
import pandas as pd
import ctypes

current_dir = os.path.dirname(os.path.abspath(__file__))
assignment_base_path = os.path.join(current_dir, 'assignment_base.xlsx')


def load_tracks_description(where=None):
    """Function to parse excel with track descriptions and provide dictionary in appropriate format which
    is need fpr farther processing.
    :param where: Path to the Excel file with data on "tracks_description" page. If file is not provided, then
    is used the assignment_base file.
    """
    if (where is not None) and os.path.isfile(where):
        file_path = where
    else:
        file_path = assignment_base_path

    if os.path.isfile(file_path):
        df = pd.read_excel(file_path, sheet_name='tracks_description')
        df_tracks = df.groupby('track_number')
        tracks_names = df_tracks.groups.keys()
        tracks_description_base = []
        for track_name in tracks_names:
            group = df_tracks.get_group(track_name)
            curves_dict = {}
            for _ in range(len(group['curve'].values)):
                curves_dict.update({
                    group['curve'].values[_]: {
                        'curve_type': group['curve_type'].values[_],
                        'color': group['color'].values[_],
                        'label': group['label'].values[_],
                        'unit': group['unit'].values[_],
                        'min': group['min'].values[_],
                        'max': group['max'].values[_],
                        'scale': group['scale'].values[_],
                        'reverse': group['reverse'].values[_],
                        'range_detection': group['range_detection'].values[_],
                         }
                   }
                )
            tracks_description_base.append({'type': group['track_type'].values[0],
                                            'curves': curves_dict})
    else:
        return []
    return tracks_description_base


def load_mnemonic_aliases_correspond(where=None):
    """Function to parse excel table with aliases and mnemonic correspondence and provide dictionary in format which
    is need fpr farther processing.
    :param where: Path to the Excel file with data on "aliases" page. If file is not provided, then
    is used the assignment_base file.
    """
    if (where is not None) and os.path.isfile(where):
        file_path = where
    else:
        file_path = assignment_base_path

    if os.path.isfile(file_path):
        mnemonic_dict = {}
        df = pd.read_excel(file_path, sheet_name='aliases')
        for _, row in df.iterrows():
            mnemonic_dict.update({row['name']: row['aliases'].replace(' ', '').split(',')})
    else:
        return {}
    return mnemonic_dict
