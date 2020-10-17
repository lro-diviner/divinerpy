import pandas as pd
from yarl import URL

try:
    # <3.9 compatibility
    from importlib_resources import path as resource_path
except ModuleNotFoundError:
    from importlib.resources import path as resource_path


with resource_path("divinerpy.data", "div_mapcycles_RA.txt") as p:
    cycles = pd.read_table(p, header=None, squeeze=True)

DIVINER_URL = URL(
    "https://pds-geosciences.wustl.edu/lro/lro-l-dlre-4-rdr-v1/lrodlr_1001/data"
)


class Mapcycle:
    """
    Convenience class for map cycles
    """

    def __init__(self, cycle):
        """"""
        self.value = str(cycle)

    @property
    def year(self):
        return int(self.value[:4])

    @property
    def timestamp(self):
        return pd.Timestamp(self.value)

    @property
    def date(self):
        return self.timestamp.date()


class _PDSBrowser:
    def __init__(self, year=None, projection="cylindrical", format="jp2"):
        self.year = str(year)
        if year is None:
            print("Without a year, you only can get L2 and L3 base URLs:")
            print(self.level_url)
        print("Change projection to 'polar' and format to 'img' if required.")
        self.projection = projection
        self.format = format

    @property
    def level_url(self):
        return DIVINER_URL / self.level_token

    @property
    def year_url(self):
        return self.level_url / self.year

    @property
    def folder_url(self):
        return self.year_url / self.projection / self.format


class L2Browser(_PDSBrowser):
    @property
    def level_token(self):
        return "gdr_l2"


class L3Browser(_PDSBrowser):
    @property
    def level_token(self):
        return "gdr_l3"


class MappedData:
    def __init__(self, cycle=None):
        pass
