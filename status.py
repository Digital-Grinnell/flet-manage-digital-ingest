import flet as ft

class StatusContainer(ft.Container):
    
    # Define attributes for result_text and progress_bar
    result_text = ft.Markdown(value="Nothing to display.")
    progress_bar = ft.ProgressBar(width="90%", value=0.0)

    # Class constructor
    def __init__(self, **kwargs):

        super().__init__(
            content=ft.Column(
                controls=[
                    # The container heading
                    ft.Text(
                        "Status", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    # Add rows of text area and progress_bar to display the result of operations
                    ft.Row([self.result_text, self.progress_bar], 
                           wrap=True, 
                           # alignment=ft.MainAxisAlignment.LEFT
                           ),
                ],  
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                spacing=0,
            ),
            padding=10,
            bgcolor=ft.Colors.GREEN_100,
            border_radius=10,    
            width=800, 
            **kwargs
        )



# def main(page: ft.Page):
#     status = StatusContainer( )
#     page.add(status)

#     status.result_text.value = "Hello, World!"
#     status.progress_bar.value = 0.5
#     page.update( )
  

# ft.app(main)
