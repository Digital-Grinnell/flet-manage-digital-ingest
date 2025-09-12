# FilePicker does NOT work in macOS due w/ Flet version 0.28.3 due to permissions/security, so we need to run 
# it as a browser app, OR degrade to Flet 0.28.2 which does work in macOS.  See https://github.com/flet-dev/flet/issues/5334#issuecomment-3065024264

import flet as ft
import os
import utils
import json
import logging

def main(page: ft.Page):
    
    # Configure basic logging
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='flet-manage-digital-ingest.log',
        filemode='a')

    # You can also specify the date format more precisely
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')

    # Get a logger instance
    logger = logging.getLogger(__name__)

    # Log messages
    logger.info(f"Initialized logging for {__name__}")
    
    # JSON config files...
    azure_blobs_JSON = "./azure_blobs.json"
    cb_collections_JSON = "./cb_collections.json"
    file_sources_JSON = "./file_sources.json"
    
    # Other 'globals'
    page.session.set("mode", None)
    page.session.set("logger", logger)
    
    # Function to open the file picker dialog
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
    def pick_files_result(e: ft.FilePickerResultEvent):
        """
        Callback function executed when the file picker dialog is closed.
        It updates the UI and passes the selected files to the processing function.
        """
        if e.files:
            num_files = len(e.files)
            directory = os.path.dirname(e.files[0].path)
            result_text.value = f"{num_files} files selected from {directory}."
            # Loop through the selected files and print their names and paths
            for file in e.files:
                logger.info(f"Selected file: {file.name} (Path: {file.path})")  
                result_text.value += f"\n- {file.name}"  
                page.update( )
            utils.show_message(page, f"{num_files} files selected from {directory}.")
            page.update( )
            process_files(page, directory, e.files)  # Pass the list of files to the processing function
        else:
            result_text.value = "Selection cancelled."
            utils.show_message(page, "File selection was cancelled.", is_error=True)
        page.update( )

    # Function to process the selected files
    def process_files(page, directory, files):
        """
        This is the processing function tasked with creating image derivatives.
        It receives a list of selected files and the directory they are located in.
        """
        result_text.value = "Processing..."
        page.update( )
        
        if files:
            logger.info(f"Processing {len(files)} files from {directory}...")
            for file in files:
                logger.info(f"  - {file.name} (Path: {file.path})")
            
            done = 0.0

            for file in files:
                derivative = utils.create_derivative(page,
                    mode=page.session.get("mode"),
                    derivative_type='thumbnail',
                    index=0,
                    url=f"http://example.com/objs/{file.name}",
                    local_storage_path=file.path,
                    blob_service_client=None
                )
                done += 0.5
                progress_bar.value = done / len(files)  # Update progress bar value
                result_text.value += f"\n- {derivative}"  
                page.update( )

                derivative = utils.create_derivative(page,
                    mode=page.session.get("mode"),
                    derivative_type='small',
                    index=0,
                    url=f"http://example.com/objs/{file.name}",
                    local_storage_path=file.path,
                    blob_service_client=None
                )
                done += 0.5
                progress_bar.value = done / len(files)  # Update progress bar value
                result_text.value += f"\n- {derivative}"  
                page.update( )

            utils.show_message(page, f"Processed {len(files)} files from {directory}.")
                
        else:
            logger.info("No files were selected for processing.")
            utils.show_message(page, "No files were selected for processing.", is_error=True)
    
    # --- Main Page Setup ---
    
    # Set up the page title and theme
    page.title = "Flet Create Image Derivatives"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.height = 1000
    page.spacing = 5

    # Display text to show the result of the file selection
    result_text = ft.Markdown(value="No files selected.")
    # Create a ProgressBar control (determinate)
    progress_bar = ft.ProgressBar(width="90%", value=0.0)

    # # Does setting the working directory here help with file paths?  Yes, somewhat.
    # os.chdir(os.path.dirname("/Users/mcfatem/"))
    # logger.info(f"Current working directory: {os.getcwd()}")
    # logger.info(f"Script directory: {os.path.dirname(__file__)}")

    # Create an instance of the FilePicker control
    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)
        
    # Create a SnackBar instance for displaying messages
    page.snack_bar = ft.SnackBar(
        content=ft.Markdown( ),
        bgcolor=ft.Colors.RED_600
    )
    
    # Build a light gray Flet container to hold Processing Mode options with a RadioGroup of controls for 
    # 'Alma' or 'CollectionBuilder' modes. 
    
    # Define the change event handler for the RadioGroup
    def mode_radio_group_changed(e):
        mode = e.control.value
        page.session.set("mode", mode)
        msg = f"Selected processing mode: '{mode}'"
        utils.show_message(page, msg, False)
        
        # Add logic here to handle the selection, for example:
        # if e.control.value == "Alma":
        #     ...
        # elif e.control.value == "CollectionBuilder":
        #     ...

    # Create the RadioGroup with the two radio buttons
    mode_options = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(value="Alma", label="Alma"),
                ft.Radio(value="CollectionBuilder", label="CollectionBuilder"),
            ],
            expand=True,
            spacing=0
        ),
        on_change=mode_radio_group_changed,
    )

    # Create the light gray container
    processing_mode_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Processing Mode",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                mode_options,
            ],
            expand=True,
        ),
        # Use a gray color for the background
        bgcolor=ft.Colors.GREY_300,
        padding=10,
        border_radius=10
    )

    # Build a light blue Flet container to hold Azure Blob Storage options with a RadioGroup of control values and labels 
    # read from 'azure_blob.json' containers. If 'collectionbuilder' is selected, add a light 
    # green container and RadioGroup of options read from the cb_collections.json file.
    
    # Placeholder for the inner container, initially hidden
    collection_options_container = ft.Container(visible=False)

    def load_blob_options():
        """Loads radio options from a .json file."""
        try:
            with open(azure_blobs_JSON, "r") as f:
                data = json.load(f)
                options = [
                    ft.Radio(value=item, label=item)
                    for item in data["options"]
                ]
            return options
        except FileNotFoundError:
            return [ft.Text(f"Error: {azure_blobs_JSON} not found.")]


    def load_collection_options():
        """Loads radio options from a .json file."""
        try:
            with open(cb_collections_JSON, "r") as f:
                data = json.load(f)
                options = [
                    ft.Radio(value=item, label=item)
                    for item in data["options"]
                ]
            return options
        except FileNotFoundError:
            return [ft.Text(f"Error: {cb_collections_JSON} not found.")]

    def blob_radio_group_changed(e):
        """Event handler for the main RadioGroup."""
        if e.control.value == "collectionbuilder":
            collection_options_container.visible = True
        else:
            collection_options_container.visible = False
        page.update()

    # The main light blue container
    blob_main_container = ft.Container(
        # width=400,
        padding=10,
        bgcolor=ft.Colors.LIGHT_BLUE_100,
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Azure Blob Storage Container Selection",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.RadioGroup(
                    content=ft.Column(controls=load_blob_options(), expand=True, spacing=0),
                    on_change=blob_radio_group_changed,
                ),
                # The nested light green container, controlled by visibility
                collection_options_container,
            ],
            spacing=0
        )
    )

    # The inner light green container, populated with JSON data
    collection_options_container.content = ft.Container(
        padding=10,
        bgcolor=ft.Colors.LIGHT_GREEN_200,
        border_radius=10,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Collection Builder Options",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.RadioGroup(
                    content=ft.Column(controls=load_collection_options(), expand=True)
                )
            ],
            expand=True,
            spacing=0
        ),
    )
    
    
    # Build a purple Flet container to hold Digital Object File Selection options with a RadioGroup of 
    # file_selection controls read from file_sources.json. If the selected option is a valid file path add 
    # a nested white Flet container with a to be determined RadioGroup of controls.  Add a Flet ElevatedButton 
    # with a title of "Select Files" and on_change action named select_files, plus another ElevatedButton with 
    # a title of "Process Files" and on_change action process_files.  
    
    # Controls for the nested container (initially empty)
    nested_controls_radio_group = ft.RadioGroup(content=ft.Column(spacing=0))
    nested_container = ft.Container(
        content=nested_controls_radio_group,
        visible=False,
        bgcolor=ft.Colors.WHITE,
        padding=10,
        border_radius=10,
    )

    def select_files(e):
        """Action for the "Select Files" button."""
        logger.info("Select Files button clicked.")
        # Add your file selection logic here.
        # For example, open a file picker or perform file-related operations.
        # The nested_controls_radio_group can be populated here.
        page.update()

    # def process_files(e):
    #     """Action for the "Process Files" button."""
    #     logger.info("Process Files button clicked.")
    #     # Add your file processing logic here.
    #     page.update()
        
    def files_radio_group_changed(e):
        """Handler for the radio group selection change."""
        selected_path = e.control.value
        logger.info(f"Selected option: {selected_path}")

        # Check if the selected path is NOT a valid directory
        if not os.path.isdir(selected_path):
            # Populate the nested container with controls
            nested_controls_radio_group.content.controls.clear()
            nested_controls_radio_group.content.controls.append(
                ft.Text(f"Contents of {selected_path}:", weight=ft.FontWeight.BOLD)
            )
            # Example: add placeholder radio buttons for further selection
            nested_controls_radio_group.content.controls.extend([
                ft.Radio(value="option1", label="Option 1 from directory"),
                ft.Radio(value="option2", label="Option 2 from directory"),
            ])
            nested_container.visible = True
        else:
            # Hide the nested container if the path is valid, and call open_file_picker( )
            nested_container.visible = False
            open_file_picker(e)
        
        page.update( )

    # Read file sources from JSON
    try:
        with open(file_sources_JSON, "r") as f:
            file_sources = json.load(f)
    except FileNotFoundError:
        file_sources = [f"Error: {file_sources_JSON} not found"]
    except json.JSONDecodeError:
        file_sources = [f"Error: Could not decode {file_sources_JSON}"]

    # Create the main RadioGroup
    file_selection_radios = ft.RadioGroup(
        content=ft.Column(
            [ft.Radio(value=source, label=source) for source in file_sources],
            expand=True,
            spacing=0
        ),
        on_change=files_radio_group_changed,
    )

    # Main object_files container
    object_files_container = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Digital Object File Selection",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                file_selection_radios,
                nested_container,  # Nested white container
        
                # Add a text area to display the result of the file selection
                ft.Row([result_text, progress_bar], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
                
                # # Add a text area to display the results of file processing
                # ft.Row([processing_results_text], alignment=ft.MainAxisAlignment.CENTER),


                # ft.Row(
                #     [
                #         ft.ElevatedButton(text="Select Files", on_click=select_files),
                #         ft.ElevatedButton(text="Process Files", on_click=process_files),
                #     ],
                # ),
            ],
            spacing=0
        ),
        expand=True,
        padding=10,
        bgcolor=ft.Colors.PURPLE_100,
        border_radius=10,
    )
    
    # close_app( ) callback function
    def close_app(e):
        page.window.close()

    # Define the close_button
    close_button = ft.ElevatedButton(
        text="Close App",
        icon=ft.Icons.CLOSE,
        on_click=close_app
    )







    
    
    
    
    
    
    
    
    
    
    
    

    # Add the controls to the page
    # -----------------------------------------------------------
    page.add(
        ft.Column(
            controls=[
                processing_mode_container, 
                blob_main_container,
                object_files_container,
                close_button,
            ],
            expand=True,
        ),
        
            
        # processing_mode_container, 
        # blob_main_container,
        # object_files_container,
        
        # # Add a text area to display the result of the file selection
        # ft.Row(
        #     [
        #         result_text
        #     ],
        #     alignment=ft.MainAxisAlignment.CENTER,
        # )
    )


if __name__ == "__main__":
    ft.app(target=main)
