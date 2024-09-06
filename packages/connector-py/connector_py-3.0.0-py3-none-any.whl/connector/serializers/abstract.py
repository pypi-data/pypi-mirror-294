import typing as t

from pydantic import BaseModel, Field, Json


class EmptyModel(BaseModel):
    pass


class CommandTypes(BaseModel):
    argument: Json[t.Any] = Field(..., description="OpenAPI Component")
    output: Json[t.Any] = Field(..., description="OpenAPI Component")


class Info(BaseModel):
    app_id: str
    capabilities: list[str]
    authentication_schema: dict[str, t.Any] | None = None
    capability_schema: dict[str, CommandTypes]
