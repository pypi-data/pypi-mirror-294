import operator
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, List, Optional

from loguru import logger
from pydantic import BaseModel, EmailStr, Field

from plurally.models.node import Node


class PrintNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.inputs["value"] = None

    def forward(self):
        ...
        # """Print the input value."""
        # name, handler = self.inputs["value"]
        # value = flow[name].outputs[handler]
        # if value is not None:
        #     print(f"{self.name}: {value}")


class BinaryOpNode(Node):
    _OP = None

    class InputSchema(Node.InputSchema):
        left: float | int
        right: float | int

    class OutputSchema(BaseModel):
        result: float

    def forward(self, node_input: InputSchema):
        self.outputs["result"] = self._OP(node_input.left, node_input.right)

    def serialize(self):
        return super().serialize()


class MultiplyNode(BinaryOpNode):
    _OP = operator.mul


class AddNode(BinaryOpNode):
    _OP = operator.add


class SendEmailSMTPNode(Node):

    class InitSchema(Node.InitSchema):
        username: str
        password: str = Field(
            None, title="Password", examples=["password123"], format="password"
        )
        smtp_server: str
        from_email: Optional[str] = None
        port: int = 587

    class InputSchema(Node.InputSchema):
        email_address: EmailStr
        subject: str = ""
        content: str = ""

    class OutputSchema(BaseModel): ...

    def __init__(
        self,
        init_inputs: InitSchema,
    ):
        super().__init__(init_inputs)
        self.inputs = {
            "username": init_inputs.username,
            "password": init_inputs.password,
            "smtp_server": init_inputs.smtp_server,
            "from_email": init_inputs.from_email,
            "port": init_inputs.port,
        }  # FIXME: storing password in plaintext
        self.from_email = (
            init_inputs.from_email
            if init_inputs.from_email
            else str(init_inputs.username)
        )
        self._server = None  # lazy init

    def _login_server(self, username: EmailStr, password: str, smtp_server, port):
        logger.debug(f"Logging to {smtp_server}:{port}")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(username, password)
        logger.debug(f"Connected successfully to {smtp_server}:{port}")
        return server

    @property
    def server(self):
        if self._server is None:
            self._server = self._login_server(
                self.inputs["username"],
                self.inputs["password"],
                self.inputs["smtp_server"],
                self.inputs["port"],
            )
        return self._server

    def forward(self, node_input: InputSchema):
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = node_input.email_address
        msg["Subject"] = node_input.subject

        # Attach the plain text body to the email
        msg.attach(MIMEText(node_input.content, "plain"))
        self.server.sendmail(
            self.from_email,
            node_input.email_address,
            msg.as_string(),
        )
        logger.debug("Email sent successfully")

    def serialize(self):
        payload = super().serialize()
        payload["inputs"] = self.inputs
        return payload

    @classmethod
    def _parse(cls, **kwargs):
        inputs = kwargs.pop("inputs")
        kwargs = {**inputs, **kwargs}
        return cls(cls.InitSchema(**kwargs))


# class Instruct(Node):

#     class InputSchema(Node.InputSchema):
#         contexts: List[str]

#     class OutputSchema(BaseModel):
#         result: str

#     def __init__(
#         self,
#         instruct: str,
#     ) -> None:
#         super().__init__()
#         self.client = instructor.from_openai(OpenAI())
#         self.model = "gpt-3.5-turbo"
#         self.instruct = instruct

#     def build_prompt(self, contexts: List[str]):
#         context_str = "\n\n".join(contexts)
#         prompt = f"""
#         You are a helpful assistant, you are given the following instructions: {self.instruct}.
#         Here are the outputs: {context_str}.
#         """
#         return prompt

#     def forward(self, *args: Any, **kwds: Any) -> Any:
#         prompt = self.build_prompt()
#         email: SendEmail.Output = self.client.chat.completions.create(
#             model=self.model,
#             messages=prompt,
#             response_model=SendEmail.Output,
#         )


# class SendEmail(Node):

#     SHORT_DESCRIPTION = "Send an email"

#     def __init__(
#         self,
#         client: instructor.Instructor,
#         model: str,
#         to: str,
#         instruct: str,
#         subject: str = None,
#     ) -> None:
#         super().__init__()
#         self.to = to
#         self.instruct = instruct
#         self.subject = subject
#         self.client = client
#         self.model = model

#     def build_prompt(self) -> List[Dict[str, str]]:
#         subject_prompt = ""
#         if self.subject is None:
#             subject_prompt = " and subject"
#         system_prompt = f"""
#         You are a helpful assistant, that helps to write content {subject_prompt} of an email.
#         """
#         user_prompt = f"""
#         [Instructions]
#         {self.instruct}.
#         [Context]
#         {self.input.state}


#         write the email content {subject_prompt}.
#         """
#         return [{"system": system_prompt}, {"user": user_prompt}]

#     def _send_email(self, email: Output) -> None:
#         print(
#             f"Email sent to {self.to} with subject {email.subject} and content {email.content}"
#         )

#     def forward(self, *args: Any, **kwds: Any) -> Any:
#         prompt = self.build_prompt()
#         email: SendEmail.Output = self.client.chat.completions.create(
#             model=self.model,
#             messages=prompt,
#             response_model=SendEmail.Output,
#         )
#         if self.subject:
#             email.subject = self.subject
#         self.state = email
#         self._send_email(email)


class ClassifyNode(Node):
    SHORT_DESCRIPTION = "Classify input"

    def __init__(self, name: str, categories: List[str]) -> None:
        super().__init__(name)
        self.categories = categories

    def _set_schemas(self):
        class InputSchema(Node.InputSchema):
            contexts: List[str]

        self.InputSchema = InputSchema

        class OutputSchema(BaseModel):
            category: str

        self.OutputSchema = OutputSchema

    def build_prompt(self) -> str:
        context = self.input["context"]

        system_prompt = "You are a helpful assistant that helps to classify input."
        user_prompt = f"""Please classify into one of the following categories:
        [Categories]
        {self.categories}
        [Input]
        {context}.
        """
        return [{"system": system_prompt}, {"user": user_prompt}]

    def forward(self, *args: Any, **kwds: Any) -> Any:
        prompt = self.build_prompt()
        output: ClassifyNode.OutputSchema = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=prompt,
            response_model=ClassifyNode.OutputSchema,
        )
        self.outputs["category"] = output.category
