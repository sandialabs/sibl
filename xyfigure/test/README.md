# Test Cases

## General

### Image Same or Different

#### Test small files 

* Test two files, without alpha channel <img alt="H_460_460_px_RGB_634800" src="H_460_460_px_RGB_634800.png" width="100"/> and <img alt="H_460_460_px_RGB_634800_clone" src="H_460_460_px_RGB_634800_clone.png" width="100"/>, original and clone, respectively

* Test three files, with alpha channel
<img alt="H_460_460_px_RGBA_846400" src="H_460_460_px_RGBA_846400.png" width="100"/>, <img alt="H_460_460_px_RGBA_846400_clone" src="H_460_460_px_RGBA_846400_clone.png" width="100"/>, and <img alt="H_460_460_px_RGBA_846400_diff" src="H_460_460_px_RGBA_846400_diff.png" width="100"/>, original, clone, and different, respectively.

#### Test Larger Files

* The .png output figure from [t_v_half_u_squared_test.json](t_v_half_u_squared_test.json) was renamed to image_diff_test.png:
![image_diff_test](image_diff_test.png)
* A duplicate image was then created as image_diff_test_clone.png:
![image_diff_test_clone](image_diff_test_clone.png)
* A final modified image image_diff_test_diff.png was created:
![image_diff_test_diff](image_diff_test_diff.png)
The test script [image_diff_test.py](image_diff_test.py) is then used to assess same or different status.

## Signal Processing

### Differentiation

#### Quadratic Function as Source

* source signal with
[t_v_half_u_squared_test.json](t_v_half_u_squared_test.json):
![t_v_half_u_squared_test](t_v_half_u_squared_test.png)
* first derivative with
[t_v_half_u_squared_test_ddt1.json](t_v_half_u_squared_test_ddt1.json):
![t_v_half_u_squared_test_ddt1](t_v_half_u_squared_test_ddt1.png)
* second derivative with
[t_v_half_u_squared_test_ddt2.json](t_v_half_u_squared_test_ddt2.json):
![t_v_half_u_squared_test_ddt2](t_v_half_u_squared_test_ddt2.png)
* third derivative with
[t_v_half_u_squared_test_ddt3.json](t_v_half_u_squared_test_ddt3.json):
![t_v_half_u_squared_test_ddt3](t_v_half_u_squared_test_ddt3.png)

#### Sine Function as Source

* source signal with
[t_v_sines.json](t_v_sines.json):
![t_v_sines](t_v_sines.png)
* first derivative with
[t_v_sines_ddt1.json](t_v_sines_ddt1.json):
![t_v_sines_ddt1](t_v_sines_ddt1.png)

### Butterworth Filter

* [signal_test.py](signal_test.py) unit test of scipy library
* cosines with [t_v_cosines_prefilter.json](t_v_cosines_prefilter.json):
![t_v_cosines_prefilter](t_v_cosines_prefilter.png) and with [t_v_cosines_postfilter.json](t_v_cosines_postfilter.json) 
![t_v_cosines_postfilter](t_v_cosines_postfilter.png)
* sines with [t_v_sines_prefilter.json](t_v_sines_prefilter.json)
![t_v_sines_prefilter](t_v_sines_prefilter.png)
and [t_v_sines_postfilter.json](t_v_sines_postfilter.json)
![t_v_sines_prefilter](t_v_sines_postfilter.png)
