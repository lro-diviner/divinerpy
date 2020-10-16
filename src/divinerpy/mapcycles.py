import pandas as pd

try:
    # <3.9 compatibility
    from importlib_resources import path as resource_path
except ModuleNotFoundError:
    from importlib.resources import path as resource_path


with resource_path("divinerpy.data", "div_mapcycles_RA.txt") as p:
    cycles = pd.read_table(p, header=None, squeeze=True)
