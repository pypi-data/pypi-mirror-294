from typing import Union
from shyft.time_series import lib_path
from shyft.energy_market.core import ModelInfo, run_state
from shyft.energy_market._energy_market import * # need to pull in dependent base-types
from shyft.energy_market.stm.shop import shyft_with_shop
if shyft_with_shop:
    from shyft.energy_market.stm.shop import ShopCommand, ShopCommandList
from ._stm import *

__doc__ = _stm.__doc__
__version__ = _stm.__version__

# backward compatible names after renaming
if shyft_with_stm:
    from . import compute

    Aggregate = Unit
    AggregateList = UnitList
    WaterRoute = Waterway
    PowerStation = PowerPlant
    HydroPowerSystem.create_aggregate = HydroPowerSystem.create_unit
    HydroPowerSystem.create_power_station = HydroPowerSystem.create_power_plant
    HydroPowerSystem.create_water_route = HydroPowerSystem.create_waterway
# end backward compat section

__all__ = [
    "shyft_with_stm",
    "HydroPowerSystem", "HydroPowerSystemList",
    "StmSystem", "StmSystemList", "StmPatchOperation",
    "MarketArea",
    "ModelState",
    "Unit", "UnitList",
    "Reservoir",
    "PowerPlant",
    "Gate",
    "Waterway",
    "UnitGroupType",
    "UnitGroup",
    "t_xy", "t_turbine_description", "MessageList", "t_xyz_list", "t_xyz",
    "_t_xy_", "_turbine_description", "_ts", "_time_axis", "_t_xy_z_list", "_string", "_double",
    "_i64", "_bool", "_u16",
    "DStmClient", "DStmServer",
    "HpsClient", "HpsServer",
    "StmClient", "StmServer",
    "StmTaskServer", "StmTaskClient",
    "StmCase", "ModelRefList", "StmModelRef", "StmTask",
    "Contract", "ContractList",
    "ContractPortfolio", "ContractPortfolioList",
    "PowerModule", "Busbar", "Network", "TransmissionLine",
    "WindFarm","WindTurbine",
    "compute_effective_price",
    "UrlResolveError"
]
