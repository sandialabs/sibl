# Image Same or Different

*Used to prevent image regressions.*

* The test script [test_image_diff.py](test_image_diff.py) is used to assess same or different status.

## Test Small Files 

* (Not part of the automated unit test, manual test only) two files, without alpha channel <img alt="H_460_460_px_RGB_634800" src="H_460_460_px_RGB_634800.png" width="100"/> and <img alt="H_460_460_px_RGB_634800_clone" src="H_460_460_px_RGB_634800_clone.png" width="100"/>, original and clone, respectively

* Automated unit test three files, with alpha channel
<img alt="H_460_460_px_RGBA_846400" src="H_460_460_px_RGBA_846400.png" width="100"/>, <img alt="H_460_460_px_RGBA_846400_clone" src="H_460_460_px_RGBA_846400_clone.png" width="100"/>, and <img alt="H_460_460_px_RGBA_846400_diff" src="H_460_460_px_RGBA_846400_diff.png" width="100"/>, original, clone, and different, respectively.

## Test Larger Files

* (Not part of the automated unit test because the test on large images is slow.)  Manual test the .png output figure from [u-squared.json](../differentiation/u-squared.json) was renamed to image_diff_test.png:
![image_diff_test](image_diff_test.png)
* A duplicate image was then created as image_diff_test_clone.png:
![image_diff_test_clone](image_diff_test_clone.png)
* A final modified image image_diff_test_diff.png was created:
![image_diff_test_diff](image_diff_test_diff.png)
