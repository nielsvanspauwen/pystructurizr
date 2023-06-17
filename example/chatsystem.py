from pystructurizr.dsl import Model
from .users import customer, support_agent

chat = Model("Chat")
chat_system = chat.SoftwareSystem("ChatSystem", "Provides a platform for customer support.")
chat_widget = chat_system.Container("ChatWidget", "Embeddable chat widget for real-time customer support.", technology="JavaScript")
chat_server = chat_system.Container("ChatServer", "Handles message routing and storage.", technology="Node.js")
message_router = chat_server.Component("MessageRouter", "Routes messages between users.", technology="Node.js")
message_store = chat_server.Component("MessageStore", "Stores chat history.", technology="MongoDB", tags=["database"])
slack = chat.SoftwareSystem("Slack", "Third party business chat application")

chat_widget.uses(chat_server, "Sends/receives messages", technology="xmpp")
message_router.uses(message_store, "Stores messages")
chat_server.uses(slack, "Integrates with")

customer.uses(chat_widget, "Initiates conversations", "chat widget")
support_agent.uses(slack, "Responds to customer requests", "Slack")
