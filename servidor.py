import socket
from threading import Thread
from arvore import BinaryTree

broadcast_users = []
names = []
clientes = BinaryTree()
host = 'localhost' #ip 
port = 50000 #porta 

def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # socket do servidor ipv4 tcp
    try:
        server.bind((host,port)) #abre conexao utilizando o ip e a porta informada
        server.listen() # modo de escuta #metodo blocnante
        
    except:
       return print('nao possivel iniciar servidor')
   
    while True:
        print('aguardando conexao\n')
        cliente, endereco = server.accept() #aceita conexao 
        username = cliente.recv(1024).decode('utf-8') # recebe o nome do usuario que se conectou
        broadcast_users.append(cliente)
        names.append(username)
        clientes.insert(username,cliente) #adiciona o nome do usuario no array
        cliente.send(b"seja bem vindo \n")
        cliente.send(b"voce esta no modo broadcast \n")
        cliente.send(b"caso queira trocar digite /comando \n")
        print('conectado em',endereco)#imprime endereço do cliente
        Thread(target=recv_msg, args=[cliente]).start()# inicia a thread pra RECEBER as mesagens vinda do cliente

def recv_msg(cliente):
    while True:
            print("esperando mensagem")
            msg = cliente.recv(1024).decode('utf-8') #recebe a mensagem do cliente
            print("mensagem recebida: " + msg)
            verificar_modo_comando(msg,cliente) # verifica se o usuaria chamou o comando
            broadCast(msg,cliente) #envia mensagem para todos os outros cliente menos pra quem enviou 
        
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
    print("entrou modo comando")
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
        
        cliente.send(b"escolha um usuario pra conversar e digite / + nome \n")
        
        msg = cliente.recv(1024).decode('utf-8') #recebe o nome escolhido com /
        nome_escolhido = tratar_mensagem(msg) #nome escolhido sem a /

        nome_buscado = clientes.search(nome_escolhido) #busca o nome escolhido na arvore

        if nome_buscado.value1 == nome_escolhido: #se o nome escolhido for igual ao nome buscado inicia conexao privada
             #endereço do nome escolhido
            cliente2 = nome_buscado.value2
            # chama func passando o endereço do usuario e de quem ele quer entrar no privado
            conexao_privada(cliente,cliente2)

    if tratar_mensagem(msg) == "continuar":
        cliente.send(b"saio do modo comando")
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