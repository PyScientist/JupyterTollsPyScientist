import numpy as np


class Calculator:
    """Class of calculator which provides methods for calculation different petrophysical properties"""
    def __init__(self):
        pass

    @staticmethod
    def porosity_density(row, matrix_density, fluid_density, input_mnem_dens):
        """Method for calculation porosity by density log using bulk density"""
        if not np.isnan(row[input_mnem_dens]):
            return (matrix_density - row[input_mnem_dens])/(matrix_density-fluid_density)
        else:
            return np.nan

    @staticmethod
    def porosity_resistivity(row, a, m, rw, input_mnem_resist):
        """Method for calculation porosity by resistivity log using deep resistivity"""
        if not np.isnan(row[input_mnem_resist]):
            return (a*rw)/(m*row[input_mnem_resist])
        else:
            return np.nan
