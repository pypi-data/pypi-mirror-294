from pydantic import BaseModel, Field


class DemographicsBaseKeys:
	MALE = "male"
	FEMALE = "female"


class DemographicsBaseLegends:
	AGE_GENDER_MALE = (
		"Number of males. " "In number of individuals per age or age group."
	)
	AGE_GENDER_FEMALE = (
		"Number of females. " "In number of individuals per age or age group."
	)


L = DemographicsBaseLegends


class AgeGender(BaseModel):
	male: dict = Field(default_factory=dict, description=L.AGE_GENDER_MALE)
	female: dict = Field(default_factory=dict, description=L.AGE_GENDER_FEMALE)
