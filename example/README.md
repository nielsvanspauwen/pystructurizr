Steps:
- Maak een repo in Product.Hydra, met daarin de PyStructurizr code
- Iedereen maakt zijn models mbv PyStructurizr
- En er is een workspace.py die alles samenbrengt
- Voor elke C4 view die we willen, is er een PyStructurizr file die die view definieert en omzet naar Structurizr DSL. Die DSL wordt met een POST request naar kroki.io gestuurd waarvan we dan gelijk de svg downloaden en uploaden naar S3 storage.
- CI pipeline gaat alle view files executen, zodat bij elke wijziging alle svg's gedownload worden
- In de wiki zetten we images die de SVG url van een diagram gebruiken
- Op die manier is de wiki altijd up to date


Tijdens het schrijven van diagram code is het niet handig (en niet wenselijk) om telkens naar S3 te moeten gaan.
Daarom moet er een live previes / hot reload mode zijn. We draaien een lokale webserver die een statische html pagina served
met daarin lokaal gebufferde SVG file. 
Dat kan met twee packages:
1. https://github.com/Pylons/hupper
dit zorgt dat het view script bij elke save van de python files opnieuw gedraaid wordt en de SVG gedownload wordt (telkens naar dezelfde /tmp/<somefolder>/<viewfile>.svg file schrijven)
2. https://github.com/thanethomson/httpwatcher
served static files en doet een automatische reload als er iets wijzigt. Best in een aparte /tmp/<somefolder> folder runnen


Ik ben een CLI aan het maken, waarmee je live preview als volgt kan krijgen:
$ python3 -m pystructurizr.cli dev --view example.componentview
(eenmaal we setuptools toegevoegd hebben, kan "python3 -m pystructurizr.cli" vervangen worden door "pystructurizr")

Nog te doen: vanuit dat 'dev' command automatisch httpserver starten:
httpwatcher --root /tmp/pystructurizr --watch /tmp/pystructurizr

en zorgen dat als de .py files getouched worden, automatisch de SVG geupdate wordt

Andere commands:
- dump: print generated SVG to console
- build: upload generated SVG to S3

