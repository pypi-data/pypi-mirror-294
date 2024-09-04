from pydantic import BaseModel

from gi_loadouts.type.levl import Level
from gi_loadouts.type.weap import WeaponType


class WeapFile(BaseModel):
    """
    Weapon storage primitive
    """
    name: str = ""
    type: WeaponType = WeaponType.none
    levl: Level = Level.Level_01_20_Rank_0
    refn: str = "Refinement 1"

    @property
    def easydict(self) -> dict:
        """
        Derive the information stored for consumption in file storage

        :return: Dictionary consisting of associated artifact collection statistics
        """
        data = {
            "name": self.name,
            "type": self.type.name,
            "levl": self.levl.value.name,
            "refn": self.refn,
        }
        return data


def make_weapfile(objc: dict) -> WeapFile:
    """
    Parse the provided dictionary of artifact statistics to make a supported weapon object

    :param objc: Dictionary consisting of associated weapon statistics
    :return: Supported weapon object for processing
    """
    try:
        weapobjc = WeapFile(
            name=objc["name"],
            type=getattr(WeaponType, objc["type"]),
            levl=getattr(Level, objc["levl"].replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")),
            refn=objc["refn"],
        )
    except Exception as expt:
        raise ValueError("Weapon data cannot be parsed.") from expt
    return weapobjc
