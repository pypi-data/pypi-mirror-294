from gai.rag.dtos.create_doc_header_request import CreateDocHeaderRequestPydantic
from typing import Optional

class CreateAgentDocHeaderRequestPydantic(CreateDocHeaderRequestPydantic):
    # Custom getter and setter for AgentId
    @property
    def AgentId(self) -> Optional[str]:
        # Get the value of CollectionName (treated as AgentId)
        return self.CollectionName

    @AgentId.setter
    def AgentId(self, value: Optional[str]) -> None:
        # Set the value of CollectionName (treated as AgentId)
        self.CollectionName = value