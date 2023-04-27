import socket
from threading import Thread
from arvore import BinaryTree

broadcast_users = []
names = []
clientes = BinaryTree()
host = 'localhost' 
port = 50000 

def main():                       #ipv4          #tcp
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
    try:
        server.bind((host,port)) 
        server.listen() 
    except:
       return print('nao possivel iniciar servidor')
   
    while True:
        print('aguardando conexao\n')
        cliente, endereco = server.accept() 
        username = cliente.recv(1024).decode('utf-8')
        broadcast_users.append(cliente)
        names.append(username)
        clientes.insert(username,cliente)
        
        cliente.send(b"seja bem vindo \n")
        cliente.send(b"voce esta no modo broadcast \n")
        cliente.send(b"caso queira trocar digite /comando \n")
        
        print('conectado em',endereco)
        Thread(target=recv_msg, args=[cliente]).start()

def recv_msg(cliente):
    while True:
            print("esperando mensagem")
            msg = cliente.recv(1024).decode('utf-8')
            verificar_modo_comando(msg,cliente)
            broadCast(msg,cliente)

def tratar_mensagem(mensagem):
    posicao_barra = mensagem.find("/")
    mensagem_tratada = mensagem[posicao_barra+1:]
    return mensagem_tratada

def verificar_modo_comando(mensagem,cliente):
    if tratar_mensagem(mensagem) == "comando":
        modo_comando(cliente)
    else:
        pass

def modo_comando(cliente):
    
    cliente.send(b"----------Modo Comando Ativado---------- \n")
    cliente.send(b"digite pra escolher o que quer ser feito \n \n")
    cliente.send(b"/privado (entra no privado)\n")
    cliente.send(b"/sair (entra no modo broadcast)\n")
    cliente.send(b"/continuar( continua na conversa e sai do comando) \n")
    
    msg = cliente.recv(1024).decode('utf-8')
    
    if tratar_mensagem(msg) == "privado":
        cliente.send(b"lista de clientes: \n")
        for username in names:
            cliente.send(str(username).encode('utf-8') + b"\n")
        
        
        msg = cliente.recv(1024).decode('utf-8')
        nome_escolhido = tratar_mensagem(msg)
        nome_buscado = clientes.search(nome_escolhido)
        print(nome_buscado)
        if nome_buscado.value1 == nome_escolhido: 
            cliente2 = nome_buscado.value2
            conexao_privada(cliente,cliente2)
        

    if tratar_mensagem(msg) == "sair":
        cliente.send(b"saio do modo comando \n")
        recv_msg(cliente)

def conexao_privada(cliente1,cliente2):
    print("entrou privado")
    while True:
        msg = cliente1.recv(1024)
        if tratar_mensagem(msg.decode('utf-8')) == "sair":
            print("saio privado voltou broad")
            recv_msg(cliente1)
        else:
            cliente2.send(msg)

def broadCast(msg, cliente):
    for i in broadcast_users:
        if i != cliente:
            pos = broadcast_users.index(i)
            nome_pos = names[pos]
            busca_nome_arvore = clientes.search(nome_pos)
            env = busca_nome_arvore.value2
            env.send(msg.encode('utf-8'))
            
main()
