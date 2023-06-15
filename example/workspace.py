from pystructurizr.dsl import Workspace

from example.users import users, customer, support_agent
from example.chatsystem import chat, chat_widget, slack

workspace = Workspace()
workspace.Model(users)
workspace.Model(chat)

customer.uses(chat_widget, "Initiates conversations", "chat widget")
support_agent.uses(slack, "Responds to customer requests", "Slack")

workspace.Styles(
    {"tag": "Person", "background": "#08427b", "color": "#ffffff"},
    {"tag": "Software System", "background": "#728da1", "color": "#000000"},
    {"tag": "Container", "background": "#728da1", "color": "#000000"},
    {"tag": "Component", "background": "#728da1", "color": "#000000"},
)
