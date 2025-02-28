import os
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "tiff"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = PROCESSED_FOLDER

# Garante que as pastas existem
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Função para verificar se o arquivo é permitido
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

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

    return img_filtrada.astype(np.uint8)  # Garante valores no intervalo 0-255


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            print("Nenhum arquivo enviado.")
            return "Nenhum arquivo enviado."

        file = request.files["file"]
        
        if file.filename == "":
            print("Nenhum arquivo selecionado.")
            return "Nenhum arquivo selecionado."

        if file and allowed_file(file.filename):
            filename = file.filename
            print(f"Arquivo recebido: {filename}")
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Abrindo a imagem e convertendo para RGB
            img = Image.open(filepath).convert("RGB")
            img_array = np.array(img)

            # Aplicar o filtro de média
            img_filtrada = aplicar_filtro_media(img_array)

            # Salvar imagem processada
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
