from pathlib import Path
from typing import Any, Dict

import pandas as pd
import yaml

from finter.data import ContentFactory
from finter.data.data_handler.handler_abstract import AbstractDataHandler
from finter.data.data_handler.registry import DataHandlerRegistry


def load_item_mapping_by_item(item: str) -> Dict[str, str]:
    yaml_path = Path(__file__).parent / "item_mappings.yaml"
    with open(yaml_path, "r") as f:
        mappings = yaml.safe_load(f)

    items = {}
    for key in mappings:
        if item in mappings[key]:
            items[key] = mappings[key][item]
    return items


@DataHandlerRegistry.register_handler("price")
class PriceHandler(AbstractDataHandler):
    def __init__(self):
        self.item_mapping = load_item_mapping_by_item("price")

    def get_data(self, cf: ContentFactory, universe: str, **kwargs) -> Any:
        if universe not in self.item_mapping:
            raise ValueError(f"Unsupported universe: {universe}")
        return cf.get_df(self.item_mapping[universe], **kwargs)  # 수정된 부분


@DataHandlerRegistry.register_handler("volume")
class VolumeHandler(AbstractDataHandler):
    def __init__(self):
        self.item_mapping = load_item_mapping_by_item("volume")

    def get_data(self, cf: ContentFactory, universe: str, **kwargs) -> Any:
        if universe not in self.item_mapping:
            raise ValueError(f"Unsupported universe: {universe}")
        return cf.get_df(self.item_mapping[universe], **kwargs)  # 수정된 부분


@DataHandlerRegistry.register_handler("dividend_factor")
class DividendFactorHandler(AbstractDataHandler):
    def __init__(self):
        self.item_mapping = load_item_mapping_by_item("dividend_factor")

    def get_data(self, cf: ContentFactory, universe: str, **kwargs) -> Any:
        if universe not in self.item_mapping:
            raise ValueError(f"Unsupported universe: {universe}")
        return cf.get_df(self.item_mapping[universe], **kwargs)  # 수정된 부분



@DataHandlerRegistry.register_handler("benchmark")
class BenchmarkHandler(AbstractDataHandler):
    def __init__(self):
        self.item_mapping = load_item_mapping_by_item("benchmark")

    def get_data(self, cf: ContentFactory, universe: str, **kwargs) -> Any:
        if universe not in self.item_mapping:
            raise ValueError(f"Unsupported universe: {universe}")
        if universe == "common":
            return cf.get_df(self.item_mapping["common"], **kwargs)
        else:
            return cf.get_df(self.item_mapping["common"], **kwargs)[
                self.item_mapping[universe]
            ]


@DataHandlerRegistry.register_calculated_method("_52week_high")
def calc_52week_high(universe, **kwargs) -> pd.Series:
    price_data = universe.price(**kwargs)
    return price_data.rolling(window=252).max()


@DataHandlerRegistry.register_calculated_method("_52week_low")
def calc_52week_low(universe, **kwargs) -> pd.Series:
    price_data = universe.price(**kwargs)
    return price_data.rolling(window=252).min()
