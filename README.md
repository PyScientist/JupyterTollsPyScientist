<h3>Package "JupyterToolsPyScientist" dedicated to provide
convenient framework for application of ML learning for petrophysical
studies.</h3>

Currently implemented two main modules:

1) jupyter_tools - standard name for import is jt
2) petrophysical_layout - standard name for import is pl

<h3>"jupyter_tools" module</h3>

Jupyter tools provided tools for:
1) Random forest model generation;
2) Graphical comparison of model performance;
3) Grid score custom visualization.

At present, it is under development and should be described better soon. 

<h3>"petrophysical_layout" module</h3>

Module petrophysical_layout is imported from package JupyterToolsPyScientist.

    from JupyterToolsPyScientist import petrophysical_layout as pl

Main class of module is "PetrophysicalLayout" which provides
easy to use methods to plot well-logging data from las. Plotting is based on matplotlib package.

Function "create_single_well_df" of module dedicated for transformation of las file
into DataFrame with standardised curve names. For transparent procedure of the data transformation is used
assignment file with correspondence names need to be used in dataframe and aliases in lasfile.

![Alt text](docs/example_of_aliases.png?raw=true "Title")

    df = pl.create_single_well_df(las_file_path, assignment_file_path)

where:

las_file_path: str - path to las file from which we are going to prepare composite df.

assignment_file_path: str [Optional] - Path to assignment Excel file with TAB - "aliases". If file isn't specified
than the program takes default one. The example of default file provided on the figure above.

After a composite DataFrame creation it can be performed its processing to calculate volume of shale, porosity, water saturation,
vsh, and other parameters. This available by function "make_processing_well_logging".

    pl.make_processing_well_logging(df)

where:

df: pd.DataFrame - is DataFrame for which processing will be applied.

At present available calculations of density and resistivity porosity using predefined constants:

    matrix_density = 2.71
    fluid_density = 1
    a = 1
    m = 2
    rw = 0.6

As continuation of processing technique should be added additional method and possibility of
constant adjusting.

![Alt text](docs/example_of_track_desription.png?raw=true "Title")

After composite DataFrame creation, and it's following processing to calculate volume of shale, porosity, saturation, etc. ... (if it needs) can be created the instance of "PetrophysicalLayout" for which can be defined the depth range, assignment file path with description how to compose tracks in layout and mode in which the layout will be created.
The "active" mode is appropriate while we are going to work from console, then 'passive' mode, which we got as default value can be used to plot layout inside jupyter notebook.

    PetrophysicalLayout(df,
                        assignment_file_path=assignment_test_path, 
                        depth_range=(4000, 4650),
                        mode='passive')

where:

assignment_file_path: str [Optional] - Path to assignment Excel file with TAB - "tracks description". If file isn't specified than the program takes default one. The example of default file provided on the figure above. It available in directory ".tests/test_dataset"

depth_range: tuple [Optional] - Depth range can be specified in form of tuple (min, max) or if "None" is specified by the default, then use min and max depth curve in dataset to determine limits of plotting.

mode: str [Optional] - By the default mode is 'passive' in this mode figure can be plotted inside jupyter, another option to set it 'active' so it can be used from command line to plot the figure.

On the figure below is provided the result of script performance.

![Alt text](docs/Example_of_plot_Kanzas_las_dataset.png?raw=true "Title")