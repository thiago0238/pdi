import os
from matplotlib import pyplot as plt
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "tif", "bmp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def gerar_histograma(img_array, filename, prefixo):
    """Gera o histograma da imagem e salva."""
    plt.figure()
    plt.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)
    plt.title(f"Histograma {prefixo}")
    plt.xlabel("Intensidade")
    plt.ylabel("Frequência")

    hist_path = os.path.join(app.config["PROCESSED_FOLDER"], f"histograma_{prefixo}_{filename}.png")
    plt.savefig(hist_path)
    plt.close()
    return hist_path

def equalizar_histograma(img_array):
    """Equaliza o histograma apenas no canal de luminância (Y)."""
    img_yuv = cv2.cvtColor(img_array, cv2.COLOR_RGB2YUV)
    img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
    return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)

def aplicar_filtro_media(img_array, kernel_size=3):
    altura, largura, canais = img_array.shape
    pad = kernel_size // 2
    img_filtrada = np.zeros_like(img_array)
    
    for c in range(canais):
        for i in range(pad, altura - pad):
            for j in range(pad, largura - pad):
                soma = 0
                for ki in range(-pad, pad + 1):
                    for kj in range(-pad, pad + 1):
                        soma += img_array[i + ki, j + kj, c]
                img_filtrada[i, j, c] = soma // (kernel_size * kernel_size)
    
    return img_filtrada.astype(np.uint8)

def aplicar_filtro_mediana(img_array, kernel_size=3):
    altura, largura, canais = img_array.shape
    pad = kernel_size // 2
    img_filtrada = np.zeros_like(img_array)
    
    for c in range(canais):
        for i in range(pad, altura - pad):
            for j in range(pad, largura - pad):
                vizinhanca = img_array[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                img_filtrada[i, j, c] = np.median(vizinhanca)
    
    return img_filtrada.astype(np.uint8)

def aplicar_filtro_maximo(img_array, kernel_size=3):
    altura, largura, canais = img_array.shape
    pad = kernel_size // 2
    img_filtrada = np.zeros_like(img_array)
    
    for c in range(canais):
        for i in range(pad, altura - pad):
            for j in range(pad, largura - pad):
                vizinhanca = img_array[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                img_filtrada[i, j, c] = np.max(vizinhanca)
    
    return img_filtrada.astype(np.uint8)

def aplicar_filtro_minimo(img_array, kernel_size=3):
    altura, largura, canais = img_array.shape
    pad = kernel_size // 2
    img_filtrada = np.zeros_like(img_array)
    
    for c in range(canais):
        for i in range(pad, altura - pad):
            for j in range(pad, largura - pad):
                vizinhanca = img_array[i - pad:i + pad + 1, j - pad:j + pad + 1, c]
                img_filtrada[i, j, c] = np.min(vizinhanca)
    
    return img_filtrada.astype(np.uint8)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files or "filter" not in request.form:
            return "Arquivo ou filtro não enviado."

        file = request.files["file"]
        filter_type = request.form["filter"]

        if file.filename == "":
            return "Nenhum arquivo selecionado."

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            img = Image.open(filepath).convert("RGB")
            img_array = np.array(img)

            if filter_type == "media":
                img_filtrada = aplicar_filtro_media(img_array)
            elif filter_type == "mediana":
                img_filtrada = aplicar_filtro_mediana(img_array)
            elif filter_type == "maximo":
                img_filtrada = aplicar_filtro_maximo(img_array)
            elif filter_type == "minimo":
                img_filtrada = aplicar_filtro_minimo(img_array)
            elif filter_type == "histograma":
                # Gerar histograma da imagem original
                hist_original_path = gerar_histograma(img_array, filename, "original")

                # Equalizar histograma
                img_equalizada = equalizar_histograma(img_array)
                
                # Gerar histograma da imagem equalizada
                hist_equalizado_path = gerar_histograma(img_equalizada, filename, "equalizado")

                # Salvar imagem equalizada
                processed_path = os.path.join(app.config["PROCESSED_FOLDER"], filename)
                Image.fromarray(img_equalizada).save(processed_path)

                return render_template(
                    "index.html",
                    original_image=filename,
                    filtered_image=filename,
                    histograma_original=os.path.basename(hist_original_path),
                    histograma_equalizado=os.path.basename(hist_equalizado_path)
                )
            else:
                return "Filtro inválido."

            img_filtrada = Image.fromarray(img_filtrada)
            processed_path = os.path.join(app.config["PROCESSED_FOLDER"], filename)
            img_filtrada.save(processed_path)

            return render_template(
                "index.html",
                original_image=filename,
                filtered_image=filename,
            )
    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/processed/<filename>")
def processed_file(filename):
    return send_from_directory(app.config["PROCESSED_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)