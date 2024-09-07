from PIL import Image, ImageFilter, ImageOps

def aplicar_desfoque(caminho_entrada, caminho_saida, intensidade=5):
    """
    Aplica um filtro de desfoque (blur) à imagem.
    
    Parâmetros:
    - caminho_entrada: Caminho da imagem original.
    - caminho_saida: Caminho para salvar a imagem desfocada.
    - intensidade: Intensidade do desfoque (padrão: 5).
    """
    with Image.open(caminho_entrada) as img:
        img_blur = img.filter(ImageFilter.GaussianBlur(intensidade))
        img_blur.save(caminho_saida)
        print(f"Imagem com desfoque salva em {caminho_saida}.")

def inverter_cores(caminho_entrada, caminho_saida):
    """
    Inverte as cores da imagem (efeito negativo).
    
    Parâmetros:
    - caminho_entrada: Caminho da imagem original.
    - caminho_saida: Caminho para salvar a imagem com cores invertidas.
    """
    with Image.open(caminho_entrada) as img:
        img_inverted = ImageOps.invert(img)
        img_inverted.save(caminho_saida)
        print(f"Imagem com cores invertidas salva em {caminho_saida}.")
