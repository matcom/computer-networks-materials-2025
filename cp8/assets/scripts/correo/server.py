import socket
import threading
import json
import os
from datetime import datetime

class SimpleSMTPServer:
    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
        self.mailbox = {}
        self.data_dir = "emails"
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def handle_smtp_session(self, conn, addr):
        print(f"[SMTP] Nueva conexión de {addr}")
        current_email = {
            'from': '',
            'to': [],
            'subject': '',
            'body': '',
            'date': ''
        }
        
        try:
            conn.sendall(b"220 Servidor SMTP Local\r\n")
            state = 'WAITING_HELO'
            
            while True:
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break
                    
                print(f"[SMTP] Comando: {data}")
                
                if state == 'WAITING_HELO' and data.upper().startswith('HELO'):
                    conn.sendall(b"250 Hello\r\n")
                    state = 'READY'
                    
                elif state == 'READY' and data.upper().startswith('MAIL FROM:'):
                    current_email['from'] = data[10:].strip('<>')
                    conn.sendall(b"250 OK\r\n")
                    
                elif state == 'READY' and data.upper().startswith('RCPT TO:'):
                    current_email['to'].append(data[8:].strip('<>'))
                    conn.sendall(b"250 OK\r\n")
                    
                elif state == 'READY' and data.upper() == 'DATA':
                    conn.sendall(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
                    state = 'RECEIVING_DATA'
                    email_data = []
                    
                elif state == 'RECEIVING_DATA':
                    if data == '.':
                        # Procesar el email completo
                        self.process_email(current_email, email_data)
                        conn.sendall(b"250 OK Message accepted\r\n")
                        state = 'READY'
                        current_email = {'from': '', 'to': [], 'subject': '', 'body': '', 'date': ''}
                    else:
                        email_data.append(data)
                        
                elif data.upper() == 'QUIT':
                    conn.sendall(b"221 Bye\r\n")
                    break
                else:
                    conn.sendall(b"500 Command not recognized\r\n")
                    
        except Exception as e:
            print(f"Error SMTP: {e}")
        finally:
            conn.close()
    
    def process_email(self, email, data_lines):
        """Procesa y guarda el email recibido"""
        email['body'] = '\n'.join(data_lines)
        email['date'] = datetime.now().isoformat()
        
        # Extraer subject si existe
        for line in data_lines:
            if line.lower().startswith('subject:'):
                email['subject'] = line[8:].strip()
                break
        
        # Guardar email
        filename = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(email, f, indent=2)
        
        print(f"[SMTP] Email guardado: {filename}")
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        
        print(f"Servidor SMTP escuchando en {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = sock.accept()
                thread = threading.Thread(
                    target=self.handle_smtp_session,
                    args=(conn, addr)
                )
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nCerrando servidor SMTP...")
        finally:
            sock.close()

if __name__ == "__main__":
    smtp_server = SimpleSMTPServer()
    smtp_server.start()