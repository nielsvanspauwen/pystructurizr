from pystructurizr.dsl import Model
from .users import customer, support_agent

chat = Model("Chat")

with chat.Group("Built by Team X") as g:
    with g.Group("In Belgium") as g2:
        chat_system = g2.SoftwareSystem("ChatSystem", "Provides a platform for customer support.")
        with chat_system.Group("Chat System Containers") as g3:
            chat_widget = g3.Container("ChatWidget", "Embeddable chat widget for real-time customer support.", technology="JavaScript")
            chat_server = g3.Container("ChatServer", "Handles message routing and storage.", technology="Node.js")
            message_router = chat_server.Component("MessageRouter", "Routes messages between users.", technology="Node.js")
            message_store = chat_server.Component("MessageStore", "Stores chat history.", technology="MongoDB", tags=["database"])

with chat.Group("External Supplier") as g4:
    slack = g4.SoftwareSystem("Slack", "Third party business chat application")

chat_widget.uses(chat_server, "Sends/receives messages", technology="xmpp")
message_router.uses(message_store, "Stores messages")
chat_server.uses(slack, "Integrates with")

customer.uses(chat_widget, "Initiates conversations", "chat widget")
support_agent.uses(slack, "Responds to customer requests", "Slack")
