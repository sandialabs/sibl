# XYFigure Dictionary

Below are dictionary `"key": value` pairs, followed by a description, for each of the XYFigure dictionary constitutents.

## Main XYFigure Dictionary

The XYFigure dictionary is the main dictionary.  It is composed of one or more [`model` dictionaries](#model-dictionary), followed by a single [`view` dictionary](#view-dictionary).

|     |
| --- |
| `"model_name":` dict<br><br>A unique `string`.  Contains the [`model` dictionary](#model-dictionary).  Non-singleton; supports `1..n` models.
| `"view_name":` dict<br><br>A unique `string`.  Contains the [`view` dictionary](#view-dictionary).  Singleton, supports only `1` view.<br>**Note:** In general, this `"view_name"` key can be any unique string.  However, when the `.json` input file is to be used with the unit tests, this `"view_name"` key string must be exactly set to `"figure"` for the unit tests to work properly.

### Model Dictionary

The model dictionary contains items that describe how each `(x,y)` data set is constructed and shown on the view.  

|     |
| --- |
| `"class": "model"`<br><br>Specific string to generate the XYModel Python class.
| `"folder":` string <br><br>Value *relative to the current working directory* of the path and folder that contains the input data.  For the current working directory, use `"."`.
| `"file":` string <br><br>Value of the comma separated value input file in `.csv` (comma separated value) format.  The first column is the `x` values, the second column is the `y` values.  The `.csv` file can use any number of header rows.  Do not attempt to plot header rows; skip header rows with the `skip_rows` key.
| `"skip_rows":` integer <br><br>*optional*<br>The number of header rows to skip at the *beginning* of the `.csv` file.  Default value is `0`.
| `"skip_rows_footer":` integer <br><br>*optional*<br>The number of footer rows to skip at the *end* of the `.csv` file.  Default value is `0`.
| `"xcolumn":` integer <br><br>*optional*<br>The *zero-based index* of the data column to plotted on the x-axis.  Default is `0`, which is the **first column** of the `.csv` file.
| `"ycolumn":` integer <br><br>*optional*<br>The *zero-based index* of the data column to be plotted on the y-axis.  Default is `1`, which is the **second column** of the `.csv` file.
| ~~`"inverted":`~~ ~~Boolean~~ <br><br>**deprecated**<br>use `"yscale": -1.0` instead<br>~~*optional*~~<br>~~`0` (default), which does **not** invert the `y` values.<br>`1` to invert the `y` data.  Multiplies all `y` data values by `-1`.~~
| `"xscale":` float <br><br>*optional*<br>Scales all values of the `x` data `xscale` factor.  Default value is `1.0` (no scaling).  `xscale` is applied to the data prior to `xoffset`.
| `"xoffset":` float <br><br>*optional*<br>Shifts all values of the `x` data to the left or the right by the `xoffset` value.  Default value is `0.0`.  `xoffset` is applied to the data after `xscale`.
| `"yscale":` float <br><br>*optional*<br>Scales all values of the `y` data `yscale` factor.  Default value is `1.0` (no scaling).  `yscale` is applied to the data prior to `yoffset`.
| `"yoffset":` float <br><br>*optional*<br>Shifts all values of the `y` data up or down by the `yoffset` value.  Default value is `0.0`.  `yoffset` is applied to the data after `yscale`.
| `"plot_kwargs":` dict <br><br>Singleton that contains the [plot keywords dictionary](#plot-keywords-dictionary).

#### Plot Keywords Dictionary

Dictionary that overrides the [`matplotlib.pyplot.plot()` kwargs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html) default values.  Default values used by XYModel follow:

|     |
| --- |
| `"linewidth":` float <br><br>*optional*<br> Default value is `2.0`. See [matplotlib lines Line2D](https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D) for more detail.
| `"linestyle":` string <br><br>*optional*<br>Default value is `"-"`, which is a solid line. See [matplotlib linestyles](https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html) for more detail.
| <br>> *Some frequently used *optional values* follow.<br>> If the keys are omitted, then the matplotlib defaults are used.*<br><br>
| `"marker":` string <br><br>*optional*<br>The string to designate a marker at the data point.  See [matplotlib marker](https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers) documentation.
| `"label":` string <br><br>*optional*<br>The string appearing in the legend correponding to the data.
| `"color:"` string <br><br>*optional*<br>The [matplotlib color](https://matplotlib.org/3.1.1/tutorials/colors/colors.html) used to plot the data.  Also, [predefined color](https://matplotlib.org/3.1.0/gallery/color/named_colors.html) names.
| `"alpha":` float <br><br>*optional*<br>Real number in the range from `0` to `1`. Numbers toward `0` are more transparent and numbers toward `1` are more opaque.  

### View Dictionary

The view dictionary contains items that describe how the main figure is constructed.

|     |
| --- |
| `"class":` `"view"` <br><br>Specific string to generate the XYView Python class.
| `"folder":` string <br><br>Value *relative to the current working directory* of the path and folder that contains the output figure data (if `"serialize"` is set to `"1"`).  For the current working directory, use `"."`.  If the folder does not exist at run time, the script will attempt to create the directory, pending the user's approval.
| `"file":` string <br><br>Value of the figure output file (e.g., `my_output_file.png`) in `.xxx` format, where `xxx` is an image file format, typically `pdf`, `png`, or `svg`.  
| `"size":` float array <br><br>*optional*<br>Array of floats containing the `[width, height]` of the output figure in units of inches.  Default is `[11.0, 8.5]`, U.S. paper, landscape.  [Example](test/README_dpi_size.md)
| `"dpi":` integer <br><br>*optional*<br>Dots per inch used for the output figure.  Default is `300`. [Example](test/README_dpi_size.md)
| `"xlim":` float array <br><br>*optional*<br>Array of floats containing the x-axis bounds `[x_min, x_max]`.  Default is matplotlib's automatic selection.
| `"ylim":` float array <br><br>*optional*<br>Array of floats containing the y-axis bounds `[y_min, y_max]`.  Default is matplotlib's automatic selection.
| `"title":` string <br><br>*optional*<br>Figure label, top and centered.  Default is `default title`. 
| `"xlabel":` string <br><br>*optional*<br>The label for the x-axis.  Default is `default x axis label`.
| `"ylabel":` string <br><br>*optional*<br>The label for the left-hand y-axis.  Default is `default y axis label`.
| `"xticks":` float array <br><br>*optional*<br>Contains an array of ascending real numbers, indicating tick placement.  Example: `[0.0, 0.5, 1.0, 1.5, 2.0]`.  Default is matplotlib's choice for tick marks.
| `"yticks":` float array <br><br>*optional*<br>Same as documentation for `xticks`.
| `"yaxis_rhs":` dict <br><br>*optional*<br>Singleton that contains the [yaxis_rhs dictionary](#yaxis_rhs-dictionary).
| `"background_image":` dict <br><br>*optional*<br>Singleton that contains the [background_image dictionary](#background_image-dictionary).
| `"display":` Boolean <br><br>*optional*<br>`0` to suppress showing figure in GUI, useful when serializing multiple figures during a parameter search loop.<br>`1` (default value) to show figure interactively, and to pause script execution.
| `"latex":` string <br><br>*optional*<br>`0` (default) uses matplotlib default fonts, results in fast generation of figures.<br>`1` uses LaTeX fonts, can be slow to generate, but produces production-quality results.
| `"details"`: Boolean <br><br>*optional*<br>`0` do **not** show plot details.<br>`1` (default) shows plot details of figure file name, date (`yyyy-mm-dd` format), and time (`hh:mm:ss` format) the figure was generated, and username.
| `"serialize":` string <br><br>*optional*<br>`0` (default) does **not** save figure to the file system.<br>`1` saves figure to the file system.  Tested on local drives, but not on network drives.

#### yaxis_rhs Dictionary
|     |
| --- |
| `"scale":` string <br><br>*optional*<br>The factor that multiplies the left-hand y-axis to produce the right-hand y-axis.  For example, if the left-hand y-axis is in `meters`, and the right-hand y-axis is in `centimeters`, the value of `scale` should be set to `100`.  Default value is `1`.
| `"label":` string <br><br>*optional*<br>The right-hand-side y-axis label.  Default is an empty string (`None`).
| `"yticks":` float array <br><br>*optional*<br>Same as documentation for `xticks`.

#### background_image Dictionary

|     |
| --- |
| `"folder":` string <br><br>Value *relative to the current working directory* of the path and folder that contains the background image file.  For the current working directory, use `"."`.
| `"file":` string <br><br>Value of the background image file name, typically in `png` format.
| `"left":` float <br><br>*optional*<br>Left-side extent of image in plot `x` coordinates.   Must be less than the right-side extent.  Default is `0.0`.
| `"right":` float <br><br>*optional*<br>Right-side extent of image in plot `x` coordinates.  Must be greater than the left-side extent. Default is `1.0`.
| `"bottom":` float <br><br>*optional*<br>Bottom-side extent of image in plot `y` coordinates.   Must be less than the top-side extent. Default is `0.0`.
| `"top":` float <br><br>*optional*<br>Top-side extent of image in plot `y` coordinates.  Must be greater than the bottom-side extent.  Default is `1.0`.
| `"alpha":` float <br><br>*optional*<br>Real number in the range from 0 to 1. Numbers toward 0 are more transparent and numbers toward 1 are more opaque.  Default is `1.0` (fully opaque, no transparency).
