This example models a simplified live chat support system, consisting of a chat widget on a website. Customers can type their message there, which gets routed to the company's Slack. 

The example consists out of the following files:
- `users.py`: models all people that interact with the system
- `chatsystem.py`: models the software system, containers and components for the chatsystem

For a more complex system, you could imagine multiple teams that each model their own software system, but share the Person definitions and potentially shared infrastructure containers.

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
