# XYFigure Dictionary

## Main XYFigure Dictionary

The XYFigure dictionary is the main dictionary.  It is composed of one or more `model` dictionaries, followed by a single `view` dictionary.

Key | Value | Description 
--- | ----- | -----------
`"model_name":` | dict | A unique `string`.  Contains the [`model` dictionary](#model-dictionary).  Non-singleton; supports `1..n` models.
`"view_name":` | dict  | A unique `string`.  Contains the [`view` dictionary](#view-dictionary).  Singleton, supports only `1` view.

### Model Dictionary

The model dictionary contains items that describe how each `(x,y)` data set is constructed and shown on the view.  

Key | Value | Description 
--- | ----- | -----------
`"class":` | `"model"` | Specific string to generate the XYModel Python class.
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the input data.  For the current working directory, use `"."`.
`"file":` | string | Value of the comma separated value input file in `.csv` (comma separated value) format.  The first column is the `x` values, the second column is the `y` values.  The `.csv` file can use any number of header rows.  Do not attempt to plot header rows; skip header rows with the `skip_rows` key.
`"skip_rows":` | integer | *optional*<br>The number of header rows to skip upon reading in the `.csv` file.  Default value is `0`.
`"inverted":` | Boolean | *optional*<br>`0` (default), which does **not** invert the `y` values.<br>`1` to invert the `y` data.  Multiplies all `y` data values by `-1`.
`"xoffset":` | float | *optional*<br>Shifts all values of the `x` data to the left or the right by the `xoffset` value.  Default value is `0.0`.
`"plot_kwargs":` | dict | Singleton that contains the [plot keywords dictionary](#plot-keywords-dictionary).

#### Plot Keywords Dictionary

Dictionary that overrides the [`matplotlib.pyplot.plot()` kwargs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html) default values.  Default values used by XYModel follow:

Key | Value | Description 
--- | ----- | -----------
`"linewidth":` | float | *optional*<br> Default value is `2.0`. See [matplotlib lines Line2D](https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D) for more detail.
`"linestyle":` | string | *optional*<br>Default value is `"-"`, which is a solid line. See [matplotlib linestyles](https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html) for more detail.
| | |Some frequently used *optional values* follow:
`"label":` | string | *optional*<br>The string appearing in the legend correponding to the data.
`"color:"` | string | *optional*<br>The [matplotlib color](https://matplotlib.org/3.1.1/tutorials/colors/colors.html) used to plot the data.
`"alpha":` | float | *optional*<br>Real number in the range from `0` to `1`. Numbers toward `0` are more transparent and numbers toward `1` are more opaque.  

### View Dictionary

The view dictionary contains items that describe how the main figure is constructed.

Key | Value | Description 
--- | ----- | -----------
`"class":` | `"view"` | Specific string to generate the XYView Python class.
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the output figure data (if `"serialize"` is set to `"1"`).  For the current working directory, use `"."`.  If the folder does not exist at run time, the script will attempt to create the directory, pending the user's approval.
`"file":` | string | Value of the figure output file (e.g., `my_output_file.png`) in `.xxx` format, where `xxx` is an image file format, typically `pdf`, `png`, or `svg`.  
`"figure_args":` | string | *optional*<br>
`"title":` | string | *optional*<br>Figure label, top and centered.  Default is the base name of the `.json` input file, followed by the timestamp of the figure creation in `yyyy-mm-dd hh:mm:ss` format.
`"xlabel":` | string | *optional*<br>The label for the x-axis.  Default is `default x axis label`.
`"ylabel":` | string | *optional*<br>The label for the left-hand y-axis.  Default is `default y axis label.`
`"xticks":` | string | *optional*<br>Contains an array of ascending real numbers, indicating tick placement.  May use all of the `numpy` syntax.  Example: `"[0, 0.50, np.pi/4, 1, np.pi/2, 2]"`.  Default is matplotlib's choice for tick marks.
`"yticks":` | string | *optional*<br>Same as documentation for `xticks`.
`"yaxis_rhs":` | dict | *optional*<br>Singleton that contains the [yaxis_rhs dictionary](#yaxis_rhs-dictionary).
`"background_image":` | dict | *optional*<br>Singleton that contains the [background_image dictionary](#background_image-dictionary).
`"display":` | Boolean | *optional*<br>`0` to suppress showing figure in GUI, useful when serializing multiple figures during a parameter search loop.<br>`1` (default value) to show figure interactively, and to pause script execution.
`"latex":` | string | *optional*<br>`0` (default) uses matplotlib default fonts, results in fast generation of figures.<br>`1` uses LaTeX fonts, can be slow to generate, but produces production-quality results.
`"serialize":` | string | *optional*<br>`0` (default) does **not** save figure to the file system.<br>`1` saves figure to the file system.  Tested on local drives, but not on network drives.

#### yaxis_rhs Dictionary

Key | Value | Description 
--- | ----- | -----------
`"scale":` | string | *optional*<br>The factor that multiplies the left-hand y-axis to produce the right-hand y-axis.  For example, if the left-hand y-axis is in `meters`, and the right-hand y-axis is in `centimeters`, the value of `scale` should be set to `100`.  Default value is `1`.
`"label":` | string | *optional*<br>The right-hand-side y-axis label.  Default is an empty string (`None`).
`"yticks":` | string | *optional*<br>Same as documentation for `xticks`.

#### background_image Dictionary

Key | Value | Description 
--- | ----- | -----------
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the background image file.  For the current working directory, use `"."`.
`"file":` | string | Value of the background image file name, typically in `png` format.
`"left":` | float | *optional*<br>Left-side extent of image in plot `x` coordinates.   Must be less than the right-side extent.  Default is `0.0`.
`"right":` | float | *optional*<br>Right-side extent of image in plot `x` coordinates.  Must be greater than the left-side extent. Default is `1.0`.
`"bottom":` | float | *optional*<br>Bottom-side extent of image in plot `y` coordinates.   Must be less than the top-side extent. Default is `0.0`.
`"top":` | float | *optional*<br>Top-side extent of image in plot `y` coordinates.  Must be greater than the bottom-side extent.  Default is `1.0`.

