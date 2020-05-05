# XYFigure Dictionary

Below are dictionary `"key": value` pairs, followed by a description, for each of the XYFigure dictionary constitutents.

## Main XYFigure Dictionary

The XYFigure dictionary is the main dictionary.  

* It is stored in an ordinary text file in `.json` format.
* It is composed of one or more [`model` dictionaries](#model-dictionary), followed by one or more [`view` dictionaries](#view-dictionary).

|     |     |     |
| --- | --- | --- |
| `"model_name":` | dict | The key `"model_name"` is a `string` that must be a globally unique identifier (`guid`) in the `.json` file.  Contains the [`model` dictionary](#model-dictionary).  Non-singleton; supports `1..m` models.
| `"view_name":`  | dict | The key `"view_name"` is a `string` that must be a globally unique identifier (`guid`) in the `.json` file.  The key Contains the [`view` dictionary](#view-dictionary).  Non-singleton, supports `1..n` views.<br><br>**Note:** In general, this `"view_name"` key can be any unique string.  However, when the `.json` input file is to be used with the unit tests, this `"view_name"` key string must be exactly set to `"figure"` for the unit tests to work properly.

There are three common variations to the XYFigure dictionary:

* **1:1** 
  * One model
  * One view
  * This is the most basic option.
* **1:n** 
  * Several models
  * One view
  * This is an advanced option, wherein multiple models are plotted to the same figure.  Considerations such as y-axis limits or the possibility of dual y-axes can become important.
* **m:n** 
  * Several models
  * Several views
  * This is the most advanced combination of the three, where all the models are created, and views explicity specify which models get plotted to a particular figure.

Signal processing may be performed on one or more models, using the [`signal_process` dictionary](#signal-processing-keywords-dictionary), to create a new model, which can also be used by the view.  A conceptual flow diagram of multiple models, one with signal processing, and one view is shown below. 


    ┌───────────────┐                                                    ┌───────────────┐
    │     Model     │─────────────────────────┐                          │               │
    └───────────────┘                         │                          │               │
                                              │                          │               │
    ┌───────────────┐                         │                          │               │
    │     Model     │─────────────────────────┤                          │               │
    └───────────────┘                         │                          │               │
            │                                 │                          │     View      │ 
                                              ├─────────────────────┬───▶│               │
            │                                 │                     │    │               │
    ┌───────────────┐                         │                     │    │               │
    │     Model     │──┬──────────────────────┘                     │    │               │
    └───────────────┘  │   ┌───────────────┐                        │    │               │
                       │   │    Signal     │    ┌───────────────┐   │    │               │
                       └──▶│    Process    │───▶│     Model     │───┘    │               │
                           └───────────────┘    └───────────────┘        └───────────────┘


### Model Dictionary

The model dictionary contains items that describe how each `(x,y)` data set is constructed and shown on the view.  

|     |     |     |
| --- | --- | --- |
| `"class":`            | `"model"` | Specific string to generate the XYModel Python class.  In the model dictionary, the `"class"` key  must have a value of `"model"`.
| `"folder":`           | string    | Value *relative to the current working directory* of the path and folder that contains the input data.  For the current working directory, use `"."`.
| `"file":`             | string    | Value of the comma separated value input file in `.csv` (comma separated value) format.  The first column is the `x` values, the second column is the `y` values.  The `.csv` file can use any number of header rows.  Do not attempt to plot header rows; skip header rows with the `skip_rows` key.
| `"skip_rows":`        | integer   | *optional*<br>The number of header rows to skip at the *beginning* of the `.csv` file.  Default value is `0`.
| `"skip_rows_footer":` | integer   | *optional*<br>The number of footer rows to skip at the *end* of the `.csv` file.  Default value is `0`.
| `"xcolumn":`          | integer   | *optional*<br>The *zero-based index* of the data column to plotted on the x-axis.  Default is `0`, which is the **first column** of the `.csv` file.
| `"ycolumn":`          | integer   | *optional*<br>The *zero-based index* of the data column to be plotted on the y-axis.  Default is `1`, which is the **second column** of the `.csv` file.
| ~~`"inverted":`~~     | ~~Boolean~~ | **deprecated**<br>use `"yscale": -1.0` instead<br>~~*optional*~~<br>~~`0` (default), which does **not** invert the `y` values.<br>`1` to invert the `y` data.  Multiplies all `y` data values by `-1`.~~
| `"xscale":`           | float     |*optional*<br>Scales all values of the `x` data `xscale` factor.  Default value is `1.0` (no scaling).  `xscale` is applied to the data prior to `xoffset`.
| `"xoffset":`          | float     | *optional*<br>Shifts all values of the `x` data to the left or the right by the `xoffset` value.  Default value is `0.0`.  `xoffset` is applied to the data after `xscale`.
| `"yscale":`           | float     | *optional*<br>Scales all values of the `y` data `yscale` factor.  Default value is `1.0` (no scaling).  `yscale` is applied to the data prior to `yoffset`.
| `"yoffset":`          | float     | *optional*<br>Shifts all values of the `y` data up or down by the `yoffset` value.  Default value is `0.0`.  `yoffset` is applied to the data after `yscale`.
| `"plot_kwargs":`      | dict      | Singleton that contains the [plot keywords dictionary](#plot-keywords-dictionary).
| `"signal_process":`   | dict      | Singleton that contains the [signal processing keywords dictionary](#signal-processing-keywords-dictionary).

#### Plot Keywords Dictionary

Dictionary that overrides the [`matplotlib.pyplot.plot()` kwargs](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html) default values.  Default values used by XYModel follow:

|     |     |     |
| --- | --- | --- |
| `"linewidth":` | float  | *optional*<br> Default value is `2.0`. See [matplotlib lines Line2D](https://matplotlib.org/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D) for more detail.
| `"linestyle":` | string | *optional*<br>Default value is `"-"`, which is a solid line. See [matplotlib linestyles](https://matplotlib.org/3.1.0/gallery/lines_bars_and_markers/linestyles.html) for more detail.
|                |        | *Some frequently used *optional values* follow.<br>If the keys are omitted, then the matplotlib defaults are used.*<br><br>
| `"marker":`    | string | *optional*<br>The string to designate a marker at the data point.  See [matplotlib marker](https://matplotlib.org/3.1.1/api/markers_api.html#module-matplotlib.markers) documentation.
| `"label":`     | string | *optional*<br>The string appearing in the legend correponding to the data.
| `"color:"`     | string | *optional*<br>The [matplotlib color](https://matplotlib.org/3.1.1/tutorials/colors/colors.html) used to plot the data.  Also, [predefined color](https://matplotlib.org/3.1.0/gallery/color/named_colors.html) names.
| `"alpha":`     | float  | *optional*<br>Real number in the range from `0` to `1`. Numbers toward `0` are more transparent and numbers toward `1` are more opaque.  

#### Signal Processing Keywords Dictionary

This dictionary is currently under active development.  For additional documentation, see

* [Butterworth filter](test/README_butterworth.md)
* [Differentiation](test/README_differentiation.md)
* [Integration](test/README_integration.md)

Below is a summary of the `"key": value` pairs available within the `signal_process` dictionary.

```bash
        "signal_process": {
            "process_guid_1": {
                "butterworth": {
                    "cutoff": 5,
                    "order": 4,
                    "type": "low"
                }
            }
            "process_guid_2": {
                "gradient": {
                    "order": 1
                }
            }
            "process_guid_3": {
                "integration": {
                    "order": 3,
                    "initial_conditions": [-10, 100, 1000]
                }
            }
            "process_guid_4": {
                "crosscorrelation": {
                    "model_keys": ["model_guid_0", "model_guid_1"],
                    "mode": "full" (or "valid" or "same")
                }
            }
            "process_guid_5: {
                "tpav": { (tpav is three-points angular velocity)
                    "model_keys": ["model_guid_0", "model_guid_1", "model_guid_2"]
                }
            }
        }      
```

All processes support serialization, via

```bash
        "signal_process": {
            "process_guid": {
                "process_key_string": {
                    "serialize": 1,
                    "folder": ".",
                    "file": "processed_output_file.csv"                
                }
            }
```

### View Dictionary

The view dictionary contains items that describe how the main figure is constructed.

|     |     |     |
| --- | --- | --- |
| `"class":`            | `"view"`    | Specific string to generate the XYView Python class. In the view dictionary, the `"class"` key must have a value of `"view"`.
| `"model_keys"`:       | string array | *optional*<br>`["model_guid_0", "model_guid_1", model_guid_2"]` (for example), an array of `1..m` strings that identifies the model `guid` to be plotted in this particular view.  If `"model_keys"` is not specified in a particular view, then all models will be plotted to the view, which is the default behavior.
| `"folder":`           | string      | Value *relative to the current working directory* of the path and folder that contains the output figure data (if `"serialize"` is set to `"1"`).  For the current working directory, use `"."`.  If the folder does not exist at run time, the script will attempt to create the directory, pending the user's approval.
| `"file":`             | string      | Value of the figure output file (e.g., `my_output_file.png`) in `.xxx` format, where `xxx` is an image file format, typically `pdf`, `png`, or `svg`.  
| `"size":`             | float array | *optional*<br>Array of floats containing the `[width, height]` of the output figure in units of inches.  Default is `[11.0, 8.5]`, U.S. paper, landscape.  [Example](test/README_dpi_size.md)
| `"dpi":`              | integer     | *optional*<br>Dots per inch used for the output figure.  Default is `300`. [Example](test/README_dpi_size.md)
| `"xlim":`             | float array | *optional*<br>Array of floats containing the x-axis bounds `[x_min, x_max]`.  Default is matplotlib's automatic selection.
| `"ylim":`             | float array | *optional*<br>Array of floats containing the y-axis bounds `[y_min, y_max]`.  Default is matplotlib's automatic selection.
| `"title":`            | string      | *optional*<br>Figure label, top and centered.  Default is `default title`. 
| `"xlabel":`           | string      | *optional*<br>The label for the x-axis.  Default is `default x axis label`.
| `"ylabel":`           | string      | *optional*<br>The label for the left-hand y-axis.  Default is `default y axis label`.
| `"xticks":`           | float array | *optional*<br>Contains an array of ascending real numbers, indicating tick placement.  Example: `[0.0, 0.5, 1.0, 1.5, 2.0]`.  Default is matplotlib's choice for tick marks.
| `"yticks":`           | float array | *optional*<br>Same as documentation for `xticks`.
| `"yaxis_rhs":`        | dict        | *optional*<br>Singleton that contains the [yaxis_rhs dictionary](#yaxis_rhs-dictionary).
| `"background_image":` | dict        | *optional*<br>Singleton that contains the [background_image dictionary](#background_image-dictionary).
| `"display":`          | Boolean     | *optional*<br>`0` to suppress showing figure in GUI, useful when serializing multiple figures during a parameter search loop.<br>`1` (default value) to show figure interactively, and to pause script execution.
| `"latex":`            | string      | *optional*<br>`0` (default) uses matplotlib default fonts, results in fast generation of figures.<br>`1` uses LaTeX fonts, can be slow to generate, but produces production-quality results.
| `"details"`:          | Boolean     | *optional*<br>`0` do **not** show plot details.<br>`1` (default) shows plot details of figure file name, date (`yyyy-mm-dd` format), and time (`hh:mm:ss` format) the figure was generated, and username.
| `"serialize":`        | string      | *optional*<br>`0` (default) does **not** save figure to the file system.<br>`1` saves figure to the file system.  Tested on local drives, but not on network drives.

#### yaxis_rhs Dictionary
|     |     |     |
| --- | --- | --- |
| `"scale":`  | string      | *optional*<br>The factor that multiplies the left-hand y-axis to produce the right-hand y-axis.  For example, if the left-hand y-axis is in `meters`, and the right-hand y-axis is in `centimeters`, the value of `scale` should be set to `100`.  Default value is `1`.
| `"label":`  | string      | *optional*<br>The right-hand-side y-axis label.  Default is an empty string (`None`).
| `"yticks":` | float array | *optional*<br>Same as documentation for `xticks`.

#### background_image Dictionary

|     |     |     |
| --- | --- | --- |
| `"folder":` | string | Value *relative to the current working directory* of the path and folder that contains the background image file.  For the current working directory, use `"."`.
| `"file":`   | string | Value of the background image file name, typically in `png` format.
| `"left":`   | float  | *optional*<br>Left-side extent of image in plot `x` coordinates.   Must be less than the right-side extent.  Default is `0.0`.
| `"right":`  | float  | *optional*<br>Right-side extent of image in plot `x` coordinates.  Must be greater than the left-side extent. Default is `1.0`.
| `"bottom":` | float  | *optional*<br>Bottom-side extent of image in plot `y` coordinates.   Must be less than the top-side extent. Default is `0.0`.
| `"top":`    | float  | *optional*<br>Top-side extent of image in plot `y` coordinates.  Must be greater than the bottom-side extent.  Default is `1.0`.
| `"alpha":`  | float  | *optional*<br>Real number in the range from 0 to 1. Numbers toward 0 are more transparent and numbers toward 1 are more opaque.  Default is `1.0` (fully opaque, no transparency).
