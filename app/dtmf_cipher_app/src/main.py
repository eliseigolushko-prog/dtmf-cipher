import flet as ft
from flet import Colors, Icons, Button
import dtmf_core
import os
import pathlib

def get_dl_dir():
    return str(pathlib.Path.home() / "Downloads")

async def main(page: ft.Page):
    page.title = "DTMF Cipher Studio"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 950
    page.window_height = 800
    page.window_resizable = False

    app_data = {"generated_wav_bytes": b"", "decrypted_text": ""}

    # --- UI COMPONENTS ---
    enc_in = ft.TextField(label="Text to Encrypt", multiline=True, min_lines=4, hint_text="Type text here...")
    enc_file_info = ft.Text(value="No file loaded", color=Colors.BLUE_200)
    enc_name = ft.TextField(label="Output WAV Name", value="encoded_dtmf.wav")
    enc_out = ft.Text(value="DTMF Code: ", color=Colors.BLUE_200, weight=ft.FontWeight.BOLD)
    enc_status = ft.Text(color=Colors.GREEN_400)

    dec_file_info = ft.Text(value="No file selected", color=Colors.BLUE_200)
    dec_out = ft.Text(value="Detected DTMF: ", color=Colors.BLUE_200, weight=ft.FontWeight.BOLD)
    dec_txt = ft.TextField(label="Decrypted Text", multiline=True, min_lines=5, read_only=True)
    dec_name = ft.TextField(label="Export TXT Name", value="decoded_text.txt")
    dec_status = ft.Text(color=Colors.GREEN_400)

    async def handle_pick_txt(e):
        enc_status.value = "Opening file browser..."
        page.update()

        result = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )

        if result and len(result) > 0:
            selected_file = result[0]
            enc_file_info.value = f"Selected: {selected_file.name} ({selected_file.size} bytes)"
            try:
                enc_in.value = selected_file.bytes.decode("utf-8", errors="replace")
                enc_status.value = "Text file loaded into memory successfully!"
            except Exception as ex:
                enc_status.value = f"Load error: {ex}"
        else:
            enc_status.value = "Selection cancelled."
        page.update()

    async def handle_pick_wav(e):
        dec_status.value = "Opening file browser..."
        page.update()

        # pick_files() возвращает list[FilePickerFile] напрямую
        result = await ft.FilePicker().pick_files(
            allow_multiple=False,
            with_data=True,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["wav"]
        )

        if result and len(result) > 0:
            selected_file = result[0]
            dec_file_info.value = f"Selected: {selected_file.name} ({selected_file.size} bytes)"
            dec_status.value = "Analyzing audio wave from memory..."
            page.update()
            try:
                s, t = dtmf_core.decode_wav_bytes_to_text(selected_file.bytes)
                dec_out.value = f"Detected: {s}"
                dec_txt.value = t
                app_data["decrypted_text"] = t
                dec_status.value = "Successfully decoded from memory!"
            except Exception as ex:
                dec_status.value = f"Decode error: {ex}"
        else:
            dec_status.value = "Selection cancelled."
        page.update()

    async def handle_generate_click(e):
        if not enc_in.value.strip():
            enc_status.value = "Error: Input text is empty!"
            page.update()
            return
        try:
            dtmf_str = dtmf_core.text_to_dtmf_string(enc_in.value)
            app_data["generated_wav_bytes"] = dtmf_core.generate_wav_bytes(enc_in.value)

            enc_out.value = f"DTMF Code: {dtmf_str}"
            enc_status.value = "Audio generated in memory! Ready to save."
            save_wav_button.disabled = False
        except Exception as ex:
            enc_status.value = f"Generation error: {ex}"
        page.update()

    async def handle_save_wav(e):
        name = enc_name.value.strip() or "encoded_dtmf.wav"
        if not name.lower().endswith(".wav"): name += ".wav"

        await ft.FilePicker().save_file(
            file_name=name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["wav"],
            src_bytes=app_data["generated_wav_bytes"]
        )
        enc_status.value = f"File '{name}' is ready. Save dialog triggered."
        page.update()

    async def handle_export_txt(e):
        if not dec_txt.value:
            dec_status.value = "Error: Nothing to export!"
            page.update()
            return
        name = dec_name.value.strip() or "decoded_text.txt"
        if not name.lower().endswith(".txt"): name += ".txt"

        await ft.FilePicker().save_file(
            file_name=name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"],
            src_bytes=dec_txt.value.encode("utf-8")
        )
        dec_status.value = f"File '{name}' is ready. Save dialog triggered."
        page.update()

    # --- UI LAYOUT ---
    save_wav_button = Button(icon=Icons.DOWNLOAD, content=ft.Text("Save/Download WAV"), on_click=handle_save_wav, disabled=True)

    page.add(ft.Container(content=ft.Column([
        ft.Text("DTMF Cipher Studio (Pure Memory Mode)", size=24, weight=ft.FontWeight.BOLD), ft.Divider(),
        ft.Row([

            ft.Card(content=ft.Container(content=ft.Column([
                ft.Text("Encoder Module", size=20, weight=ft.FontWeight.BOLD, color=Colors.BLUE_400),
                Button(icon=Icons.FOLDER_OPEN, content=ft.Text("Load TXT File"), on_click=handle_pick_txt),
                enc_file_info, ft.Divider(),
                enc_in, enc_name,
                Button(icon=Icons.AUDIO_FILE, content=ft.Text("1. Generate WAV in Memory"), on_click=handle_generate_click, bgcolor=Colors.BLUE_700),
                save_wav_button,
                enc_out, enc_status
            ], spacing=12, scroll=ft.ScrollMode.AUTO), padding=15), expand=True),

            ft.Card(content=ft.Container(content=ft.Column([
                ft.Text("Decoder Module", size=20, weight=ft.FontWeight.BOLD, color=Colors.GREEN_400),
                Button(icon=Icons.AUDIO_FILE, content=ft.Text("Select & Decode WAV"), on_click=handle_pick_wav),
                dec_file_info, ft.Divider(),
                dec_status, dec_out, dec_txt, dec_name,
                Button(icon=Icons.SAVE, content=ft.Text("Export Text to File"), on_click=handle_export_txt, bgcolor=Colors.GREEN_700)
            ], spacing=12, scroll=ft.ScrollMode.AUTO), padding=15), expand=True)
        ], expand=True)
    ]), padding=10, expand=True))

if __name__ == "__main__":
    ft.run(main)
