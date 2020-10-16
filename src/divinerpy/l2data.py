import warnings
from pathlib import Path

import pvl
from yarl import URL

from planetarypy.utils import url_retrieve

DIVINER_URL = URL(
    "https://pds-geosciences.wustl.edu/lro/lro-l-dlre-4-rdr-v1/lrodlr_1001/data"
)

root = Path("/luna4/maye/l2_data")


class DataManager:
    @property
    def labels(self):
        return sorted(list(root.glob("*.lbl")))

    @property
    def images(self):
        return sorted(list(root.glob("*.jp2")))


class L2Data:
    GDR_L2_URL = DIVINER_URL / "gdr_l2"

    def __init__(
        self,
        cycle=None,
        datatype="ltim",
        tbol_res=1,
        projection="cylindrical",
        format="jp2",
        year=None,
    ):
        self.cycle = cycle
        self.datatype = datatype
        self.tbol_res = tbol_res
        self.projection = projection
        self.format = format
        self.year = year

        if cycle is None and year is None:
            warnings.warn("Set `year` for getting a correct folder URL.")

    @property
    def cycle(self):
        return self._cycle

    @cycle.setter
    def cycle(self, value):
        self._cycle = value

    @property
    def year(self):
        if self.cycle is not None:
            return str(self.cycle)[:4]
        else:
            return self._year

    @year.setter
    def year(self, value):
        self._year = str(value)

    @property
    def tbol_res(self):
        return self._tbol_res

    @tbol_res.setter
    def tbol_res(self, value):
        self._tbol_res = str(value).zfill(3)

    @property
    def datatype(self):
        return self._datatype

    @datatype.setter
    def datatype(self, value):
        """Set datatype string.

        This is for a Diviner GDR L3 datatype.

        Parameters
        ----------
        value : {"jd", "ltim", "tb3", "tbol"}
            RA = Rock abundance
            RMS = RMS error for RA
            ST = Regolith temperature
            TBOL = Average Bolometric Temperature
        """
        allowed = "jd ltim".split()
        allowed += [f"tb{i}" for i in range(3, 10)]
        allowed += [f"vb{i}" for i in range(1, 3)]
        if not value.lower() in allowed:
            raise ValueError(f"Only {allowed} allowed.")
        else:
            self._datatype = value.lower()

    @property
    def second_token(self):
        # TODO: deal with "err, cnt"
        return "avg"

    @property
    def fname(self):
        "Construct L3 GDR data filename."

        res = 128
        if self.datatype == "tbol":
            res = self.tbol_res
        return f"dgdr_{self.datatype}_{self.second_token}_cyl_{self.cycle}n_{res}_{self.format}.{self.format}"

    @property
    def label(self):
        return str(Path(self.fname).with_suffix(".lbl"))

    @property
    def folder_url(self):
        return self.GDR_L2_URL / self.year / self.projection / self.format

    @property
    def data_url(self):
        return self.folder_url / self.fname

    @property
    def label_url(self):
        return self.folder_url / self.label

    def download_label(self, subfolder=""):
        if not subfolder:
            p = root
        else:
            p = Path(subfolder)
        p.mkdir(exist_ok=True)
        url_retrieve(self.label_url, Path(subfolder) / self.label)

    def download_data(self, subfolder="", overwrite=False):
        if not subfolder:
            p = root
        else:
            p = Path(subfolder)
        p.mkdir(exist_ok=True)
        savepath = p / self.fname
        if savepath.exists() and not overwrite:
            print("File exists, use `overwrite=True` to force download.")
            return
        else:
            url_retrieve(self.data_url, Path(subfolder) / self.fname)
