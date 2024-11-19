from typing import Dict, Optional, Any

class Agent:
    """
    Represents an agent.
    
    Attributes:
    identifier (str): Unique identifier for the agent.
    public_key (str): Public key associated with the agent.
    metadata (dict): Metadata containing additional agent-specific details, 
                        such as agent type, geolocation, and other properties.
    Metadata example:
        {
            "timestamp": "2024-11-18 15:30:00"
            "agent_type": "Ship",
            "location": "North Sea",
            "geolocation": {
                "latitude": 12.34,
                "longitude": 56.78
            }
        }
    """
    def __init__(self, identifier: Optional[str],
                public_key: Optional[str],
                metadata: Optional[dict] = None):
        self.identifier = identifier
        self.public_key = public_key
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "identifier": self.identifier,
            "public_key": self.public_key,
            "metadata": self.metadata