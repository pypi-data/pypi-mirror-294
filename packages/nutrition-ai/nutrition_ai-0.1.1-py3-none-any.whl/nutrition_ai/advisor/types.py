from pydantic import BaseModel, Field
from typing import Optional, List, Any
import json


class AdvisorResponseUsage(BaseModel):
    model: str


class AdvisorDataRequest(BaseModel):
    name: str
    respondParameters: str
    runId: str
    toolCallId: str


class AdvisorActionResponse(BaseModel):
    data: str
    messageId: str
    name: str


class AdvisorResponse(BaseModel):
    threadId: str
    messageId: str
    content: Optional[str] = Field(
        default=None,
        description="JSON-encoded string of response content. Will be empty if dataRequest or actionResponse is not null.",
    )
    contentToolHints: Optional[List[str]] = Field(
        default_factory=list,
        description="An array of tool names that the advisor has sensed could be useful to run on this response.",
    )
    dataRequest: Optional[AdvisorDataRequest] = None
    actionResponse: Optional[AdvisorActionResponse] = None
    usage: Optional[AdvisorResponseUsage] = None

    @property
    def decoded_content(self) -> Any:
        """Returns the decoded content if it exists, otherwise None."""
        return json.loads(self.content) if self.content else None


class ToolInfo(BaseModel):
    name: str
    displayName: str
    type: str
    description: str


class ToolInfoList(BaseModel):
    tools: List[ToolInfo]

