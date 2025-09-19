import flet as ft
import utils
import os


# Class constructor
# ---------------------------------------------------------------
class ObjectSelectionContainer(ft.Container):

    # Controls for the nested container (initially empty)
    nested_controls_radio_group = ft.RadioGroup(content=ft.Column(spacing=0))
    nested_container = ft.Container(
        content=nested_controls_radio_group,
        visible=False,
        bgcolor=ft.Colors.WHITE,
        padding=10,
        border_radius=10,
    )

    def files_radio_group_changed(e):
        """Handler for the radio group selection change."""

        page = e.page
        logger = utils.get_logger( )
        selected_path = e.control.value
        logger.info(f"Selected option: {selected_path}")

        # # Clear any previously nested controls no matter what the new selection is
        # # nested_controls_radio_group.content.controls.clear( )
        # nested_container.visible = False
        # page.update( )

        expanded_path = None

        # Check if the selected path contains a slash indicating it IS a path
        if '/' in selected_path:
            # If the selected_path begins with a tilde, translate that into the user's home directory
            if selected_path.startswith("~"):
                expanded_path = os.path.expanduser(selected_path)
            else:
                expanded_path = selected_path
            
            # Check if the selected path is NOT a valid directory
            if not os.path.isdir(expanded_path):
                msg = f"Selected option '{expanded_path}' does not appear to be a valid path. Is it mapped to this device?"
                logger.error(msg)
                utils.show_message(page, msg, True)
            else:  # Hide the nested container if the path is valid, and call open_file_picker( )
                msg = f"Selected option '{expanded_path}' yields a valid path. Launching the file picker."
                logger.info(msg)
                utils.show_message(page, msg, False)
                # nested_container.visible = False
                # open_file_picker(e)

        else:  # Choosing the fuzzy search option, reading a list of filenames from a worksheet
            msg = f"Sorry, this option has not been implemented.  Check back later, please."
            logger.error(msg)
            utils.show_message(page, msg, True)

            # # Populate the nested container with controls
            # nested_controls_radio_group.content.controls.clear( )
            # nested_controls_radio_group.content.controls.append(
            #     ft.Text(f"Contents of {selected_path}:", weight=ft.FontWeight.BOLD)
            # )
            # # Example: add placeholder radio buttons for further selection
            # nested_controls_radio_group.content.controls.extend([
            #     ft.Radio(value="option1", label="Option 1 from directory"),
            #     ft.Radio(value="option2", label="Option 2 from directory"),
            # ])
            # nested_container.visible = True
            
        page.update( )



    # Class constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):

        super().__init__(
            content=ft.Column(
                controls=[
                    # The container heading
                    ft.Text(
                        "Object File Selection", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.RadioGroup(
                        content=ft.Column(controls=utils.load_radio_options_from_json("./file_sources.json"), expand=True, spacing=0),
                        on_change=self.files_radio_group_changed,
                    ),
                ],  
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                spacing=0,
            ),
            padding=10,
            bgcolor=ft.Colors.PURPLE_100,
            border_radius=10,    
            width=800, 
            **kwargs
        )


