import http.server
import socketserver
from urllib.parse import parse_qs
import os

PORT = 8000  # Porta onde o servidor irá rodar

jogadores = []  # Lista para armazenar os nomes dos jogadores
partidas = []  # Lista para armazenar as partidas
resultados = []  # Lista para armazenar os resultados das partidas
rodada_atual = 1  # Variável para controlar a rodada atual

# Função que gera a página inicial perguntando o número de jogadores
def gerar_html_inicial():
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Configuração Inicial</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
            input, button {{ margin: 10px; padding: 10px; font-size: 16px; }}
        </style>
    </head>
    <body>
        <h1>Configurar Torneio</h1>
        <form action="/inserir_jogadores" method="GET">
            <label for="jogadores">Quantos jogadores? (par)</label><br>
            <input type="number" id="jogadores" name="jogadores" min="2" step="2" required><br>
            <button type="submit">Continuar</button>
        </form>
    </body>
    </html>
    """

# Função que gera o formulário para inserir os nomes dos jogadores
def gerar_formulario_jogadores(num_jogadores):
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Inserir Jogadores</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
            input, button {{ margin: 10px; padding: 10px; font-size: 16px; }}
        </style>
    </head>
    <body>
        <h1>Insira os nomes dos jogadores</h1>
        <form action="/gerar_chaveamento" method="GET">
    """
    # Cria um campo de input para cada jogador
    for i in range(num_jogadores):
        html += f"""
            <label for="jogador{i}">Jogador {i + 1}:</label>
            <input type="text" id="jogador{i}" name="jogador{i}" required><br>
        """

    html += """
            <button type="submit">Gerar Chaveamento</button>
        </form>
    </body>
    </html>
    """
    return html

# Função que gera o HTML com a visualização do chaveamento
def gerar_chaveamento_html(rodada_atual, partidas, vencedores=[]):
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Chaveamento</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
            .bracket-container {{ display: flex; justify-content: center; }}
            .round {{ display: flex; flex-direction: column; align-items: center; margin: 0 20px; }}
            .match {{ margin: 10px 0; padding: 10px; border: 1px solid black; width: 200px; text-align: center; }}
            .arrow {{ font-size: 20px; margin: 5px 0; }}
            form {{ margin-top: 20px; }}
            button {{ padding: 10px 20px; }}
        </style>
    </head>
    <body>
        <h1>Chaveamento - Rodada {rodada_atual}</h1>
        <div class="bracket-container">
    """

    # Exibição das partidas da rodada atual
    html += '<div class="round">'
    html += f"<h2>Rodada {rodada_atual}</h2>"
    html += '<form action="/atualizar_chaveamento" method="GET">'

    # Cria a lista de partidas com os botões para escolher os vencedores
    for i, (jogador1, jogador2) in enumerate(partidas):
        html += f"""
        <div class="match">
            {jogador1} vs {jogador2}<br>
            <input type="radio" id="jogador1_{i}" name="vencedor{i}" value="{jogador1}" required>
            <label for="jogador1_{i}">{jogador1}</label><br>
            <input type="radio" id="jogador2_{i}" name="vencedor{i}" value="{jogador2}" required>
            <label for="jogador2_{i}">{jogador2}</label>
        </div>
        <div class="arrow">⟶</div>
        """
    html += '<button type="submit">Avançar para a próxima rodada</button></form>'
    html += "</div></div></body></html>"

    return html

# Classe que manipula as requisições HTTP e define as rotas
class ChaveamentoHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global jogadores, partidas, resultados, rodada_atual

        if self.path == "/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(gerar_html_inicial().encode())  # Página inicial

        elif self.path.startswith("/inserir_jogadores"):
            query = parse_qs(self.path.split("?")[1])  # Obtém o número de jogadores da URL
            num_jogadores = int(query.get("jogadores")[0])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(gerar_formulario_jogadores(num_jogadores).encode())  # Formulário para inserir os jogadores

        elif self.path.startswith("/gerar_chaveamento"):
            query = parse_qs(self.path.split("?")[1])  # Obtém os nomes dos jogadores da URL
            jogadores = [query[f"jogador{i}"][0] for i in range(len(query))]
            partidas = [(jogadores[i], jogadores[i + 1]) for i in range(0, len(jogadores), 2)]  # Cria as partidas
            self.send_response(200)
            self.end_headers()
            self.wfile.write(gerar_chaveamento_html(rodada_atual, partidas).encode())  # Exibe o chaveamento

        elif self.path.startswith("/atualizar_chaveamento"):
            query = parse_qs(self.path.split("?")[1])  # Obtém os vencedores das partidas
            vencedores = [query[f"vencedor{i}"][0] for i in range(len(partidas))]
            partidas = [(vencedores[i], vencedores[i + 1]) for i in range(0, len(vencedores), 2)]  # Atualiza as partidas com os vencedores
            rodada_atual += 1  # Avança para a próxima rodada
            self.send_response(200)
            self.end_headers()
            self.wfile.write(gerar_chaveamento_html(rodada_atual, partidas).encode())  # Exibe o novo chaveamento

# Configuração do servidor HTTP
with socketserver.TCPServer(("", PORT), ChaveamentoHandler) as httpd:
    print(f"Servidor rodando em: http://localhost:{PORT}")  # Exibe a URL onde o servidor está rodando
    print("Pressione Ctrl+C para encerrar o servidor.")
    httpd.serve_forever()  # Inicia o servidor
