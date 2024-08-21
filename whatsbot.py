import flet as ft
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time

# Função para iniciar o bot
def start_bot(mensagem, lista_contatos):
    service = Service(ChromeDriverManager().install())
    nav = webdriver.Chrome(service=service)
    nav.get('https://web.whatsapp.com')
    time.sleep(40)

    # Enviar a mensagem para meu número e depois encaminhar
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span').click()
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(lista_contatos[0])
    nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
    time.sleep(1)

    pyperclip.copy(mensagem)
    nav.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.CONTROL + 'v')
    time.sleep(2)
    nav.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p').send_keys(Keys.ENTER)
    time.sleep(3)

    qtde_contatos = len(lista_contatos)
    if qtde_contatos % 5 == 0:
        qtde_blocos = qtde_contatos / 5
    else:
        qtde_blocos = int(qtde_contatos / 5) + 1

    for i in range(int(qtde_blocos)):  # Converte qtde_blocos para int
        i_inicial = i * 5 
        i_final = (i + 1) * 5 
        lista_enviar = lista_contatos[i_inicial:i_final]

        lista_elementos = nav.find_elements('class name', '_amk6')
        for item in lista_elementos:
            mensagem = mensagem.replace("\n", "")
            texto = item.text.replace("\n", "")
            if mensagem in texto:
                elemento = item

        ActionChains(nav).move_to_element(elemento).perform()
        elemento.find_element('class name', '_ahkm').click()
        time.sleep(1)
        nav.find_element('xpath', '//*[@id="app"]/div/span[5]/div/ul/div/li[4]/div').click()
        time.sleep(0.5)
        nav.find_element('xpath', '//*[@id="main"]/span[2]/div/button[4]/span').click()
        time.sleep(1)

        for nome in lista_enviar:
            nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(nome)
            time.sleep(1)
            nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
            time.sleep(1.5)
            nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div[1]/p').send_keys(Keys.BACKSPACE)
            time.sleep(1)
        nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div').click()
        time.sleep(3)

# Função para o botão de envio
def enviar_mensagem(e):
    mensagem = campo_mensagem.value
    lista_contatos = [contato.strip() for contato in campo_contatos.value.split(",")]
    start_bot(mensagem, lista_contatos)

# Criação da interface com Flet
def main(page: ft.Page):
    global campo_mensagem, campo_contatos

    page.title = "WhatsApp Bot"

    campo_mensagem = ft.TextField(label="Mensagem", width=400, height=100, multiline=True)
    campo_contatos = ft.TextField(label="Lista de Contatos (separados por vírgula)", width=400, height=100, multiline=True)
    
    botao_enviar = ft.ElevatedButton(text="Enviar", on_click=enviar_mensagem)

    # Adicionar a logo arredondada
    imagem = ft.Image(
        src="/Users/nanda/OneDrive/Área de Trabalho/autoPy/BotWhatsApp-py/Penguin_codeIcon.png",
        width=100,
        height=100,
        fit=ft.ImageFit.COVER,
        border_radius=50,  # Torna a imagem arredondada
    )

       # Container para os campos de texto e botão
    conteudo_principal = ft.Column(
        [
            campo_mensagem,
            ft.Container(height=5),
            campo_contatos,
            ft.Container(height=5),
            botao_enviar,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Container para centralizar a área principal
    container_principal = ft.Container(
        content=ft.Column(
            [
                imagem,  # Adiciona a imagem acima dos campos de texto
                ft.Container(height=25),  # Espaçamento de 25 pixels
                conteudo_principal
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        alignment=ft.alignment.center,
        expand=True,
        height=500,  # Ajuste a altura do container principal conforme necessário
    )

    # Rodapé com texto centralizado
    rodape = ft.Container(
        content=ft.Text("Todos os Direitos Reservados | Penguin Code", theme_style=ft.TextThemeStyle.BODY_MEDIUM),
        alignment=ft.alignment.center,
    )

    # Estrutura principal da página
    page.add(
        container_principal,
        rodape,
    )

ft.app(target=main)