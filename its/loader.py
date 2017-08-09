"""
Script to validate images being submitted for transformation.
"""
import operator
from .loaders import BaseLoader
from .errors import ITSLoaderError, ConfigError
from . import settings


def loader(namespace, filename):

    """
    Loads image using the IMAGE_LOADER specified in settings.
    """
    image = None

    loader_classes = BaseLoader.__subclasses__()

    image_loader = [
        loader for loader in loader_classes
        if loader.slug == settings.IMAGE_LOADER]

    if len(image_loader) == 1:
        if filename.endswith(".svg"):
            image = image_loader[0].get_fileobj(namespace, filename)
        else:
            image = image_loader[0].load_image(namespace, filename)
    elif len(image_loader) == 0:
        raise ITSLoaderError("No Image Loader with slug '%s' found." % settings.IMAGE_LOADER)
    elif len(image_loader) > 1:
        raise ConfigError("Two or more Image Loaders have slug '%s'." % settings.IMAGE_LOADER)

    return image
