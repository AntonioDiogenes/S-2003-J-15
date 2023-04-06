import socket
from threading import Thread

host = 'localhost'
port = 50000

def main():
    cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)# socket cliente ipv4 tcp
    try:
        cliente.connect((host,port))#conecta no socket do servidor      
    except:
        return print('nao foi possivel conectar ao servidor')
    
    username = input("usuario> ") #pega o nome do usuario
    cliente.send(username.encode('utf-8'))
    print('conectado') 
    
    Thread(target=recv_msg, args=[cliente]).start() #inicia thread pra RECEBER mensagem
    Thread(target=env_msg, args=[cliente,username]).start() #inicia thread pra ENVIAR mensagem

def env_msg(cliente,username): #recebe o socket do cliente e seu nome
    while True:
        try:
            msg = input() #recebe uma mensagem
            cliente.send(f'<{username}> {msg}'.encode('utf-8'))#envia a mensagem pro servidor
        except:
            return

def recv_msg(cliente): #recebe o socket do cliente
    while True:
        try:
            msg = cliente.recv(1024).decode('utf-8') #recebe a mensagem vinda do servidor
            print(msg,"\n")
        except:
            print("nao possivel permanecer conectado")
            print("precione <enter> pra continuar . . .")
            cliente.close() #fecha a conexao com o servidor
            break
        
main()  