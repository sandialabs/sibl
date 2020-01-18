# XYFigure defaults

## Keys, Values, Descriptions

### XYFigure Dictionary

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
`"inverted":` | Boolean | *optional*<br>Convenience key to invert the `y` value data by multiplying all data by `-1`.  Default value is `0`.
`"xoffset":` | real | *optional*<br>Shifts all values of the `x` data to the left or the right by the `xoffset` value.  Default value is `0.0`.

### View Dictionary

The view dictionary contains items that describe how the main figure is constructed.

