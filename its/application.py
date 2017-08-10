#!/usr/bin/env python3

from io import BytesIO
from flask import Flask, request, abort, Response
from its.pipeline import process_transforms
from its.loader import loader
from its.optimize import optimize
from its.settings import MIME_TYPES, DEBUG
from its.errors import NotFoundError

app = Flask(__name__)


def process_request(namespace, query, filename):
    
    disable_optimize = True
    
    try:
        image = loader(namespace, filename)
    except NotFoundError as e:
        abort(404)
    
    """
    PIL doesn't support SVG and ITS doesn't change them in any way,
    so loader returns a ByesIO object so the images will still be returned to the browser.
    This BytesIO object is returned from each loader class's get_fileobj() function.
    """
    if isinstance(image, BytesIO):
        output = image
        mime_type = MIME_TYPES["SVG"]
    else:
        image.info['filename'] = filename

        if len(query) > 0:
            result = process_transforms(image, query)

        # image conversion and compression
        # cache result
        if not disable_optimize:
            result = optimize(result, query)

        if result.format is None:
            result.format = image.format

        mime_type = MIME_TYPES[result.format.upper()]

        output = BytesIO()
        result.save(output, format=result.format.upper())

    return Response(response=output.getvalue(), mimetype=mime_type)

def process_old_request(namespace, filename, transform, width=None, height=None, ext=None, x=None, y=None):

    query = {}

    if transform in ["focalcrop", "crop", "fit"]:
        transform = "fit"

    query[transform] = "x"
    if width is not None:
        query[transform] = str(width) + query[transform]
    
    if height is not None:
        query[transform] = query[transform] + str(height)

    if ext is not None:
        query['format'] = ext

    if x is not None:
        query[transform] = query[transform] + "x" + str(x)

    if y is not None:
        query[transform] = query[transform] + "x" + str(y)

    return query

# New ITS
# image transform command
@app.route('/<namespace>/<path:filename>', methods=['GET'])
def transform_image(namespace, filename):
    query = request.args.to_dict()
    result = process_request(namespace, query, filename)
    return result


# Old ITS Support
@app.route('/<namespace>/<path:filename>.crop.<width>x<height>.<ext>')
def crop(namespace, filename, width, height, ext):
    query = process_old_request(namespace, filename, "fit", width, height, ext)
    result = process_request(namespace, query, filename)
    return result


@app.route(
    '/<namespace>/<path:filename>.focalcrop.<width>x<height>.' +
    '<int(min=0,max=100):x>.<int(min=0,max=100):y>.<ext>')
def focalcrop(namespace, filename, width, height, x, y, ext):
    query = process_old_request(namespace, filename, "fit", width, height, ext, x, y)
    result = process_request(namespace, query, filename)
    return result


@app.route('/<namespace>/<path:filename>.fit.<width>x<height>.<ext>')
def fit(namespace, filename, width, height, ext):
    query = process_old_request(namespace, filename, "fit", width, height, ext)
    result = process_request(namespace, query, filename)
    return result


# resize with pseduo-optional arguments
@app.route('/<namespace>/<path:filename>.resize.<width>x<height>.<ext>')
@app.route('/<namespace>/<path:filename>.resize.x<height>.<ext>')
@app.route('/<namespace>/<path:filename>.resize.<width>x.<ext>')
def resize(namespace, filename, ext, width=None, height=None):
    query = process_old_request(namespace, filename, "resize", width, height, ext)
    result = process_request(namespace, query, filename)
    return result


# passport overlay resize with pseduo-optional arguments
@app.route('/<namespace>/<path:filename>.resize.<int:width>x<int:height>.passport.<ext>')
@app.route('/<namespace>/<path:filename>.resize.x<int:height>.passport.<ext>')
@app.route('/<namespace>/<path:filename>.resize.<int:width>x.passport.<ext>')
def resize_passport(namespace, filename, width, height, ext):
    query = process_old_request(namespace, filename, "resize", width, height, ext)
    query['overlay'] = 'passport'
    result = process_request(namespace, query, filename)
    return result


if __name__ == '__main__':
    app.run(debug=DEBUG)
