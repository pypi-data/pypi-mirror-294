"""""" # start delvewheel patch
def _delvewheel_patch_1_8_1():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'cramjam.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_8_1()
del _delvewheel_patch_1_8_1
# end delvewheel patch

from .cramjam import *

__doc__ = cramjam.__doc__
if hasattr(cramjam, "__all__"):
    __all__ = cramjam.__all__
