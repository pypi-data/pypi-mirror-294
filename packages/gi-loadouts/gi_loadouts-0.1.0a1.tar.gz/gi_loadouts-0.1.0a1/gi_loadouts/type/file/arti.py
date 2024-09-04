from enum import Enum

from pydantic import BaseModel

from gi_loadouts.data.arti import ArtiList
from gi_loadouts.type.arti import ArtiLevl
from gi_loadouts.type.rare import Rare
from gi_loadouts.type.stat import ATTR, __revmap__


class ArtiArea(str, Enum):
    """
    Set of possible artifact areas
    """
    fwol = "FWOL"
    pmod = "PMOD"
    sdoe = "SDOE"
    gboe = "GBOE"
    ccol = "CCOL"


class ArtiFile(BaseModel):
    """
    Artifact storage primitive
    """
    name: str = ""
    type: ArtiList = getattr(ArtiList, "None")
    area: Enum = ArtiArea.fwol
    rare: Rare = Rare.Star_1
    levl: ArtiLevl = ArtiLevl.Level_00
    stat_main: ATTR = ATTR()
    stat_a: ATTR = ATTR()
    stat_b: ATTR = ATTR()
    stat_c: ATTR = ATTR()
    stat_d: ATTR = ATTR()

    @property
    def easydict(self) -> dict:
        """
        Derive the information stored for consumption in file storage

        :return: Dictionary consisting of associated artifact statistics
        """
        data = {
            "name": self.name,
            "type": self.type.value.name,
            "area": self.area.value,
            "rare": self.rare.value.qant,
            "levl": self.levl.value.name,
            "stat": {
                "main": {
                    "name": self.stat_main.stat_name.value,
                    "data": self.stat_main.stat_data,
                },
                "a": {
                    "name": self.stat_a.stat_name.value,
                    "data": self.stat_a.stat_data,
                },
                "b": {
                    "name": self.stat_b.stat_name.value,
                    "data": self.stat_b.stat_data,
                },
                "c": {
                    "name": self.stat_c.stat_name.value,
                    "data": self.stat_c.stat_data,
                },
                "d": {
                    "name": self.stat_d.stat_name.value,
                    "data": self.stat_d.stat_data,
                },
            }
        }
        return data


def make_artifile(objc: dict) -> ArtiFile:
    """
    Parse the provided dictionary of artifact statistics to make a supported artifact object

    :param objc: Dictionary consisting of associated artifact statistics
    :return: Supported artifact object for processing
    """
    try:
        artiobjc = ArtiFile(
            name=objc["name"],
            type=getattr(ArtiList, objc["type"].replace(" ", "_").replace("'", "").replace("-", "_")),
            area=getattr(ArtiArea, objc["area"].lower()),
            rare=getattr(Rare, f"Star_{objc["rare"]}"),
            levl=getattr(ArtiLevl, objc["levl"].replace(" ", "_")),
            stat_main=ATTR(stat_name=__revmap__[objc["stat"]["main"]["name"]], stat_data=objc["stat"]["main"]["data"]),
            stat_a=ATTR(stat_name=__revmap__[objc["stat"]["a"]["name"]], stat_data=objc["stat"]["a"]["data"]),
            stat_b=ATTR(stat_name=__revmap__[objc["stat"]["b"]["name"]], stat_data=objc["stat"]["b"]["data"]),
            stat_c=ATTR(stat_name=__revmap__[objc["stat"]["c"]["name"]], stat_data=objc["stat"]["c"]["data"]),
            stat_d=ATTR(stat_name=__revmap__[objc["stat"]["d"]["name"]], stat_data=objc["stat"]["d"]["data"]),
        )
    except Exception as expt:
        raise ValueError("Artifact unit data cannot be parsed.") from expt
    return artiobjc
