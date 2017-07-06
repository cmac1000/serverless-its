# import os

# Set DEBUG = True to enable debugging application.
DEBUG = True

IMAGE_LOADER = 'file_system'

OVERLAYS = {
	'passport': "static/Passport_Compass_Rose.png",
}

OVERLAY_PLACEMENT = [50, 50]

# the keyword used to recognize focal point args in filenames
FOCUS_KEYWORD = "focus-" 

SMART_CROP_DELIMITERS = "x_,"