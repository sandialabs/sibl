# xyfigure

## Getting Started

Here we create an example data file from an Excel spreadsheet and walk through the steps to create a simple `xyfigure`.

* Create the example data [file](../io/xyfigure_example/t_versus_f_source.xlsx) in Microsoft Excel.  Here we create a time column `t` (the x-axis), and two functions (two different data series for the y-axis) of time columns `sin(t)` and `cos(2t)`.  

> Generally this file does not come from an Excel file; rather, it come from the output of a simulation.
* Export two `.csv` files as for the [sin](../io/xyfigure_example/t_versus_sin_t.csv) and [cos](../io/xyfigure_example/t_versus_cos_2t.csv) files.
* Create and update the [json](../io/xyfigure_example/figure.json) file, which controls the appearance of the figure.
* From the folder that contains the json file, run the Python script:

```console
$ cd ~/sibl/io/xyfigure_example/
$ python ../../xyfigure/client.py figure.json
```

The output file `figure_example.png` contains this figure:

![figure_example](../io/xyfigure_example/figure_example.png)

will result, written to the `~/sibl/io/xyfigure_example/` folder.

For more information on the variations that are possible for formatting, see the the [XYFigure dictionary](XYFigure_dictionary.md) documentation.

## Getting Minimalistic

Most of the keywords documented in the [XYFigure dictionary](XYFigure_dictionary.md) are *optional*.  If the optional keywords are not specified, XYFigure selects sensible default values.  Users override the default behaviour by specifying the optional keywords.  

Here is the sine and cosine example from above, as a minimual [json](../io/xyfigure_example/min_spec.md) file, without any optional keywords:

```json
{
    "sine-data": {
        "class": "model",
        "folder": ".",
        "file": "t_versus_sin_t.csv"
    },
    "cosine-data": {
        "class": "model",
        "folder": ".",
        "file": "t_versus_cos_2t.csv"
    },
    "figure-output": {
        "class": "view",
        "folder": ".",
        "file": "min_spec.png"
    }
}
```

Here is the output that will be shown to the screen:

![min_spec](../io/xyfigure_example/min_spec.png)


## Getting More Sophisticated

Here we plot the chess board [image](../io/xyfigure_example/chess_800_800_px.png) <img align="left" width="200" height="200" src="../io/xyfigure_example/chess_800_800_px.png"> behind the figure, and override the default tick marks with some specific tick marks.  We also use the alpha channel for a transparent chess board appearance.

The [json](../io/xyfigure_example/figure_with_background.json) file results in this figure:

![figure_example](../io/xyfigure_example/figure_with_background.png)
