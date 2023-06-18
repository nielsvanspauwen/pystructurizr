from example.workspace import workspace
from example.analysissystem import analysis_system
from example.chatsystem import chat_server

workspace.ContainerView(
    analysis_system,
    "Analytics Container View",
    "The container view of the analytics system."
).include(chat_server)
