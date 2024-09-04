from pydantic import BaseModel, Field

from .base_demographics import AgeGender


class MortalityV1Legends:
	DEATHS_BY_AGE = (
		"Death count per year. " "In number of individuals per age or age group."
	)
	TOTAL_DEATHS = "Total number of deaths in a year. " "In number of individuals."
	INFANT_DEATHS = "Number of infant deaths in the population."
	INFANT_DEATH_RATE = "Infant death rate per 1000 live births."


L = MortalityV1Legends


class Mortality(BaseModel):
	deaths_by_age: AgeGender = Field(
		default_factory=AgeGender, description=L.DEATHS_BY_AGE
	)
	total_deaths: float | None = Field(default=None, description=L.TOTAL_DEATHS)
	infant_deaths: float | None = Field(default=None, description=L.INFANT_DEATHS)
	infant_death_rate: float | None = Field(
		default=None, description=L.INFANT_DEATH_RATE
	)


class MortalityV1Keys:
	DEATHS_BY_AGE = "deaths_by_age"
	TOTAL_DEATHS = "total_deaths"
	INFANT_DEATHS = "infant_deaths"
	INFANT_DEATH_RATE = "infant_death_rate"
