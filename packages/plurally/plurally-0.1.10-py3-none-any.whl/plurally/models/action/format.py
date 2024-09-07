import re

from pydantic import BaseModel, Field, field_validator

from plurally.models.node import Node
from plurally.models.utils import create_dynamic_model


class FormatText(Node):
    DESC = """
    Format text using a template.
    """.strip()

    class InitSchema(Node.InitSchema):
        template: str = Field(
            description="Template to format the text, example: Hello, {name}! I like {food}.",
            examples=["Hello, {name}, I like {food}."],
        )

        @field_validator("template")
        def check_template(cls, value):
            if not re.findall(r"{([^{}]+)}", value):
                raise ValueError("Template should contain at least one NAMED variable")
            return value

    class InputSchema(Node.InputSchema):
        text: str

    class OutputSchema(BaseModel):
        formatted_text: str

    def __init__(self, init_inputs: InitSchema):
        self.template = init_inputs.template
        super().__init__(init_inputs)

    def _set_schemas(self) -> None:
        # create pydantic model from output_fields
        self.InputSchema = create_dynamic_model(
            "InputSchema", self.vars, base=Node.InputSchema
        )

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, value):
        self._template = value
        self.vars = re.findall(r"{(.*?)}", value)

    def forward(self, node_input):
        formatted_text = self.template.format(**node_input.model_dump())
        self.outputs["formatted_text"] = formatted_text

    def serialize(self):
        return {
            "template": self.template,
            "input_schema": self.InputSchema.model_json_schema(),
            **super().serialize(),
        }


__all__ = [
    "FormatText",
]
