# XYFigure Dictionary

## Main XYFigure Dictionary

The XYFigure dictionary is the main dictionary.  It is composed of one or more `model` dictionaries, followed by a single `view` dictionary.

Key | Value | Description 
--- | ----- | -----------
`"model_name":` | `{...}` | A unique `string`.  Contains the [`model` dictionary](#model-dictionary).  Non-singleton; supports `1..n` models.
`"view_name":` | `{...}` | A unique `string`.  Contains the [`view` dictionary](#view-dictionary).  Singleton, supports only `1` view.

### Model Dictionary

The model dictionary contains items that describe how each `(x,y)` data set is constructed and shown on the view.  

Key | Value | Description 
--- | ----- | -----------
`"class":` | `"model"` | Specific string to generate the XYModel Python class.
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the input data.  For the current working directory, use `"."`.
`"file":` | string | Value of the comma separated value input file in `.csv` (comma separated value) format.  The first column is the `x` values, the second column is the `y` values.  The `.csv` file can use any number of header rows.  Do not attempt to plot header rows; skip header rows with the `skip_rows` key.
`"skip_rows":` | integer | *optional*<br>The number of header rows to skip upon reading in the `.csv` file.  Default value is `0`.
`"inverted":` | Boolean | *optional*<br>Set to `1` to invert the `y` data; will multiplying all `y` data values by `-1`.  Default value is `0`, which does *not* invert the `y` values.
`"xoffset":` | float | *optional*<br>Shifts all values of the `x` data to the left or the right by the `xoffset` value.  Default value is `0.0`.
`"plot_kwargs":` | `{...}` | Singleton that contains the [plot keywords dictionary](#plot-keywords-dictionary).

#### Plot Keywords Dictionary

Dictionary that overrides the [`matplotlib.pyplot.plot()` kwargs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html) default values.  Default values used by XYModel follow:

Key | Value | Description 
--- | ----- | -----------
`"linewidth":` | float | *optional*<br> Default value is `2`.
`"linestyle":` | string | *optional*<br>Default value is `"-"`, which is a solid line. See [matplotlib linestyles](https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html) for more detail.

Some frequently used *optional values* follow:

Key | Value | Description 
--- | ----- | -----------
`"label":` | string | *optional*<br>The string appearing in the legend correponding to the data.
`"color:"` | string | *optional*<br>The [matplotlib color](https://matplotlib.org/3.1.1/tutorials/colors/colors.html) used to plot the data.
`"alpha":` | float | *optional*<br>Real number in the range from `0` to `1`. Numbers toward `0` are more transparent and numbers toward `1` are more opaque.  

### View Dictionary

The view dictionary contains items that describe how the main figure is constructed.

Key | Value | Description 
--- | ----- | -----------
`"class":` | `"view"` | Specific string to generate the XYView Python class.
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the output figure data (if `"serialize"` is set to `"1"`).  For the current working directory, use `"."`.
`"file":` | string | Value of the out file in `.xxx` format, where `xxx` is an image file format, typically `pdf`, `png`, or `svg`.  
`"figure_args":` | string | *optional*<br>
`"title":` | string | *optional*<br>
`"xlabel":` | string | *optional*<br>
`"ylabel":` | string | *optional*<br>
`"xticks":` | string | *optional*<br>
`"yticks":` | string | *optional*<br>
`"yaxis_rhs":` | string | *optional*<br>
`"background-image":` | string | *optional*<br>
`"display":` | string | *optional*<br>
`"latex":` | string | *optional*<br>
`"serialize":` | string | *optional*<br>

#### yaxis_rhs Dictionary

Key | Value | Description 
--- | ----- | -----------
`"scale":` | string | *optional*<br>
`"label":` | string | *optional*<br>
`"yticks":` | string | *optional*<br>

#### background-image Dictionary

Key | Value | Description 
--- | ----- | -----------
`"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the background image file.  For the current working directory, use `"."`.
`"file":` | string | Value of the background image file, typically in `png` format.
`"left":` | float | Left-side extent of image in plot `x` coordinates.   Must be less than the right-side extent.
`"right":` | float | Right-side extent of image in plot `x` coordinates.  Must be greater than the left-side extent.
`"bottom":` | float | Bottom-side extent of image in plot `y` coordinates.   Must be less than the top-side extent.
`"top":` | float | Top-side extent of image in plot `y` coordinates.  Must be greater than the bottom-side extent.

