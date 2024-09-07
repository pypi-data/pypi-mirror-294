from json import JSONEncoder, dumps
from time import time_ns
from typing import Any, Dict, List, Literal, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_serializer, field_validator
from typing_extensions import Annotated

from galileo_core.schemas.shared.document import Document
from galileo_core.schemas.shared.message import Message
from galileo_core.schemas.shared.message_role import MessageRole
from galileo_core.schemas.shared.workflows.node_type import NodeType

StepIOType = Union[
    str, Document, Message, Dict[str, str], Union[Sequence[Document], Sequence[Message], Sequence[Dict[str, Any]]]
]
LlmStepAllowedIOType = Union[str, Message, Dict[str, str], Sequence[str], Sequence[Dict[str, str]], Sequence[Message]]
LlmStepIOType = Union[Message, Sequence[Message]]
RetrieverStepAllowedOutputType = Union[Sequence[str], Sequence[Dict[str, str]], Sequence[Document]]


class PydanticJsonEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump(mode="json")
        return super().default(obj)


class BaseStep(BaseModel):
    type: NodeType = Field(
        default=NodeType.workflow, description="Type of the step. By default, it is set to workflow."
    )
    input: StepIOType = Field(description="Input to the step.")
    output: StepIOType = Field(default="", description="Output of the step.")
    name: str = Field(default="", description="Name of the step.", validate_default=True)
    created_at_ns: int = Field(
        default_factory=time_ns, description="Timestamp of the step's creation, as nanoseconds since epoch."
    )
    duration_ns: int = Field(default=0, description="Duration of the step in nanoseconds.")
    metadata: Dict[str, str] = Field(default_factory=dict, description="Metadata associated with this step.")
    status_code: Optional[int] = Field(
        default=None, description="Status code of the step. Used for logging failed/errored steps."
    )
    ground_truth: Optional[str] = Field(default=None, description="Ground truth expected output for the step.")

    model_config = ConfigDict(validate_assignment=True)

    @field_validator("name", mode="before")
    def set_name(cls, value: Optional[str], info: ValidationInfo) -> str:
        return value or info.data["type"]

    @field_validator("created_at_ns", mode="before")
    def set_timestamp(cls, value: Optional[int]) -> int:
        if value is None:
            return time_ns()
        return value

    @field_validator("duration_ns", mode="before")
    def set_duration(cls, value: Optional[int]) -> int:
        if value is None:
            return 0
        return value

    @field_validator("metadata", mode="before")
    def set_metadata(cls, value: Optional[Dict[str, str]]) -> Dict[str, str]:
        if value is None:
            return dict()
        return value

    @field_serializer("input", when_used="json")
    def serialize_input(self, input: StepIOType) -> str:
        return input if isinstance(input, str) else dumps(input, cls=PydanticJsonEncoder)

    @field_serializer("output", when_used="json")
    def serialize_output(self, output: StepIOType) -> str:
        return output if isinstance(output, str) else dumps(output, cls=PydanticJsonEncoder)


class _StepWithChildren(BaseStep):
    steps: List["AWorkflowStep"] = Field(default_factory=list, description="Steps in the workflow.")
    parent: Optional["_StepWithChildren"] = Field(
        default=None, description="Parent node of the current node. For internal use only.", exclude=True
    )


class WorkflowStep(_StepWithChildren):
    type: Literal[NodeType.workflow] = Field(
        default=NodeType.workflow, description="Type of the step. By default, it is set to workflow."
    )


class ChainStep(_StepWithChildren):
    type: Literal[NodeType.chain] = Field(
        default=NodeType.chain, description="Type of the step. By default, it is set to chain."
    )


class LlmStep(BaseStep):
    type: Literal[NodeType.llm] = Field(
        default=NodeType.llm, description="Type of the step. By default, it is set to llm."
    )
    input: LlmStepIOType = Field(
        description="Input to the LLM step. This can be a string, a Message, or a list of `Message`s."
    )
    output: LlmStepIOType = Field(
        default=Message(content=""),
        description="Output of the LLM step. This can be a string, a Message, or a list of `Message`s.",
    )
    model: Optional[str] = Field(default=None, description="Model used for this step.")
    input_tokens: Optional[int] = Field(default=None, description="Number of input tokens.")
    output_tokens: Optional[int] = Field(default=None, description="Number of output tokens.")
    total_tokens: Optional[int] = Field(default=None, description="Total number of tokens.")
    temperature: Optional[float] = Field(default=None, description="Temperature used for generation.")

    @staticmethod
    def parse_io(value: LlmStepAllowedIOType, role: MessageRole = MessageRole.user) -> LlmStepIOType:
        if isinstance(value, (str, dict, Message)):
            if isinstance(value, str):
                parsed_value = Message.model_validate(dict(content=value, role=role))
            elif isinstance(value, dict):
                parsed_value = Message.model_validate({"role": role, **value})
            else:
                parsed_value = value
            return parsed_value
        if isinstance(value, list):
            if all(isinstance(msg, str) for msg in value):
                parsed_values = [Message.model_validate(dict(content=msg, role=role)) for msg in value]
            elif all(isinstance(msg, dict) for msg in value):
                parsed_values = [Message.model_validate({"role": role, **msg}) for msg in value]
            elif all(isinstance(msg, Message) for msg in value):
                parsed_values = [Message.model_validate(msg) for msg in value]
            else:
                raise ValueError("LLM input must be a list of strings, a list of dictionaries, or a list of Messages.")
            return parsed_values
        raise ValueError(
            "LLM input must be one of: A string, a dictionary with keys content and role, a Message, a list of strings, or a list of Messages."
        )

    @field_validator("input", mode="before")
    def set_input(cls, value: LlmStepAllowedIOType) -> LlmStepIOType:
        return cls.parse_io(value, MessageRole.user)

    @field_validator("output", mode="before")
    def set_output(cls, value: LlmStepAllowedIOType) -> LlmStepIOType:
        return cls.parse_io(value, MessageRole.assistant)


class RetrieverStep(BaseStep):
    type: Literal[NodeType.retriever] = Field(
        default=NodeType.retriever, description="Type of the step. By default, it is set to retriever."
    )
    input: str = Field(description="Input query to the retriever.")
    output: List[Document] = Field(
        default_factory=list,
        description="Documents retrieved from the retriever. This can be a list of strings or `Document`s.",
    )

    @field_validator("output", mode="before")
    def set_output(cls, value: Union[List[str], List[Dict[str, str]], List[Document]]) -> List[Document]:
        if isinstance(value, list):
            if all(isinstance(doc, str) for doc in value):
                parsed = [Document.model_validate(dict(content=doc)) for doc in value]
            elif all(isinstance(doc, dict) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            elif all(isinstance(doc, Document) for doc in value):
                parsed = [Document.model_validate(doc) for doc in value]
            else:
                raise ValueError("Retriever output must be a list of strings, a list of dicts, or a list of Documents.")
            return parsed
        raise ValueError("Retriever output must be a list of strings, a list of dicts or a list of Documents.")


class ToolStep(BaseStep):
    type: Literal[NodeType.tool] = Field(
        default=NodeType.tool, description="Type of the step. By default, it is set to tool."
    )


class AgentStep(_StepWithChildren):
    type: Literal[NodeType.agent] = Field(
        default=NodeType.agent, description="Type of the step. By default, it is set to agent."
    )


AWorkflowStep = Annotated[
    Union[WorkflowStep, ChainStep, LlmStep, RetrieverStep, ToolStep, AgentStep], Field(discriminator="type")
]
