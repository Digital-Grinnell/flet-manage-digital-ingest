import flet as ft
import utils

class MainMenuContainer(ft.Container):
    
    # Class constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):

        super().__init__(ft.Container(
            content=ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Home",
                        icon=ft.Icons.HOME,
                        on_click=lambda e: print("Home button clicked")
                    ),

                    # ft.ElevatedButton(
                    #     text="Profile",
                    #     icon=ft.Icons.PERSON,
                    #     on_click=lambda e: print("Profile button clicked")
                    # ),

                    # ft.ElevatedButton(
                    #     text="Settings",
                    #     icon=ft.Icons.SETTINGS,
                    #     on_click=lambda e: print("Settings button clicked")
                    # ),

                    # Define the close_button
                    close_button := ft.ElevatedButton(
                        text="Close App",
                        icon=ft.Icons.CLOSE,
                        on_click=utils.close_app
                    ),

                    # Create an ElevatedButton 'Create Selected Derivatives' with the click event handler
                    create_derivatives_button := ft.ElevatedButton(
                        text="Create Selected",
                        icon=ft.Icons.ADD_OUTLINED,
                        on_click=utils.process_files
                    ),
                ],
                # Align buttons horizontally in the center
                alignment=ft.MainAxisAlignment.CENTER,
                # Add spacing between the buttons
                spacing=5,
            ),
        ),  

        # Container styling
        padding=ft.padding.all(10),
        bgcolor=ft.Colors.with_opacity(1, ft.Colors.RED),
        border_radius=ft.border_radius.all(10),
    )

