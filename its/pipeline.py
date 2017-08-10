"""
Script to apply transformations to validated images.
"""
import re
from io import BytesIO
from .transformations import BaseTransform


def process_transforms(img, query, *args):

    """
    View that returns an image transformed according to the
    query options in the request string.
    Return URI to transformed image.
    """
    transform_classes = BaseTransform.__subclasses__()

    if not isinstance(img, BytesIO):
        img_info = img.info
        transform_order = ["fit", "overlay", "resize"]

        # check if a similar transform on the same image is already in cache

        num_subclasses = len(transform_classes)
        # sort the transform classes into the right order
        transform_classes.sort(key= lambda x: transform_order.index(x.slug)
            if x.slug in transform_order
            else num_subclasses)

        # loop through the order dict and apply the transforms
        for tclass in transform_classes:
            if tclass.slug in query:
                query[tclass.slug] = query[tclass.slug].split('x')
                img = tclass.apply_transform(img, query[tclass.slug])

        if img.format is None and 'filename' in img_info.keys():
            # attempt to grab the filetype from the filename
            file_type = re.sub('.+?(\.)', '', img_info['filename'], flags=re.IGNORECASE)
            if file_type.lower() == "jpg" or file_type.lower() == "jpeg":
                img.format = "JPEG"
            else:
                img.format = file_type.upper()

    return img
