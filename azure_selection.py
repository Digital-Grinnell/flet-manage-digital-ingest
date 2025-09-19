import flet as ft
import utils


# Class constructor
# ---------------------------------------------------------------
class AzureSelectionContainer(ft.Container):
    
    # Define attribute for the inner container
    collection_options_container = ft.Container(
        padding=10,
        bgcolor=ft.Colors.LIGHT_GREEN_200,
        border_radius=10,
        visible=False,
        content=ft.Column(
            controls=[
                ft.Text(
                    "Collection Builder Options",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.RadioGroup(
                    content=ft.Column(controls=utils.load_radio_options_from_json("./cb_collections.json"), expand=True, spacing=0),
                )
            ],
        ),
    )

    def blob_radio_group_changed(self, e):
        """Event handler for the main RadioGroup."""
        page = e.page
        if e.control.value == "collectionbuilder":
            self.collection_options_container.visible = True
        else:
            self.collection_options_container.visible = False
        page.update( )


    # Class constructor
    # ---------------------------------------------------------------
    def __init__(self, **kwargs):

        super().__init__(
            content=ft.Column(
                controls=[
                    # The container heading
                    ft.Text(
                        "Azure Blob Storage Selection", 
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    
                    ft.RadioGroup(
                        content=ft.Column(controls=utils.load_radio_options_from_json("./azure_blobs.json"), expand=True, spacing=0),
                        on_change=self.blob_radio_group_changed,
                    ),
            
                    # The nested light green container, controlled by visibility
                    self.collection_options_container,

                ],  
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
                spacing=0,
            ),
            padding=10,
            bgcolor=ft.Colors.LIGHT_BLUE,
            border_radius=10,    
            width=800, 
            **kwargs
        )


