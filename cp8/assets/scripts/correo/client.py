import socket
import time

class SMTPClient:
    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
    
    def send_email(self, from_addr, to_addrs, subject, body):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((self.host, self.port))
            
            # Leer banner
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
            # HELO
            sock.sendall(b"HELO localhost\r\n")
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
            # FROM
            sock.sendall(f"MAIL FROM: <{from_addr}>\r\n".encode())
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
            # TO
            for to_addr in to_addrs:
                sock.sendall(f"RCPT TO: <{to_addr}>\r\n".encode())
                response = sock.recv(1024)
                print(f"Servidor: {response.decode()}")
            
            # DATA
            sock.sendall(b"DATA\r\n")
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
            # Email content
            email_content = f"Subject: {subject}\r\n\r\n{body}\r\n.\r\n"
            sock.sendall(email_content.encode())
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
            # QUIT
            sock.sendall(b"QUIT\r\n")
            response = sock.recv(1024)
            print(f"Servidor: {response.decode()}")
            
        except Exception as e:
            print(f"Error: {e}")
        finally:
            sock.close()

if __name__ == "__main__":
    client = SMTPClient()
    
    # Enviar email de prueba
    client.send_email(
        from_addr="remitente@ejemplo.com",
        to_addrs=["destinatario@ejemplo.com"],
        subject="Prueba de correo",
        body="Este es un mensaje de prueba desde nuestro cliente SMTP."
    )