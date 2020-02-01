# Image Same or Different

*Used to prevent regressions.*

## Test Small Files 

* Test two files, without alpha channel <img alt="H_460_460_px_RGB_634800" src="H_460_460_px_RGB_634800.png" width="100"/> and <img alt="H_460_460_px_RGB_634800_clone" src="H_460_460_px_RGB_634800_clone.png" width="100"/>, original and clone, respectively

* Test three files, with alpha channel
<img alt="H_460_460_px_RGBA_846400" src="H_460_460_px_RGBA_846400.png" width="100"/>, <img alt="H_460_460_px_RGBA_846400_clone" src="H_460_460_px_RGBA_846400_clone.png" width="100"/>, and <img alt="H_460_460_px_RGBA_846400_diff" src="H_460_460_px_RGBA_846400_diff.png" width="100"/>, original, clone, and different, respectively.

## Test Larger Files

* The .png output figure from [t_v_half_u_squared_test.json](t_v_half_u_squared_test.json) was renamed to image_diff_test.png:
![image_diff_test](image_diff_test.png)
* A duplicate image was then created as image_diff_test_clone.png:
![image_diff_test_clone](image_diff_test_clone.png)
* A final modified image image_diff_test_diff.png was created:
![image_diff_test_diff](image_diff_test_diff.png)
The test script [image_diff_test.py](image_diff_test.py) is then used to assess same or different status.
