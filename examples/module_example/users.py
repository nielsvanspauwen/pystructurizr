from pystructurizr.dsl import Model

users = Model("Users")
customer = users.Person("Customer", "A user of our website.")
support_agent = users.Person("Support Agent", "Handles customer queries.")
analyst = users.Person("Data analyst", "Gathers insight about products and features and reports them to management.")
