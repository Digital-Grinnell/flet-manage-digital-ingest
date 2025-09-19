# FilePicker does NOT work in macOS w/ Flet version 0.28.3 due to permissions/security, so we need to run 
# it as a browser app, OR degrade to Flet 0.28.2 which does work in macOS.  See https://github.com/flet-dev/flet/issues/5334#issuecomment-3065024264

import flet as ft
import os
import utils
import my_logger
from status import StatusContainer
from mode_selection import ModeSelectionContainer
from main_menu import MainMenuContainer
from azure_selection import AzureSelectionContainer
from object_selection import ObjectSelectionContainer


# Main function
# ---------------------------------------------------------------
def main(page: ft.Page):

    logger = my_logger.init_logger( )

    # Log messages
    logger.info(f"Initialized logging for {__name__}")

    # Other 'globals'
    page.session.set("mode", None)
    page.session.set("logger", logger)
    if not page.session.contains_key("selected_object_paths"):
        page.session.set("selected_object_paths", [ ])  # set up an empty list to hold selected files/paths
    
        
    
    # --- Main Page Setup ---
    
    # Set up the page title and theme
    page.title = "Flet Manage Digital Ingest"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.height = 1000
    page.spacing = 5

    # # Does setting the working directory here help with file paths?  Yes, somewhat.
    # os.chdir(os.path.dirname("/Users/mcfatem/"))
    # logger.info(f"Current working directory: {os.getcwd()}")
    # logger.info(f"Script directory: {os.path.dirname(__file__)}")

    # Create a SnackBar instance for displaying messages
    page.snack_bar = ft.SnackBar(
        content=ft.Markdown( ),
        bgcolor=ft.Colors.RED_600
    )

    # Create containers from defined classes in other modules
    # -----------------------------------------------------------
    main_menu_container = MainMenuContainer( )
    mode_container = ModeSelectionContainer( )
    azure_selection_container = AzureSelectionContainer( )
    object_selection_container = ObjectSelectionContainer( )
    status_container = StatusContainer( )
    
    # Save references to the containers in page.session for access from other modules
    # -----------------------------------------------------------
    page.session.set("status_container", status_container)  # Save a reference to the status container in session for logging messages from other modules   
    page.session.set("object_selection_container", object_selection_container)  # Save a reference to the object selection container in session for updating from other modules   
    page.session.set("azure_selection_container", azure_selection_container)  # Save a reference to the azure selection container in session for updating from other modules   
    page.session.set("mode_container", mode_container)  # Save a reference to the mode selection container in session for updating from other modules           

    
    # Add the controls to the page in the order they should appear
    # -----------------------------------------------------------
    page.add(
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
    page.overlay.append(ObjectSelectionContainer.file_picker)


if __name__ == "__main__":
    ft.app(target=main)
