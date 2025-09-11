# Flet Manage Digital Ingest

## Setup Command Sequence

```zsh
mkdir flet-manage-digital-ingest
cd flet-manage-digital-ingest
python3.12 -m venv .venv
code .
source /Users/mcfatem/GitHub/flet-manage-digital-ingest/.venv/bin/activate
pip3 install 'flet[all]'
pip install --upgrade pip
```

## Prompt

Initial code here was created using AI from the following prompt...  

```
Create a single page Flet app using ft.FilePicker to select a multiple image or PDF files and return pass them to an undefined processing function.
```

## AI Result

To create a Flet app that selects multiple image and PDF files, you need to use the  control. You must set  and configure the  to  with a list of . The selected files will be available in the event data of the  callback, from which they can be passed to your processing function. 
The following Python code provides a single-page Flet application that demonstrates this functionality: 

1. A button triggers the file picker dialog. 
2. The dialog is configured to allow multiple selections of JPEG, PNG, and PDF files. 
3. An  callback function is used to handle the selection. 
4. Inside the callback, the selected files are passed to a placeholder  function. 
5. A  control is used to display the number of selected files for user feedback. 


## Code

The code that AI created...  

```py
import flet as ft

def process_files(files):
    """
    This is the undefined processing function.
    You can add your custom logic here to handle the selected files.
    """
    if files:
        print(f"Processing {len(files)} files...")
        for file in files:
            print(f"  - {file.name} (Path: {file.path})")
    else:
        print("No files were selected for processing.")

def main(page: ft.Page):
    # Set up the page title and theme
    page.title = "Multi-File Picker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Display text to show the result of the file selection
    result_text = ft.Text(value="No files selected.", size=18)

    def pick_files_result(e: ft.FilePickerResultEvent):
        """
        Callback function executed when the file picker dialog is closed.
        It updates the UI and passes the selected files to the processing function.
        """
        if e.files:
            num_files = len(e.files)
            result_text.value = f"{num_files} files selected."
            process_files(e.files)  # Pass the list of files to the processing function
        else:
            result_text.value = "Selection cancelled."
            process_files(None)
        page.update()

    # Create an instance of the FilePicker control
    file_picker = ft.FilePicker(on_result=pick_files_result)
    page.overlay.append(file_picker)

    def open_file_picker(e):
        """
        Function to open the file picker dialog.
        """
        file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=["jpg", "jpeg", "png", "pdf"],
            dialog_title="Select multiple images or PDF files"
        )

    # Add the controls to the page
    page.add(
        ft.Row(
            [
                ft.ElevatedButton(
                    text="Select Files",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=open_file_picker,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [
                result_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
```

## Problems

This app will not run on macOS as a desktop app because Flet's FilePicker will not open due to missing/default macOS entitlements, the file picker window simply refuses to appear.  

The app will run in a browser if you specify `flet run --web`.  

AI typically generates references to `.icons` and `.colors`, but both were recently converted to begin with uppercase letters, so `.Icons` and `.Colors` are needed.  

