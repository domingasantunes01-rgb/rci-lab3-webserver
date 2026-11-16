# -*- coding: utf-8 -*-
"""
Lab3 - Cliente Web

Utilização:
    python webclient.py server_host server_port filename

Exemplo:
    python webclient.py 192.168.56.21 6789 /index.html
"""

from socket import *  # importa o módulo socket
import sys # Para ler os argumentos e terminar o programa

# Verifica os argumentos da linha de comando
if len(sys.argv) != 4:
	print('Uso: python webclient.py server_host server_port filename')
	sys.exit(1)

serverHost = sys.argv[1]       # endereço IP ou nome do host do servidor
serverPort = int(sys.argv[2])  # porta onde o servidor está à escuta
filename = sys.argv[3]         # caminho do objecto pedido
if not filename.startswith('/'):
	filename = '/' + filename

# Cria um socket TCP do cliente
#(AF_INET é utilizado para o protocolo IPv4)
#(SOCK_STREAM é utilizado para o TCP)
clientSocket = socket(AF_INET, SOCK_STREAM)

try:
	# Estabelece a conexão TCP com o servidor (3-way handshake)
	clientSocket.connect((serverHost, serverPort))
except error as e:
	print('Não foi possível ligar a %s:%d (%s)' % (serverHost, serverPort, e))
	clientSocket.close()
	sys.exit(1)

# Monta o pedido HTTP GET (linha de pedido + cabeçalhos + linha vazia)
request = ('GET %s HTTP/1.1\r\n'
           'Host: %s:%d\r\n'
           'User-Agent: webclient.py\r\n'
           'Connection: close\r\n'
           '\r\n') % (filename, serverHost, serverPort)

# Envia o pedido HTTP ao servidor
clientSocket.send(request.encode())

# Recebe a resposta até o servidor fechar a conexão (recv devolve vazio)
response = b''
while True:
	data = clientSocket.recv(1024)
	if not data:
		break
	response += data

# Fecha o socket do cliente
clientSocket.close()

# Apresenta a resposta do servidor (cabeçalhos + corpo)
print(response.decode('utf-8', 'replace'))

sys.exit(0) # Encerra o programa
