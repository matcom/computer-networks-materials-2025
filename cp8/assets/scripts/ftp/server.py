import socket
import threading

class ThreadedTCPServer:
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def handle_client(self, conn, addr):
        print(f"[+] Conexión establecida con {addr}")
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                print(f"[{addr}] Mensaje recibido: {message}")
                
                # Procesar comando (simulación FTP)
                response = self.process_command(message)
                conn.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error con {addr}: {e}")
        finally:
            conn.close()
            print(f"[-] Conexión cerrada con {addr}")
    
    def process_command(self, command):
        """Simula comandos FTP básicos"""
        command = command.strip().upper()
        if command == "LIST":
            return "archivo1.txt\narchivo2.txt\ndirectorio/"
        elif command.startswith("GET "):
            filename = command[4:]
            return f"Enviando archivo: {filename}"
        elif command == "PWD":
            return "/home/usuario/"
        elif command == "QUIT":
            return "Adiós!"
        else:
            return f"Comando no reconocido: {command}"
    
    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = self.sock.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\nCerrando servidor...")
        finally:
            self.sock.close()

if __name__ == "__main__":
    server = ThreadedTCPServer()
    server.start()