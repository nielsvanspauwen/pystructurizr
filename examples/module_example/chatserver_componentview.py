from .workspace import workspace
from .chatsystem import chat_server

workspace.ComponentView(
    chat_server,
    "Component View",
    "The component view of the MessageRouter."
)
