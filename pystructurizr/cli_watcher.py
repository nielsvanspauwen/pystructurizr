import datetime
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def formatted_timestamp():
    return datetime.datetime.now().strftime('%H:%M:%S')

class CodeChangeEventHandler(FileSystemEventHandler):
    def __init__(self, modules_to_monitor, on_modified_callback):
        self.modules_to_monitor = modules_to_monitor
        self.on_modified_callback = on_modified_callback
        self.modified_modules = set()

    def on_modified(self, event):
        # Check if modified file is one of the modules to monitor
        modified_file = event.src_path
        module_name = self.get_module_name(modified_file)
        if (module_name in self.modules_to_monitor) and (module_name not in self.modified_modules):
            # Execute your command or function here
            print(f"{formatted_timestamp()}: Module {module_name} was modified.")
            self.modified_modules.add(module_name)

    @staticmethod
    def get_module_name(filename):
        # Convert filename to module name
        module_name = os.path.relpath(filename).replace('.py', '').replace('/', '.')
        if module_name.startswith('.'):
            module_name = module_name[1:]
        return module_name


async def observe_modules(modules_to_monitor, on_modified_callback):
    # Create an observer and event handler
    event_handler = CodeChangeEventHandler(modules_to_monitor, on_modified_callback)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)

    # Start the observer
    observer.start()

    try:
        # Keep the observer running until interrupted
        print(f"{formatted_timestamp()}: Monitoring for file changes in following modules:")
        print(modules_to_monitor)
        while True:
            time.sleep(1)
            if bool(event_handler.modified_modules):
                event_handler.modified_modules.clear()
                print(f"{datetime.datetime.now().strftime('%H:%M:%S')}: Regenerating diagram...")
                await event_handler.on_modified_callback()
                print(f"{formatted_timestamp()}: Monitoring for file changes...")
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
