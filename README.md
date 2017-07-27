# serverless-its
ITS rewrite

ITS (Image Transform Service) performs transformations on images by accepting transform requests in the form of query strings. 


## Crop

There are three varieties of crop -- default, focal and smart crop.

*Default*
The default crop crops the input image about the center of the image. To use this crop, use the crop keyword like so:

http://its_pbs_org/<file_path/filename.ext>?crop=WWxHH

Where:
* crop -- indicates that ITS should perform a crop and use the middle of the image as the focal point for the crop.
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image

Example





*Focal*

Focal crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, utilize the focal keyword:

http://its_pbs_org/<file_path/filename.ext>?focal=WWxHHxXXxYY

Where:
* focal -- indicates that ITS should perform a focal crop
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image
* XX -- the x axis of the focal point, represented as a percentage value of the height of the original picture
* YY -- the y axis of the focal point, represented as a percentage value of the height of the original picture

Example


*Smart*

Smart crop returns an image focused around a user-specified point in the original image of a user-specified size. To use this crop, the crop keyword and include the focal parameters in the filename of the input image: 

http://its_pbs_org/<file_path/filename_focus-XXxYY.ext>?crop=WWxHH

Where:
* crop -- indicates that ITS should perform a crop
* HH -- a numerical pixel value representing the desired height of the output image
* XX -- the x axis of the focal point, represented as a percentage value of the height of the original picture
* YY -- the y axis of the focal point, represented as a percentage value of the height of the original picture
Example

## Overlay

Overlay returns the input image with the specified overlay image placed on top of it. The overlay is placed according to the expected position of its top left corner as input by the user. To use overlay, use the overlay keyword:

http://its_pbs_org/<file_path/filename.ext>?overlay=<overlay_img_path>xPXxPY

Where:
* Overlay -- indicates that ITS should put an overlay on the input image
* Overlay_img_path -- path to the overlay (optionally, can be a keyword a keyword in the OVERLAYS dictionary in settings)
* PX -- the x axis of the top left corner of the overlay image,  represented as a percentage value of the height of the original picture (default is 50%)
* PY -- the y axis of the top left corner of the overlay image, represented as a percentage value of the height of the original picture (default is 50%)

Example



## Resize

Resize returns a resized version of the original image without distortion of the aspect ratio. To use it, use the resize keyword:

http://its_pbs_org/<file_path/filename.ext>?resize=WWxHH

Where:
* Resize -- indicates that ITS should perform a resize transform
* WW -- a numerical pixel value representing the desired width of the output image
* HH -- a numerical pixel value representing the desired height of the output image

Note: Resizing to a larger size isn’t recommended, as it will compromise image quality.

Example


## Format

Format returns the input image in the specified type, rather than being left as the original image’s type. It currently supports conversion to JPG, PNG, and WEBP. To use it, use the format keyword:

http://its_pbs_org/<file_path/filename.ext>?format=<ext>

Where:
* format -- indicates that ITS should perform a format transform
* ext -- the requested output type. Can only be JPG, PNG or WEBP

Example


## Combination
All of the transforms described above can be combined into one query by separating them with ‘&’. For example, the following query crops the input PNG image, applies an overlay to it, and then outputs the result as a JPG:

http://its_pbs_org/demo/demo.png?crop=100x100&overlay=overlay_image.jpg&format=jpg

