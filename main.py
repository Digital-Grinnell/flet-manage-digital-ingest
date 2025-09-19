# FilePicker does NOT work in macOS w/ Flet version 0.28.3 due to permissions/security, so we need to run 
# it as a browser app, OR degrade to Flet 0.28.2 which does work in macOS.  See https://github.com/flet-dev/flet/issues/5334#issuecomment-3065024264

import flet as ft
import os
import utils
import json
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
    
    # Function to open the file picker dialog
    # This is called when a valid directory option is selected in the file selection RadioGroup
    # -----------------------------------------------------------
    def open_file_picker(e):
        """
        Function to open the file picker dialog.
        """
        file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=["jpg", "jpeg", "png", "pdf", ".tiff", "tif"],
            dialog_title="Select multiple images and/or PDF files",
            initial_directory=e.control.value
        )
        
    # Callback function to handle the result of the file picker dialog
    # This function saves the selected files/paths in ft.page.session for later processing
    # -----------------------------------------------------------
    def pick_files_result(e: ft.FilePickerResultEvent):
        """
        Callback function executed when the file picker dialog is closed.
        It updates the UI and passes the selected file/paths to ft.page.session ...the processing function.
        """
        if e.files:
            num_files = len(e.files)
            directory = os.path.dirname(e.files[0].path)
            result_text.value = f"{num_files} files selected from {directory}."
            
            # Clear the previous selection
            page.session.set("selected_object_paths", [ ])
            objects = page.session.get("selected_object_paths")
            
            # Loop through the selected files and log their paths. Append each path to page.session[selected_object_paths]
            for file in e.files:
                logger.info(f"Selected file: {file.name} (Path: {file.path})")  
                status_container.result_text.value += f"\n- {file.name}"  
                objects.append(file.path)
                page.update( )
            utils.show_message(page, f"{num_files} files selected from {directory}.")
            page.session.set("selected_object_paths", objects)
            page.update( )
            # process_files(page, directory, e.files)  # Pass the list of files to the processing function
        else:
            status_container.result_text.value = "Selection cancelled."
            utils.show_message(page, "File selection was cancelled.", is_error=True)
            page.session.set

        page.update( )
    
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

    
    # # Digital Object File Selection
    # # =================================================================================================
    
    # # Build a purple Flet container to hold Digital Object File Selection options with a RadioGroup of 
    # # file_selection controls read from file_sources.json. If the selected option is a valid file path add 
    # # a nested white Flet container with a to be determined RadioGroup of controls.  Add a Flet ElevatedButton 
    # # with a title of "Select Files" and on_change action named select_files, plus another ElevatedButton with 
    # # a title of "Process Files" and on_change action process_files.  
    
    # # Controls for the nested container (initially empty)
    # nested_controls_radio_group = ft.RadioGroup(content=ft.Column(spacing=0))
    # nested_container = ft.Container(
    #     content=nested_controls_radio_group,
    #     visible=False,
    #     bgcolor=ft.Colors.WHITE,
    #     padding=10,
    #     border_radius=10,
    # )

    # # def select_files(e):
    # #     """Action for the "Select Files" button."""
    # #     logger.info("Select Files button clicked.")
    # #     # Add your file selection logic here.
    # #     # For example, open a file picker or perform file-related operations.
    # #     # The nested_controls_radio_group can be populated here.
    # #     page.update( )

        
    # def files_radio_group_changed(e):
    #     """Handler for the radio group selection change."""
    #     selected_path = e.control.value
    #     logger.info(f"Selected option: {selected_path}")

    #     # Clear any previously nested controls no matter what the new selection is
    #     nested_controls_radio_group.content.controls.clear( )
    #     nested_container.visible = False
    #     page.update( )

    #     expanded_path = None

    #     # Check if the selected path contains a slash indicating it IS a path
    #     if '/' in selected_path:
    #         # If the selected_path begins with a tilde, translate that into the user's home directory
    #         if selected_path.startswith("~"):
    #             expanded_path = os.path.expanduser(selected_path)
    #         else:
    #             expanded_path = selected_path
            
    #         # Check if the selected path is NOT a valid directory
    #         if not os.path.isdir(expanded_path):
    #             msg = f"Selected option '{expanded_path}' does not appear to be a valid path. Is it mapped to this device?"
    #             logger.error(msg)
    #             utils.show_message(page, msg, True)
    #         else:  # Hide the nested container if the path is valid, and call open_file_picker( )
    #             nested_container.visible = False
    #             open_file_picker(e)

    #     else:  # Choosing the fuzzy search option, reading a list of filenames from a worksheet
    #         msg = f"Sorry, this option has not been implemented.  Check back later, please."
    #         logger.error(msg)
    #         utils.show_message(page, msg, True)

    #         # # Populate the nested container with controls
    #         # nested_controls_radio_group.content.controls.clear( )
    #         # nested_controls_radio_group.content.controls.append(
    #         #     ft.Text(f"Contents of {selected_path}:", weight=ft.FontWeight.BOLD)
    #         # )
    #         # # Example: add placeholder radio buttons for further selection
    #         # nested_controls_radio_group.content.controls.extend([
    #         #     ft.Radio(value="option1", label="Option 1 from directory"),
    #         #     ft.Radio(value="option2", label="Option 2 from directory"),
    #         # ])
    #         # nested_container.visible = True
            
    #     page.update( )

    # # Read file sources from JSON
    # try:
    #     with open(file_sources_JSON, "r") as f:
    #         file_sources = json.load(f)
    # except FileNotFoundError:
    #     file_sources = [f"Error: {file_sources_JSON} not found"]
    # except json.JSONDecodeError:
    #     file_sources = [f"Error: Could not decode {file_sources_JSON}"]

    # # Create the main RadioGroup
    # file_selection_radios = ft.RadioGroup(
    #     content=ft.Column(
    #         [ft.Radio(value=source, label=source) for source in file_sources],
    #         expand=True,
    #         spacing=0
    #     ),
    #     on_change=files_radio_group_changed,
    # )

    # # Main object_files container
    # object_files_container = ft.Container(
    #     content=ft.Column(
    #         [
    #             ft.Text(
    #                 "Digital Object File Selection",
    #                 size=18,
    #                 weight=ft.FontWeight.BOLD,
    #                 text_align=ft.TextAlign.CENTER,
    #             ),
    #             file_selection_radios,
    #             nested_container,  # Nested white container
        
    #         ],
    #         spacing=0
    #     ),
    #     padding=10,
    #     bgcolor=ft.Colors.PURPLE_100,
    #     border_radius=10,
    # )
    

    # Create containers from defined classes
    # -----------------------------------------------------------
    main_menu_container = MainMenuContainer( )
    mode_container = ModeSelectionContainer( )
    azure_selection_container = AzureSelectionContainer( )
    object_selection_container = ObjectSelectionContainer( )
    status_container = StatusContainer( )
    

    
    
    
    
    
    
    
    
    
    
    

    # Add the controls to the page
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


if __name__ == "__main__":
    ft.app(target=main)
