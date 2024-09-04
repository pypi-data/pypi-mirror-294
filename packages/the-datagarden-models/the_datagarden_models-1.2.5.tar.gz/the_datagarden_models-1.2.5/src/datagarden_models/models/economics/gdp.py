from pydantic import BaseModel, Field

from .base_economics import EconomicsUnit, EconomicsValue


class ValueAddedKeys:
	UNITS = "units"
	TOTAL = "total"
	BY_NACE_ACTIVIT = "by_nace_activity"


class ValueAddedLegends:
	TOTAL = "Total value added in given units."
	UNITS = "Currency and units."
	BY_NACE_ACTIVITY = (
		"By NACE economic activity. See also "
		"https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Glossary:Statistical_classification_of_economic_activities_in_the_European_Community_(NACE)"
	)


LV = ValueAddedLegends


class ValueAdded(BaseModel):
	units: EconomicsUnit = Field(default_factory=EconomicsUnit, description=LV.UNITS)
	total: float | None = Field(default=None, description=LV.TOTAL)
	by_nace_activity: dict = Field(
		default_factory=dict, description=LV.BY_NACE_ACTIVITY
	)


class GDPV1Legends:
	TOTAL_GDP = "Total GDP value for the region."
	GDP_PER_INHABITANT = "GDP per inhabitant."
	VALUE_ADDED = "Economic value added data per region."


L = GDPV1Legends


class GDP(BaseModel):
	total_gpd: EconomicsValue = Field(
		default_factory=EconomicsValue, description=L.TOTAL_GDP
	)
	gpd_per_inhabitant: EconomicsValue = Field(
		default_factory=EconomicsValue, description=L.TOTAL_GDP
	)
	value_added: ValueAdded = Field(default_factory=ValueAdded, description=L.TOTAL_GDP)


class GDPV1Keys(ValueAddedKeys):
	TOTAL_GDP = "total_gpd"
	GDP_PER_INHABITANT = "gpd_per_inhabitant"
	VALUE_ADDED = "value_added"
