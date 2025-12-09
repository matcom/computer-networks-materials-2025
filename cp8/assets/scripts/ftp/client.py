import socket

class TCPClient:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            print("Conectado al servidor. Escribe 'QUIT' para salir.")
            
            while True:
                message = input("Comando (LIST, GET archivo, PWD, QUIT): ")
                sock.sendall(message.encode('utf-8'))
                
                if message.upper() == 'QUIT':
                    break
                
                response = sock.recv(1024).decode('utf-8')
                print(f"Servidor: {response}")
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    client = TCPClient()
    client.start()