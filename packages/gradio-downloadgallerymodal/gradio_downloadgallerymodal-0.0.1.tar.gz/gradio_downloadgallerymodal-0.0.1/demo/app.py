import gradio as gr
from gradio_downloadgallerymodal import DownloadGalleryModal

example = DownloadGalleryModal().example_value()
payload = DownloadGalleryModal().example_payload()

with gr.Blocks() as demo:
    with gr.Row():
        # DownloadGallery(label="Blank"),  # blank component
        gallery = DownloadGalleryModal(value=example, interactive=False)  #

    def on_toggle_favorite(value, evt: gr.EventData):
        favorite = evt._data["favorite"]
        if favorite:
            # add here logic to save the image to favorites
            print(f"Add {evt._data['image']['orig_name']} to favorites")
        else:
            # add here logic to remove the image from favorites
            print(f"Remove {evt._data['image']['orig_name']} from favorites")

    gallery.toggle_favorite(on_toggle_favorite, gallery, None)


if __name__ == "__main__":
    demo.launch()
