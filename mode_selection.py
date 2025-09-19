import flet as ft
import utils

class ModeSelectionContainer(ft.Container):
    
    # # Define attributes for result_text and progress_bar
    # result_text = ft.Markdown(value="Nothing to display.")
    # progress_bar = ft.ProgressBar(width="90%", value=0.0)

    # Define the change event handler for the RadioGroup
    def mode_radio_group_changed(e):
        page = e.page
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
        on_change = mode_radio_group_changed,
    )

    # Class constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):

        super().__init__(
            content=ft.Column(
                controls=[
                    # The container heading
                    ft.Text(
                        "Select Processing Mode", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    self.mode_options
                ],  
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                spacing=0,
            ),
            padding=10,
            bgcolor=ft.Colors.GREY_300,
            border_radius=10,    
            width=800, 
            **kwargs
        )



    # # Build a light gray Flet container to hold Processing Mode options with a RadioGroup of controls for 
    # # 'Alma' or 'CollectionBuilder' modes. 
    
    # # Define the change event handler for the RadioGroup
    # def mode_radio_group_changed(e):
    #     mode = e.control.value
    #     page.session.set("mode", mode)
    #     msg = f"Selected processing mode: '{mode}'"
    #     utils.show_message(page, msg, False)
        
    #     # Add logic here to handle the selection, for example:
    #     # if e.control.value == "Alma":
    #     #     ...
    #     # elif e.control.value == "CollectionBuilder":
    #     #     ...

    # # Create the RadioGroup with the two radio buttons
    # mode_options = ft.RadioGroup(
    #     content=ft.Column(
    #         controls=[
    #             ft.Radio(value="Alma", label="Alma"),
    #             ft.Radio(value="CollectionBuilder", label="CollectionBuilder"),
    #         ],
    #         expand=True,
    #         spacing=0
    #     ),
    #     on_change=mode_radio_group_changed,
    # )

    # # Create the light gray container
    # processing_mode_container = ft.Container(
    #     content=ft.Column(
    #         controls=[
    #             ft.Text(
    #                 "Processing Mode",
    #                 size=18,
    #                 weight=ft.FontWeight.BOLD,
    #                 text_align=ft.TextAlign.CENTER,
    #             ),
    #             mode_options,
    #         ],
    #         expand=True,
    #     ),
    #     # Use a gray color for the background
    #     bgcolor=ft.Colors.GREY_300,
    #     padding=10,
    #     border_radius=10
    # )

