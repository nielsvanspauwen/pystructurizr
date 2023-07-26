from pystructurizr.dsl import Workspace
from pystructurizr.dsl import Model

with Model("Users") as users:
    customer = users.Person("Customer", "A user of our website.")
    support_agent = users.Person("Support Agent", "Handles customer queries.")
    analyst = users.Person("Data analyst", "Gathers insight about products and features and reports them to management.")

with Model("Chat") as chat:
    with chat.Group("Our system") as g:
        chat_system = g.SoftwareSystem("ChatSystem", "Provides a platform for customer support.")
        chat_widget = chat_system.Container("ChatWidget", "Embeddable chat widget for real-time customer support.", technology="JavaScript")
        chat_server = chat_system.Container("ChatServer", "Handles message routing and storage.", technology="Node.js")
        message_router = chat_server.Component("MessageRouter", "Routes messages between users.", technology="Node.js")
        message_store = chat_server.Component("MessageStore", "Stores chat history.", technology="MongoDB", tags=["database"])

    with chat.Group("External systems") as g2:
        slack = g2.SoftwareSystem("Slack", "Third party business chat application")

    chat_widget.uses(chat_server, "Sends/receives messages", technology="xmpp")
    message_router.uses(message_store, "Stores messages")
    chat_server.uses(slack, "Integrates with")

    customer.uses(chat_widget, "Initiates conversations", "chat widget")
    support_agent.uses(slack, "Responds to customer requests", "Slack")

with Workspace() as workspace:
    workspace.Model(users)
    workspace.Model(chat)

    workspace.Styles(
        {"tag": "Person", "background": "#08427b", "color": "#ffffff"},
        {"tag": "Software System", "background": "#728da1", "color": "#000000"},
        {"tag": "Container", "background": "#728da1", "color": "#000000"},
        {"tag": "Component", "background": "#728da1", "color": "#000000"},
    )

    workspace.SystemLandscapeView(
        "System View",
        "The system-level view of the chat support system."
    )
