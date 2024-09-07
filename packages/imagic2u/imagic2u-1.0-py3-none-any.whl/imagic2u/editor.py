from PIL import Image, ImageDraw, ImageFont

def redimensionar_imagem(caminho_entrada, caminho_saida, largura, altura):
    """
    Redimensiona uma imagem para as dimensões especificadas.
    
    Parâmetros:
    - caminho_entrada: Caminho da imagem original.
    - caminho_saida: Caminho para salvar a imagem redimensionada.
    - largura: Nova largura.
    - altura: Nova altura.
    """
    with Image.open(caminho_entrada) as img:
        img_resized = img.resize((largura, altura))
        img_resized.save(caminho_saida)
        print(f"Imagem salva em {caminho_saida}.")

def converter_para_pb(caminho_entrada, caminho_saida):
    """
    Converte uma imagem colorida para preto e branco.
    
    Parâmetros:
    - caminho_entrada: Caminho da imagem original.
    - caminho_saida: Caminho para salvar a imagem em preto e branco.
    """
    with Image.open(caminho_entrada) as img:
        img_bw = img.convert("L")
        img_bw.save(caminho_saida)
        print(f"Imagem em preto e branco salva em {caminho_saida}.")

def adicionar_texto(caminho_entrada, caminho_saida, texto, posicao, cor=(255, 255, 255), tamanho_fonte=40):
    """
    Adiciona texto a uma imagem em uma posição específica.
    
    Parâmetros:
    - caminho_entrada: Caminho da imagem original.
    - caminho_saida: Caminho para salvar a imagem com texto.
    - texto: Texto a ser adicionado.
    - posicao: Uma tupla (x, y) indicando a posição do texto.
    - cor: Cor do texto (padrão: branco).
    - tamanho_fonte: Tamanho da fonte do texto.
    """
    with Image.open(caminho_entrada) as img:
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", tamanho_fonte)
        except IOError:
            font = ImageFont.load_default()

        draw.text(posicao, texto, font=font, fill=cor)
        img.save(caminho_saida)
        print(f"Texto adicionado e imagem salva em {caminho_saida}.")
