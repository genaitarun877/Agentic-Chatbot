
from typing_extensions import TypedDict,Annotated,List
from langgraph.graph.message import add_messages
from typing import Dict, Any, Optional

class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    messages:Annotated[List,add_messages]
    user_controls: Optional[Dict[str, Any]]
