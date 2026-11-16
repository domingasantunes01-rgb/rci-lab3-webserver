# -*- coding: utf-8 -*-
"""
Lab3 - Servidor e Cliente Web

Docente: João Costa (joaojdacosta@gmail.com)
Outubro, 2024.
"""

from socket import *  # importa o módulo socket
import sys # Por forma a terminar o programa

# Cria um socket do servidor TCP
#(AF_INET é utilizado para o protocolo IPv4)
#(SOCK_STREAM é utilizado para o TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Atribui o número de porta
serverPort = 6789

# TODO #1:  Vincular o socket ao endereço e porta do servidor
# Preencha o início
# Permite reutilizar a porta logo após reiniciar o servidor
# (evita o erro "Address already in use" por causa do TIME_WAIT)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
# '' = todas as interfaces da máquina (incluindo 192.168.56.21)
serverSocket.bind(('', serverPort))
# Preencha o fim

# TODO #2: Escutar, no máximo, 1 conexão por vez
# Preencha o início
serverSocket.listen(1)
# Preencha o fim

# O servidor deve estar Up, em execução e a escuta
# por novas conexões

while True:
	print('O servidor está pronto para receber')

	# TODO #3: Configurar uma nova conexão do cliente
	# Preencha o início
	# accept() bloqueia até um cliente concluir o 3-way handshake e
	# devolve um novo socket dedicado a essa conexão
	connectionSocket, addr = serverSocket.accept()
	print('Conexão recebida de %s:%d' % addr)
	# Preencha o fim

	# Se ocorrer uma excepção durante a execução da cláusula try
	# o resto da cláusula é ignorado
	# Se o tipo de exceção corresponder à palavra após except
	# a cláusula except é executada
	try:
		# TODO #4: Receber a mensagem de solicitação do cliente
		message = connectionSocket.recv(1024).decode() #Preencha o início 	#Preencha o fim
		print('Pedido: %s' % message.split('\r\n')[0])
		# Extrae o caminho do objecto solicitado da mensagem
		# O caminho é a segunda parte do cabeçalho HTTP,
		# identificado por [1]
		filename = message.split()[1]
		# O caminho extraído da solicitação HTTP inclui
		# um caractere '\', lemos o caminho do
		# segundo caractere
		f = open(filename[1:])
		# Armazena todo o conteúdo do ficheiro solicitado
		# em um buffer temporário
		outputdata = f.read()
		f.close()
		# TODO #5: Enviar a linha de cabeçalho de resposta HTTP
		# para o socket de conexão
		# Preencha o início
		header = ("HTTP/1.1 200 OK\r\n"
		          "Content-Type: text/html; charset=utf-8\r\n"
		          "Connection: close\r\n"
		          "\r\n")
		connectionSocket.send(header.encode())
		# Preencha o fim

		# Envia o conteúdo do ficheiro solicitado
		# para o socket de conexão
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode())
		connectionSocket.send("\r\n".encode())

		# Fecha o socket de conexão do cliente
		connectionSocket.close()
		print('Resposta: 200 OK (%s)' % filename)

	except (IOError, IndexError):
		# IOError: o ficheiro pedido não existe
		# IndexError: pedido vazio/mal formado (ex.: telnet fechado sem GET)
		# TODO #6: Enviar mensagem de resposta HTTP para ficheiro não encontrado
		# Preencha o início
		try:
			connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
			connectionSocket.send(("Content-Type: text/html; charset=utf-8\r\n"
			                       "Connection: close\r\n"
			                       "\r\n").encode())
			connectionSocket.send(("<html><head><title>404 Not Found</title></head>"
			                       "<body><h1>404 Not Found</h1>"
			                       "<p>O ficheiro pedido nao existe neste servidor.</p>"
			                       "</body></html>\r\n").encode())
		except error:
			# O cliente já fechou a conexão: não há a quem responder,
			# mas o servidor continua a correr
			pass
		# Preencha o fim

		# TODO #7: Fechar o socket de conexão do cliente
		# Preencha o início
		connectionSocket.close()
		print('Resposta: 404 Not Found')
		# Preencha o fim

serverSocket.close()
sys.exit()# Encerra o programa após enviar os dados correspondentes.
