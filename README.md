Package "JupyterToolsPyScientist" dedicated to provide
convenient framework for application of ML learning for petrophysical
studies.

Currently implemented two main modules:

1) jupyter_tools - standard name for input is jt
2) petrophysical_layout - standard name for input is pl

<h3>"jupyter_tools" module</h3>

<h3>"petrophysical_layout" module</h3>

Main class of module is "PetrophysicalLayout" which provides
easy to use methods to plot well-logging data from las. Plotting is based on matplotlib package.

Function "create_single_well_df" of module dedicated for transformation of las file
into DataFrame with standardised curve names. For transparent procedure of the data transformation is used
assignment file with correspondence names need to be used in dataframe and aliases in lasfile.

![Alt text](docs/example_of_track_desription.png?raw=true "Title")

df = create_single_well_df(las_file_path, assignment_file_path)

where:

las_file_path: str - path to las file from which we are going to prepare composite df.

assignment_file_path: str [Optional] - Path to assignment Excel file with TAB "aliases". If file isn't specified
than the program takes default one. The example of default file provided on the figure above.

After the creation of composite df it can be applied its processing to calculate porosity, water saturation,
vsh, and other parameters. This available by function "make_processing_well_logging".

make_processing_well_logging(df)

where:

df: pd.DataFrame - is DataFrame for which processing will be applied.


![Alt text](docs/example_of_aliases.png?raw=true "Title")

After creation of composite DataFrame and following it processing (if it needs) can be created the instance of "PetrophysicalLayout" for which can be defined the depth range, assignment file path with description how to compose tracks in layout and mode in which the layout will be created.
The "active" mode is appropriate while we are going to work from console, then 'passive' mode, which we got as default value can be used to plot layout inside jupyter notebook.

PetrophysicalLayout(df,
                    assignment_file_path=self.assignment_test_path,
                    depth_range=(1000, 5700),
                    mode='active')

where:

assignment_file_path: str [Optional] - Path to assignment Excel file with TAB "aliases". If file isn't specified than the program takes default one. The example of default file provided on the figure above. 

depth_range: tuple [Optional] - Depth range can be specified in form of tuple (min, max) or if "None" is specified by the default, then use min and max depth curve in dataset to determine limits of plotting.

mode: str [Optional] - By the default mode is 'passive' in this mode figure can be plotted inside jupyter, another option to set it 'active' so it can be used from command line to plot the figure.