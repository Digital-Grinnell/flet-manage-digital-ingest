import flet as ft
import utils

# Defines a Flet container class to promote common use of a container for McFate apps
class McFateFletContainer(ft.Container):
    
    # Class constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):

        # Handle the title argument if passed, otherwise set a default title
        self.title = "Pass a title to the McFateFletContainer or `title=None` to suppress this message"
        if "title" in kwargs:
            self.title = kwargs.pop("title")
            if self.title is None:
                self.title = ""

        # Handle any "controls" array argument if passed, otherwise set default options    
        self.control_args = [ft.Markdown(f"No control args array was passed to McFateFletContainer")]
        if "controls" in kwargs:
            self.control_args = kwargs.pop("controls")
            if self.control_args is None:
                self.control_args = [ ]

        # Handle 'background' argument if passed, otherwise set a default color
        self.background_color = ft.Colors.GREY_300
        if "background" in kwargs:
            self.background_color = kwargs.pop("background")          

        # Call the parent constructor to create the container
        super( ).__init__(

            # Add a Column to the container to hold the title and other controls
            content=ft.Column(
                controls=[
                    # The container heading
                    ft.Text(
                        self.title,
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        # text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                ],  
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                spacing=0,
            ),
            padding=10,
            bgcolor=self.background_color,
            border_radius=10,    
            width=800, 
            **kwargs
        )

        # If any controls were passed, add them to the Column's controls
        if self.control_args:
            for control in self.control_args:
                self.content.controls.append(control)   


