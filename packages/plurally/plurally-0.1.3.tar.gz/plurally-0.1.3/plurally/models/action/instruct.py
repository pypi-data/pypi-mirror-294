from typing import Any, Dict, List

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

from plurally.models.node import Node
from plurally.models.utils import BaseEnvVars, create_dynamic_model


class Instruct(Node):
    class InitSchema(Node.InitSchema):
        instruct: str = Field(
            title="Instructions",
            description="Instructions for the AI model.",
            format="textarea",
            examples=["Write a support email."],
        )
        fields: List[str] = Field(
            ["result"],
            title="Outputs",
            description="The fields for structured output of the AI model",
            examples=["subject, content"],
        )

    class OutputSchema(BaseModel):
        key_vals: Dict[str, str]

    class InputSchema(Node.InputSchema):
        contexts: List[str] = None

    class EnvVars(BaseEnvVars):
        OPENAI_API_KEY: str = Field(
            None, title="OpenAI API Key", examples=["sk-1234567890abcdef"]
        )

    def __init__(
        self,
        init_inputs: InitSchema,
    ) -> None:
        super().__init__(init_inputs)
        self._client = None  # lazy init
        self.model = "gpt-3.5-turbo"
        self.instruct = init_inputs.instruct
        self.fields = init_inputs.fields

    def _set_schemas(self, init_inputs: InitSchema) -> None:
        # create pydantic model from fields
        self.OutputSchema = create_dynamic_model("OutputSchema", init_inputs.fields)

    @property
    def client(self):
        if self._client is None:
            self._client = instructor.from_openai(OpenAI())
        return self._client

    def build_messages(self, contexts: List[str] = None) -> str:
        prompt = self.instruct + "\n"
        for ix_ctx, ctx in enumerate((contexts or [])):
            prompt += f'\nContext {ix_ctx + 1}: """\n{ctx}\n"""'
        return [
            {"role": "assistant", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]

    def forward(self, node_input: InputSchema) -> Any:
        messages = self.build_messages(node_input.contexts)
        output: self.OutputSchema = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_model=self.OutputSchema,
        )
        self.outputs = output.model_dump()

    def serialize(self) -> dict:
        return {
            **super().serialize(),
            "instruct": self.instruct,
            "fields": self.fields,
            "output_schema": self.OutputSchema.model_json_schema(),
        }
