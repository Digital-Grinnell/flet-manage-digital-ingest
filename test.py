import flet as ft

# class SingleColumnContainer(ft.Column):
#     def __init__(self, controls=None, **kwargs):
#         super().__init__(
#             controls=controls if controls else [],
#             **kwargs
#         )

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
                    ft.Row([self.result_text, self.progress_bar], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
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


    # # Create a container to display process status/output.
    # # -----------------------------------------------------------
    # status_container = ft.Container(
    #     content=ft.Column(
    #         scroll=ft.ScrollMode.ADAPTIVE,
    #         expand=True,
    #         controls=[
    #             ft.Text(
    #                 "Status",
    #                 size=18,
    #                 weight=ft.FontWeight.BOLD,
    #                 text_align=ft.TextAlign.CENTER,
    #             ),
    #             # Add a text area and progress_bar to display the result of operations
    #             ft.Row([result_text, progress_bar], alignment=ft.MainAxisAlignment.CENTER, wrap=True),
    #         ],
    #         spacing=0,
    #     ),
    #     padding=10,
    #     bgcolor=ft.Colors.GREEN_100,
    #     border_radius=10,     

    # )


def main(page: ft.Page):
    status = StatusContainer( )
    page.add(status)

    status.result_text.value = "Hello, World!"
    status.progress_bar.value = 0.5
    page.update( )
  

ft.app(main)
