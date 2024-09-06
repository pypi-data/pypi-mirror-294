from typing import Dict, List, Union

from dcim.models import Device, Location
from django_pandas.io import read_frame
from pandas import DataFrame, merge
from sens_platform.api.modules.utils import zero_data_control
from sens_platform.constants import *

from .abc_type_modules import AbstractTypeModules

__all__ = ("GenerateMenus",)


class GenerateMenus(AbstractTypeModules):
    _name: str = GENERATE_MENUS

    def __init__(
        self,
        slug: str,
        dates: Dict,
        location: str = None,
        device: List[str] = None,
        time_window: str = None,
        transducer: List[str] = None,
        dimension: str = None,
    ):
        super().__init__(
            slug=slug,
            dates=dates,
            location=location,
            device=device,
            time_window=time_window,
            transducer=transducer,
            dimension=dimension,
        )

    def execute(self) -> List[Dict]:
        self._generate_settings()
        return self._generate_data()

    def _generate_settings(self) -> None:
        self._setting = {
            "slug": self._slug,
            "postgres": {
                "model": Location,
                "columns_init": [
                    "id",
                    "name",
                    "site__slug",
                ],
            },
        }

    @staticmethod
    def _to_dict(data: DataFrame) -> Union[List[Dict], Dict]:
        result = []
        for _, row in data.iterrows():
            item = {
                "label": f"{row['name']} ({row['count']})",
                "url": "#",
                "subitems": [
                    {"label": "Subitem 1.1", "url": "#"},
                    {"label": "Subitem 1.2", "url": "#"},
                ],
            }
            result.append(item)
        return result

    def _generate_data(self) -> List[Dict]:
        devices = Device.objects.filter(
            site__slug=self._slug,
        )
        _devices: DataFrame = read_frame(
            devices,
            fieldnames=["id", "name", "location__name"],
            verbose=False,
        )
        _device_counts = (
            _devices.groupby("location__name").size().reset_index(name="count")
        )
        _device_counts = _device_counts.rename(columns={"location__name": "name"})
        _device_counts["count"] = _device_counts["count"].astype(str)

        locations = Location.objects.filter(site__slug=self._slug)
        _locations: DataFrame = read_frame(
            locations,
            fieldnames=["id", "name"],
            verbose=False,
        )
        _merged_df = merge(_locations, _device_counts, on="name", how="left").fillna(
            {"count": 0}
        )
        return self._to_dict(_merged_df)
