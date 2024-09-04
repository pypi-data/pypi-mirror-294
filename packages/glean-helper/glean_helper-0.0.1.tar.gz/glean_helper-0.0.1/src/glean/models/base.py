from typing import Any, Dict
from pydantic import BaseModel, ConfigDict
import json


class GleanModel(BaseModel):
    """
    Allow dumping a model to the alias names required for CSV upload to Glean.
    """

    model_config = ConfigDict(populate_by_name=True, use_enum_values=True)

    def model_dump(
        self,
        *,
        by_alias: bool = False,
        exclude_non_aliased: bool = False,
        **kwargs: Any
    ) -> Dict[str, Any]:
        dump = super().model_dump(by_alias=by_alias, **kwargs)
        if by_alias:
            return {
                self.model_fields[field_name].alias: value
                for field_name, value in dump.items()
                if self.model_fields[field_name].alias is not None
                or not exclude_non_aliased
            }
        return dump

    def model_dump_dict(
        self,
        *,
        by_alias: bool = False,
        exclude_non_aliased: bool = False,
        **kwargs: Any
    ) -> Dict[str, Any]:
        dump = json.loads(super().model_dump_json(by_alias=by_alias, **kwargs))
        if by_alias:
            return {
                self.model_fields[field_name].alias: value
                for field_name, value in dump.items()
                if self.model_fields[field_name].alias is not None
                or not exclude_non_aliased
            }
        return dump
