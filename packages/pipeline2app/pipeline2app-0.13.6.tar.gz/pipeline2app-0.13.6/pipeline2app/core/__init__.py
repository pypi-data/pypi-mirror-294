from ._version import __version__

PACKAGE_NAME = "pipeline2app"
CODE_URL = f"https://github.com/ArcanaFramework/{PACKAGE_NAME}"


__authors__ = [("Thomas G. Close", "tom.g.close@gmail.com")]

from .image import Pipeline2appImage, App, Metapackage  # noqa
