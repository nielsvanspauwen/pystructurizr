This example models a simplified live chat support system, consisting of a chat widget on the ACME website. Customers can type their message there, which gets routed to the ACME's Slack. In the background, a sentiment analysis and analysis engines analyzes the customer messages and provides insights and statistics for the different products and features that ACME offers.

The example consists out of the following files:
- `users.py`: models all people that interact with the system
- `chatsystem.py`: models the software system, containers and components for the chatsystem
- `analysissystem.py`: models the software system, containers and components for the sentiment analysis and statistics system

For the purpose of this example, assume Team A works on the core chat product, and Team B works on the analytics engine. Each team models their own system, but they share the Person definitions and potentially shared infrastructure containers.

The `workspace.py` file brings the different models and software systems together, and adds toplevel relationships between them.

Finally, multipe view files (`componentview.py`, `containerview.py`, `systemlandscapeview.py`) describe which views to generate an SVG for.

To run the example, you would for instance do:
```
$ pystructurizr dev --view example.componentview
```
or 
```
$ pystructurizr build --view example.containerview --gcs-credentials <...> --bucket-name <...> --object-name <...>
```
