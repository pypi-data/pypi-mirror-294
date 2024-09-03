try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"


from .utils import build_default_library
from .material import UsualMaterial
from .base_class import Material