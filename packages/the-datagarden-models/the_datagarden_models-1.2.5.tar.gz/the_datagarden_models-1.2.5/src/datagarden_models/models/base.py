from typing import Union, get_args, get_origin

from pydantic import BaseModel, Field, model_validator


class DataGardenModelLegends:
	DATAGARDEN_MODEL_VERSION = "Version of the data model."


class DataGardenModel(BaseModel):
	datagarden_model_version: str = Field("v1.0", frozen=True)

	@model_validator(mode="before")
	def check_datagarden_model_version(cls, values):
		if (
			"datagarden_model_version" in values
			and values["datagarden_model_version"]
			!= cls.model_fields["datagarden_model_version"].default
		):
			raise ValueError("The field 'datagarden_model_version' is immutable.")
		return values

	@classmethod
	def units(cls, attribute: str | None = None, indent: int = 0):
		def print_description(prefix, field_info, indent_level):
			indent_space = "    " * indent_level
			description = field_info.description
			if description:
				print(f"{indent_space}{prefix}: {description}")

		def is_base_model(annotation):
			if isinstance(annotation, type) and issubclass(annotation, BaseModel):
				return True
			if get_origin(annotation) is Union:
				return any(is_base_model(arg) for arg in get_args(annotation))
			return False

		def recursive_units(sub_cls: type[BaseModel], attr_prefix="", indent_level=0):
			for field_name, field_info in sub_cls.model_fields.items():
				full_attr_name = (
					f"{attr_prefix}.{field_name}" if attr_prefix else field_name
				)
				if is_base_model(field_info.annotation):
					print_description(full_attr_name, field_info, indent_level)
					if field_info.annotation:
						recursive_units(
							field_info.annotation, full_attr_name, indent_level + 1
						)
					else:
						print_description(full_attr_name, field_info, indent_level)

		if attribute:
			parts = attribute.split(".")
			current_model = cls
			for part in parts:
				field_info = current_model.model_fields.get(part)
				if not field_info:
					print(f"No description available for attribute: {attribute}")
					return
				if issubclass(field_info.__class__, BaseModel):
					current_model = field_info.__class__
				else:
					print_description(attribute, field_info, indent)
					return
			recursive_units(current_model, attribute, indent + 1)
		else:
			recursive_units(cls)
