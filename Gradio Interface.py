import gradio as gr
from PIL import Image
import numpy as np
from greyscale.rgb_to_greyscale import rgb_to_greyscale
from greyscale.quantize_and_dither import quantize_and_dither
from greyscale.key_gen_greyscale import key_gen_greyscale
from greyscale.encrypt_4levels import encrypt_4levels
from binary.rgb_to_binary import rgb_to_binary
from binary.key_gen_binary import key_gen_binary
from binary.encrypt_binary import encrypt_binary
from tools.VC_conversion import VC_conversion_diagonal
from tools.VC_conversion import VC_conversion_vertical
from tools.VC_conversion import VC_conversion_horizontal
from tools.VC_conversion import VC_conversion_greyscale_4levels

def encrypt(image, mode, key_option, key_image=None):
    if image is None:
        return None, None, "❌ Please provide an input image."
    
    #if mode == "Binary" and filling is None:
    #    return None, None, "❌ Please choose a filling option for binary mode."

    if key_option == "Provide Key":
        if key_image is None:
            return None, None, "❌ Please provide a key image."
        if image.size != key_image.size:
            return None, None, "❌ The input and key images must be the same size."
    
    img = np.array(image)

    if mode == "Greyscale":
        grey_image = rgb_to_greyscale(img)
        quantized_image = quantize_and_dither(grey_image)

        if key_option == "Generate Random":
            key = key_gen_greyscale(quantized_image)
        else:
            key = np.array(key_image)

        cypher = encrypt_4levels(quantized_image, key)

        cypher = Image.fromarray(cypher)
        key = Image.fromarray(key)

        return cypher, key, "✅ Encryption successful!"
    else:
        if key_option == "Generate Random":
            key = key = key_gen_binary(img)
        else:
            key = np.array(key_image)
        
        cypher = encrypt_binary(img, key)

        return cypher, key, "✅ Encryption successful!"
    
def vc_convert(mode, filling, img):
    if img is None:
        return None, "❌ Please provide an input image."

    img = np.array(img)

    if mode == "Greyscale":
        vc_img = VC_conversion_greyscale_4levels(img)
        vc_img = Image.fromarray(vc_img)
        return vc_img, "✅ VC Conversion successful!"
    else:
        if filling == "Horizontal":
            vc_img = VC_conversion_horizontal(img)
        elif filling == "Vertical":
            vc_img = VC_conversion_vertical(img)
        elif filling == "Diagonal":
            vc_img = VC_conversion_diagonal(img)

        vc_img = Image.fromarray(vc_img)
        return vc_img, "✅ VC Conversion successful!"

bin_hor_img = "images/bin_hor_scheme.png"
bin_ver_img = "images/bin_ver_scheme.png"
bin_diag_img = "images/bin_diag_scheme.png"
grey_img = "images/greyscale_scheme.png"

def update_preview(mode, filling):
    if mode == "Binary":
        if filling == "Horizontal":
            return bin_hor_img
        elif filling == "Vertical":
            return bin_ver_img
        elif filling == "Diagonal":
            return bin_diag_img
        else:
            return None
    elif mode == "Greyscale":
        return grey_img
    else:
        return None

# ------------------------------
# BUILD INTERFACE
# ------------------------------
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>🔐 Visual Cryptography Tool</h1>")

    with gr.Tab("Encrypt"):

        mode = gr.Radio(
            ["Binary", "Greyscale"], 
            value="Binary",
            label="Select the type of quantization you wish to apply to your input image",
            info="Binary: 1-bit images (optimal for texts or black and white logos). Greyscale: 4-level greyscale images (optimal for detailed images)."
        )

        # --- Input image ---
        input_img = gr.Image(type="pil", label="Upload Input Image")

        # --- Key selection ---
        key_option = gr.Radio(
            ["Provide Key", "Generate Random"], 
            label="Key Option"
        )
        key_img = gr.Image(type="pil", label="Upload Key Image (same size as input)", visible=False)

        def toggle_key(opt):
            return gr.update(visible=(opt == "Provide Key"))

        key_option.change(toggle_key, key_option, key_img)

        # --- Run button + Output ---
        run_btn = gr.Button("🔒 Encrypt")

        cypher = gr.Image(type="pil", format="png", label="Cypher / Share 1")
        key = gr.Image(type="pil", format="png", label="Key / Share 2")
        status = gr.Label(label="Status")

        run_btn.click(
            encrypt,
            inputs=[input_img, mode, key_option, key_img],
            outputs=[cypher, key, status]
        )

    with gr.Tab("VC Conversion"):
        gr.Markdown("This tool allows the conversion of shares generated with the encryption" \
                    "algorithm into transparent overlaiable images, as shown in the scheme below.")

        with gr.Row():
            with gr.Column():
                mode = gr.Radio(
                    ["Binary", "Greyscale"], 
                    value="Binary",
                    label="Choose Image Type",
                    info="Binary: 1-bit images (black & white). Greyscale: 4-level greyscale images."
                )

                filling = gr.Radio(
                    ["Horizontal", "Vertical", "Diagonal"], 
                    value="Diagonal",
                    label="Choose Filling (Binary Only)", 
                    visible=True
                )

                # Show filling options only if "Binary" is chosen
                def toggle_filling(m):
                    return gr.update(visible=(m == "Binary"))

                mode.change(toggle_filling, mode, filling)

            with gr.Column():
                info_img = gr.Image(type="filepath",
                                    value=bin_diag_img,
                                    show_download_button=False,
                                    show_fullscreen_button=False,
                                    container=False)
        
        mode.change(update_preview, [mode, filling], info_img)
        filling.change(update_preview, [mode, filling], info_img)

        input_img = gr.Image(type="pil", label="Upload Share Image")
        vc_conv_btn = gr.Button("🌀 Apply VC Conversion")
        output_img = gr.Image(type="pil", format="png", label="Overlaiable Image")

        vc_conv_btn.click(
            vc_convert,
            inputs=[mode, filling, input_img],
            outputs=[output_img, status]
        )


demo.launch(share=False)
