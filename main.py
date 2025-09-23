# FilePicker does NOT work in macOS w/ Flet version 0.28.3 due to permissions/security, so we need to run 
# it as a browser app, OR degrade to Flet 0.28.2 which does work in macOS.  See https://github.com/flet-dev/flet/issues/5334#issuecomment-3065024264

import flet as ft
import my_logger
from status import StatusContainer
from mode_selection import ModeSelectionContainer
from main_menu import MainMenuContainer
from azure_selection import AzureSelectionContainer
from object_selection import ObjectSelectionContainer

# AI: Create a Flet app as a Class with page as an attribute.
# To create a Flet app in an object-oriented way, define a class that takes and stores the page object as an attribute, then build the interface inside the class using methods. Here’s how to structure a basic Flet app in this style:

class MyApp:
    
    # MyApp's class constructor definiing the app and main page.
    # ---------------------------------------------------------------------------
    def __init__(self, page: ft.Page):
        logger = my_logger.init_logger( )

        # Log messages
        logger.info(f"Initialized logging for {__name__}")

        # Set up the page
        self.page = page
        self.page.title = "Flet Manage Digital Ingest"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.height = 1000
        self.page.spacing = 5

        # Other 'globals'
        self.page.session.set("mode", None)
        self.page.session.set("logger", logger)
        if not self.page.session.contains_key("selected_object_paths"):
            self.page.session.set("selected_object_paths", [ ])  # set up an empty list to hold selected files/paths

        # Create a SnackBar instance for displaying messages
        self.page.snack_bar = ft.SnackBar(
            content=ft.Markdown( ),
            bgcolor=ft.Colors.RED_600
        )

        # Create containers from defined classes in other modules
        main_menu_container = MainMenuContainer( )
        mode_container = ModeSelectionContainer( )
        azure_selection_container = AzureSelectionContainer( )
        object_selection_container = ObjectSelectionContainer( )
        status_container = StatusContainer( )
    
        # Save references to the containers in page.session for access from other modules
        self.page.session.set("status_container", status_container)  # Save a reference to the status container in session for logging messages from other modules   
        self.page.session.set("object_selection_container", object_selection_container)  # Save a reference to the object selection container in session for updating from other modules   
        self.page.session.set("azure_selection_container", azure_selection_container)  # Save a reference to the azure selection container in session for updating from other modules   
        self.page.session.set("mode_container", mode_container)  # Save a reference to the mode selection container in session for updating from other modules           

        # Add the controls to the page in the order they should appear
        self.page.add(
            ft.Column(
                controls=[
                    main_menu_container,
                    mode_container, 
                    azure_selection_container,
                    object_selection_container,
                    status_container,
                ],
                expand=True,
            ),
        )
        
        # Add the file_picker container as an overlay
        self.page.overlay.append(ObjectSelectionContainer.file_picker)

# Simple 'main' method to run the app.
# ------------------------------------------------------------------------
def main(page: ft.Page):
    app = MyApp(page)

ft.app(target=main)


