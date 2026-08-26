"""
Propósito: Dividir as questões por padrão. Observa-se que ao início de cada questão tem uma faixa de alguma cor, que é o padrão de início de cada questão
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a imagem "colunas_concatenadas_verticalmente.png" do passo 6 para essa pasta do passo 7

OBS2: puxe a pasta "inteiras" do passo 5 para essa pasta do passo 7

OBS3: este código foi originalmente preparado para percorrer cada pixel de cima para baixo, analizando o penúltimo pixel da direita (linha 55), procurando por um padrão visual vertical de 10 pixels RGB 0-255 (64, 193, 243), seguido de 7 pixels RGB 0-255 (179, 230, 250), 4 px RGB 0-255 (64, 193, 243) e 8 px RGB 0-255 (179, 230, 250). Quando encontrava esse padrão, cortava-se 13 pixels acima de começar o padrão (linha 71).

OBS4: tendo isso em mente, use o GIMP para identificar qual é o padrão visual da sua prova (que indica o início de cada questão), quantos pixels acima do padrão visual você precisa cortar, e também qual pixel é melhor percorrer para procurar por essa faixa. SEJA CRÍTICO(A)!

OBS5: em algumas situações, o pixel procurado é a mesma cor de uma imagem ou letra. Nesses casos, você pode pedir para percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel. Isso vai depender do padrão visual da sua prova.

OBS6: além disso, em algumas situações, o padrão visual varia um pixel ou outro. Por isso, é interessante considerar uma margem de erro de 3 pixels para mais e 3 pixels para menos em cada uma das faixas do seu padrão visual.

OBS6: use IA para mudar minimamente o código a fim de cortar sua imagem seguindo o padrão visual vertical da sua prova, qual pixel percorrer, qual cor RGB 0-255 procurar, quantos pixels acima do padrão visual cortar, e se necessário, percorrer uma faixa de determinada altura e largura e determinada cor, e não apenas um pixel.

OBS7: rode esse código para cada imagem que você precisa cortar. Atualize as linhas 138 e 139 para identificar a imagem e atualize o nome da pasta de saída também

OBS8: execute o código, e abra as imagens para conferir se as questões foram divididas corretamente. Se não, ajuste os valores de corte e execute novamente.
"""
"""
Propósito: Dividir as questões por padrão. Observa-se que ao início de cada questão tem uma faixa de alguma cor, que é o padrão de início de cada questão
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a imagem "colunas_concatenadas_verticalmente.png" do passo 6 para essa pasta do passo 7
OBS2: puxe a pasta "inteiras" do passo 5 para essa pasta do passo 7
OBS3 a OBS8: Padrão adaptado para detectar faixa de 64px de altura nos 2 últimos pixels da direita com cor RGB(74, 73, 73) e margem de erro de ±3px, cortando 16px acima.
"""
"""
Propósito: Dividir as questões por padrão visual vertical das faixas laterais.
Autor: Alexandre Nassar de Peder (Atualizado conforme especificações)
Criação: 02/10/2025
Atualização: 03/06/2026
"""

from PIL import Image
import os

def encontrar_faixa_padrao(imagem, cor_alvo, tolerancia=3, altura_faixa=64):
    """
    Encontra posições onde há uma faixa vertical do padrão especificado no penúltimo pixel da direita.
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    posicoes_corte = []
    
    y = 0
    while y <= altura - altura_faixa:
        faixa_encontrada = True
        
        # Percorre a altura da faixa de 64 pixels
        for dy in range(altura_faixa):
            # Penúltimo pixel da direita (largura - 2)
            pixel = pixels[largura - 2, y + dy]
            
            if len(pixel) == 4: # RGBA
                r, g, b, a = pixel
            else: # RGB
                r, g, b = pixel[:3]
            
            # Aplica a margem de erro de ±3 pixels na cor RGB
            if (abs(r - cor_alvo[0]) > tolerancia or
                abs(g - cor_alvo[1]) > tolerancia or
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            # Corta 16 pixels acima do início do padrão visual
            posicao_corte = y - 16
            if posicao_corte < 0:
                posicao_corte = 0
                
            posicoes_corte.append(posicao_corte)
            print(f"Padrão encontrado em y={y}. Posição de corte definida em y={posicao_corte}")
            
            # Pula a extensão da faixa na busca para não detectar o mesmo padrão várias vezes
            y += altura_faixa
        else:
            y += 1
            
    return posicoes_corte

def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo):
    """
    Divide a imagem verticalmente cortando ANTES das faixas, mantendo a faixa na imagem resultante.
    """
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    print(f"Imagem carregada: {largura}x{altura} pixels")
    
    posicoes_corte = encontrar_faixa_padrao(imagem, cor_alvo)
    
    if not posicoes_corte:
        print("Nenhum padrão encontrado na imagem com os parâmetros fornecidos!")
        return
        
    print(f"Encontradas {len(posicoes_corte)} ocorrências do padrão para corte.")
    os.makedirs(pasta_saida, exist_ok=True)
    
    posicao_anterior = 0
    for i, posicao_corte in enumerate(posicoes_corte):
        if posicao_corte <= posicao_anterior:
            continue
            
        # Recorta do ponto anterior até a posição de corte atual
        area_corte = (0, posicao_anterior, largura, posicao_corte)
        secao = imagem.crop(area_corte)
        
        nome_arquivo = f"parte_{i+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")
        
        # CORREÇÃO AQUI: A próxima parte começa EXATAMENTE no ponto de corte,
        # preservando a faixa visual e os 16px acima na nova imagem.
        posicao_anterior = posicao_corte

    # Recorta o trecho final (da última faixa até o fim da imagem)
    if posicao_anterior < altura:
        area_corte = (0, posicao_anterior, largura, altura)
        secao = imagem.crop(area_corte)
        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"
        caminho_completo = os.path.join(pasta_saida, nome_arquivo)
        secao.save(caminho_completo)
        print(f"Salvo: {caminho_completo} ({secao.width}x{secao.height}px)")

if __name__ == "__main__":
    caminho_imagem = "inteiras_concatenadas_verticalmente.png" 
    pasta_saida = "inteiras_divididas"
    
    cor_do_padrao = (189, 188, 188)
    
    print(f"Buscando padrão na cor RGB: {cor_do_padrao}")
    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_do_padrao)
    print("Divisão concluída!")