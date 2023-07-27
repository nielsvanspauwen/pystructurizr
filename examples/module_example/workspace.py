from pystructurizr.dsl import Workspace

from .users import users
from .chatsystem import chat
from .analysissystem import analytics

workspace = Workspace()
workspace.Model(users)
workspace.Model(chat)
workspace.Model(analytics)

analytics.uses(chat, "Derives insights from")

workspace.Styles(
    {"tag": "Person", "background": "#08427b", "color": "#ffffff"},
    {"tag": "Software System", "background": "#728da1", "color": "#000000"},
    {"tag": "Container", "background": "#728da1", "color": "#000000"},
    {"tag": "Component", "background": "#728da1", "color": "#000000"},
)
