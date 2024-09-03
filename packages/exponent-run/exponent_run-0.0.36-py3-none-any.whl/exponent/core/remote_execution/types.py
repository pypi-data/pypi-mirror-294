import datetime
import json
from datetime import timezone
from enum import Enum
from functools import cached_property
from pathlib import Path, PurePath
from typing import Annotated, Any, ClassVar, Generic, Literal, TypeGuard, TypeVar

from exponent.core.types.generated.command_request_data import (
    CommandRequestDataType,
)
from pydantic import BaseModel, Field


class UseToolsMode(str, Enum):
    read_only = "read_only"
    read_write = "read_write"
    disabled = "disabled"


class UseToolsConfig(BaseModel):
    mode: UseToolsMode = UseToolsMode.read_only

    @property
    def read_only(self) -> bool:
        return self.mode == UseToolsMode.read_only

    @property
    def read_write(self) -> bool:
        return self.mode == UseToolsMode.read_write

    def disable(self) -> None:
        self.mode = UseToolsMode.disabled


class CreateChatResponse(BaseModel):
    chat_uuid: str


class StartChatRequest(BaseModel):
    chat_uuid: str
    prompt: str
    use_tools_config: UseToolsConfig


class StartChatResponse(BaseModel):
    chat_uuid: str


class ExecutionEndResponse(BaseModel):
    execution_ended: bool


class SignalType(str, Enum):
    disconnect = "disconnect"

    def __str__(self) -> str:
        return self.value


class GitInfo(BaseModel):
    branch: str
    remote: str | None


class PythonEnvInfo(BaseModel):
    interpreter_path: str | None
    interpreter_version: str | None
    name: str | None = "exponent"
    provider: Literal["venv", "pyenv", "pipenv", "conda"] | None = "pyenv"


class SystemInfo(BaseModel):
    name: str
    cwd: str
    os: str
    shell: str
    git: GitInfo | None
    python_env: PythonEnvInfo | None


class HeartbeatInfo(BaseModel):
    system_info: SystemInfo | None
    timestamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(timezone.utc)  # noqa: UP017
    )


class RemoteFile(BaseModel):
    file_path: str
    working_directory: str = "."

    @cached_property
    def pure_path(self) -> PurePath:
        return PurePath(self.working_directory, self.file_path)

    @cached_property
    def path(self) -> Path:
        return Path(self.working_directory, self.file_path)

    @cached_property
    def name(self) -> str:
        return self.pure_path.name

    @cached_property
    def absolute_path(self) -> str:
        return self.path.absolute().as_posix()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RemoteFile):
            return False

        return self.path.name == other.path.name

    def __lt__(self, other: "RemoteFile") -> bool:
        # Prefer shorter paths
        if (cmp := self._cmp_path_len(other)) is not None:
            return cmp

        # Prefer paths sorted by parent directory
        if (cmp := self._cmp_path_str(other)) is not None:
            return cmp

        # Prefer paths with alphabetical first character
        return self._cmp_first_char(other)

    def __hash__(self) -> int:
        return hash(self.absolute_path)

    def _cmp_first_char(self, other: "RemoteFile") -> bool:
        return self._cmp_str(self.path.name, other.path.name)

    def _cmp_path_len(self, other: "RemoteFile") -> bool | None:
        self_parts = self.path.absolute().parent.parts
        other_parts = other.path.absolute().parent.parts

        if len(self_parts) == len(other_parts):
            return None

        return len(self_parts) < len(other_parts)

    def _cmp_path_str(self, other: "RemoteFile") -> bool | None:
        self_parts = self.path.absolute().parent.parts
        other_parts = other.path.absolute().parent.parts

        if self_parts == other_parts:
            return None

        for a, b in zip(self_parts, other_parts):
            if a != b:
                return self._cmp_str(a, b)

        return False

    @staticmethod
    def _cmp_str(s1: str, s2: str) -> bool:
        if s1[:1].isalpha() == s2[:1].isalpha():
            return s1 < s2

        return s1[:1].isalpha()


class URLAttachment(BaseModel):
    attachment_type: Literal["url"] = "url"
    url: str
    content: str


class FileAttachment(BaseModel):
    attachment_type: Literal["file"] = "file"
    file: RemoteFile
    content: str


MessageAttachment = Annotated[
    FileAttachment | URLAttachment,
    Field(discriminator="attachment_type"),
]


Direction = Literal[
    "request",
    "response",
]

Namespace = Literal[
    "code_execution",
    "file_write",
    "command",
    "list_files",
    "get_file_attachment",
    "get_file_attachments",
    "get_matching_files",
    "system_context",
    "get_all_tracked_files",
]

SupportedLanguage = Literal[
    "python",
    "shell",
]

WRITE_STRATEGY_FULL_FILE_REWRITE: Literal["FULL_FILE_REWRITE"] = "FULL_FILE_REWRITE"
WRITE_STRATEGY_UDIFF: Literal["UDIFF"] = "UDIFF"
WRITE_STRATEGY_SEARCH_REPLACE: Literal["SEARCH_REPLACE"] = "SEARCH_REPLACE"
WRITE_STRATEGY_NATURAL_EDIT: Literal["NATURAL_EDIT"] = "NATURAL_EDIT"
FileWriteStrategyName = Literal[
    "FULL_FILE_REWRITE", "UDIFF", "SEARCH_REPLACE", "NATURAL_EDIT"
]


class RemoteExecutionMessageData(BaseModel):
    namespace: Namespace
    direction: Direction
    message_data: str

    def message_type(self) -> str:
        return f"{self.namespace}.{self.direction}"


class RemoteExecutionMessage(BaseModel):
    direction: ClassVar[Direction]
    namespace: ClassVar[Namespace]
    correlation_id: str

    @classmethod
    def message_type(cls) -> str:
        return f"{cls.namespace}.{cls.direction}"

    @property
    def result_key(self) -> str:
        return f"{self.namespace}:{self.correlation_id}"


### Response Types


class RemoteExecutionResponseData(RemoteExecutionMessageData):
    pass


class RemoteExecutionResponse(RemoteExecutionMessage):
    direction: ClassVar[Direction] = "response"


ResponseT = TypeVar("ResponseT", bound=RemoteExecutionResponse)


class CodeExecutionResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "code_execution"

    content: str


class FileWriteResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "file_write"

    content: str


class ListFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "list_files"

    files: list[RemoteFile]


class GetFileAttachmentResponse(RemoteExecutionResponse, FileAttachment):
    namespace: ClassVar[Namespace] = "get_file_attachment"

    exists: bool = Field(default=True)


class GetFileAttachmentsResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_file_attachments"

    file_attachments: list[FileAttachment]


class GetMatchingFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_matching_files"

    files: list[RemoteFile]


class GetAllTrackedFilesResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "get_all_tracked_files"

    files: list[RemoteFile]


class SystemContextResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "system_context"

    exponent_txt: str | None
    system_info: SystemInfo | None


### Request Types


class RemoteExecutionRequestData(RemoteExecutionMessageData):
    pass


class RemoteExecutionRequest(RemoteExecutionMessage, Generic[ResponseT]):
    direction: ClassVar[Direction] = "request"

    def validate_response_type(
        self, response: RemoteExecutionMessage
    ) -> TypeGuard[ResponseT]:
        if self.namespace != response.namespace or response.direction != "response":
            raise ValueError(
                f"Expected {self.namespace}.response, but got {response.namespace}.{response.direction}"
            )
        return True


class CodeExecutionRequest(RemoteExecutionRequest[CodeExecutionResponse]):
    namespace: ClassVar[Namespace] = "code_execution"

    language: SupportedLanguage
    content: str


class FileWriteRequest(RemoteExecutionRequest[FileWriteResponse]):
    namespace: ClassVar[Namespace] = "file_write"

    file_path: str
    # Note we don't use SupportedLanguage here because we don't
    # require language-specific execution support for file writes
    language: str
    write_strategy: FileWriteStrategyName
    content: str


class ListFilesRequest(RemoteExecutionRequest[ListFilesResponse]):
    namespace: ClassVar[Namespace] = "list_files"

    directory: str


class GetFileAttachmentRequest(RemoteExecutionRequest[GetFileAttachmentResponse]):
    namespace: ClassVar[Namespace] = "get_file_attachment"

    file: RemoteFile


class GetFileAttachmentsRequest(RemoteExecutionRequest[GetFileAttachmentsResponse]):
    namespace: ClassVar[Namespace] = "get_file_attachments"

    files: list[RemoteFile]


class GetMatchingFilesRequest(RemoteExecutionRequest[GetMatchingFilesResponse]):
    namespace: ClassVar[Namespace] = "get_matching_files"

    search_term: str


class GetAllTrackedFilesRequest(RemoteExecutionRequest[GetAllTrackedFilesResponse]):
    namespace: ClassVar[Namespace] = "get_all_tracked_files"


class SystemContextRequest(RemoteExecutionRequest[SystemContextResponse]):
    namespace: ClassVar[Namespace] = "system_context"


### Commands


### Command Response Types


class CommandResponse(RemoteExecutionResponse):
    namespace: ClassVar[Namespace] = "command"

    content: str


### Command Request Types


class CommandRequest(RemoteExecutionRequest[CommandResponse]):
    namespace: ClassVar[Namespace] = "command"

    data: CommandRequestDataType = Field(..., discriminator="type")


RemoteExecutionRequestType = (
    CodeExecutionRequest
    | FileWriteRequest
    | ListFilesRequest
    | GetFileAttachmentRequest
    | GetFileAttachmentsRequest
    | GetMatchingFilesRequest
    | GetAllTrackedFilesRequest
    | SystemContextRequest
    | CommandRequest
)

RemoteExecutionResponseType = (
    CodeExecutionResponse
    | FileWriteResponse
    | ListFilesResponse
    | GetFileAttachmentResponse
    | GetFileAttachmentsResponse
    | GetMatchingFilesResponse
    | GetAllTrackedFilesResponse
    | SystemContextResponse
    | CommandResponse
)


class ChatMode(str, Enum):
    DEFAULT = "default"
    CLOUD = "cloud"


class CLIConnectedState(BaseModel):
    chat_uuid: str
    connected: bool
    last_connected_at: datetime.datetime | None
    system_info: SystemInfo | None


class DevboxConnectedState(str, Enum):
    # TODO: Only needed if we create devbox async
    INITIALIZED = "INITIALIZED"
    # The chat has been initialized, but the devbox is still loading
    DEVBOX_LOADING = "DEVBOX_LOADING"
    # CLI is connected and running on devbox
    CONNECTED = "CONNECTED"
    # CLI has disconnected
    # TODO: what condition?
    CLI_DISCONNECTED = "CLI_DISCONNECTED"
    # CLI has an error, devbox is running
    CLI_ERROR = "CLI_ERROR"
    # Devbox has an error
    DEVBOX_ERROR = "DEVBOX_ERROR"
    # Devbox_shutdown
    # TODO: In theory our terminal state, do we want to name something different?
    DEVBOX_SHUTDOWN = "DEVBOX_SHUTDOWN"


class CloudConnectedState(BaseModel):
    chat_uuid: str
    connected_state: DevboxConnectedState
    last_connected_at: datetime.datetime | None
    system_info: SystemInfo | None


class CLIErrorLog(BaseModel):
    event_data: str
    timestamp: datetime.datetime = datetime.datetime.now()
    attachment_data: str | None = None

    @property
    def loaded_event_data(self) -> Any | None:
        try:
            return json.loads(self.event_data)
        except json.JSONDecodeError:
            return None

    @property
    def attachment_bytes(self) -> bytes | None:
        if not self.attachment_data:
            return None
        return self.attachment_data.encode()
