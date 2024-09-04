from .demographics import DemographicsV1, DemographicsV1Keys
from .economics import EconomicsV1, EconomicsV1Keys
from .health import HealthV1, HealthV1Keys


class DatagardenModels:
	DEMOGRAPHICS = DemographicsV1
	ECOMOMICS = EconomicsV1
	HEALTH = HealthV1


class DatagardenModelKeys:
	DEMOGRAPHICS = DemographicsV1Keys
	ECOMOMICS = EconomicsV1Keys
	HEALTH = HealthV1Keys


__all__ = ["DatagardenModels", "DatagardenModelKeys"]
