from pydantic import BaseModel, Field, field_validator

from plurally.models.node import Node


class FormatText(Node):
    DESC = """
    Format text using a template.
    """.strip()

    class InitSchema(Node.InitSchema):
        template: str = Field(
            description="Template to format the text, example: Hello, {}!",
            examples=["Hello, {}!"],
        )

        @field_validator("template")
        @classmethod
        def template_must_have_curly_braces(cls, v: str) -> str:
            if "{}" not in v:
                raise ValueError(
                    "Template must contain a placeholder '{}', example: Hello, {}!"
                )
            return v

    class InputSchema(Node.InputSchema):
        text: str

    class OutputSchema(BaseModel):
        formatted_text: str

    def __init__(self, init_inputs: InitSchema):
        super().__init__(init_inputs)
        self.template = init_inputs.template

    def forward(self, node_input: InputSchema):
        formatted_text = self.template.format(node_input.text)
        self.outputs["formatted_text"] = formatted_text

    def serialize(self):
        return {
            "template": self.template,
            **super().serialize(),
        }


__all__ = [
    "FormatText",
]
