import socket
import threading
import time
import json

# Server sozlamalari
HOST = '0.0.0.0'
PORT = 5555
MAX_PLAYERS = 4 # Maksimal 4 o'yinchi

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(MAX_PLAYERS)

print(f"Server {HOST}:{PORT} manzilida ishga tushdi...")

clients = {} # {client_socket: client_address}
players_data = {} # {player_id: {'position': [x, y, z], 'health': 20, 'address': client_address}}
player_id_counter = 1

# 100x100 maydon cheklovi
ARENA_SIZE = 100

def broadcast(message, sender_id=None):
    """Barcha ulangan klientlarga xabar yuborish."""
    message_bytes = (message + '\n').encode('utf-8')
    for client_socket, address in clients.items():
        if players_data.get(address, {}).get('id') != sender_id:
            try:
                client_socket.sendall(message_bytes)
            except:
                # Klient uzilgan bo'lsa
                print(f"Klient {address} uzildi (broadcast xatosi).")
                remove_client(client_socket, address)

def remove_client(client_socket, client_address):
    """Klientni ro'yxatdan o'chirish va boshqalarga xabar berish."""
    if client_socket in clients:
        del clients[client_socket]
    
    player_id = None
    for pid, data in players_data.items():
        if data['address'] == client_address:
            player_id = pid
            break
            
    if player_id is not None:
        del players_data[player_id]
        broadcast(f"DISCONNECT:{player_id}")
        print(f"O'yinchi {player_id} ({client_address}) uzildi.")
        
    try:
        client_socket.close()
    except:
        pass

def handle_client(client_socket, client_address):
    """Har bir klientdan kelgan ma'lumotlarni qabul qilish va qayta ishlash."""
    global player_id_counter
    
    # O'yinchi ID'sini belgilash
    player_id = player_id_counter
    player_id_counter += 1
    
    # Boshlang'ich ma'lumotlar
    players_data[player_id] = {
        'position': [50.0, 1.0, 50.0],
        'health': 20,
        'address': client_address
    }
    
    # Klientga o'z ID'sini yuborish
    client_socket.sendall(f"ID:{player_id}\n".encode('utf-8'))
    
    # Boshqa o'yinchilarga yangi o'yinchi haqida xabar berish
    broadcast(f"NEW_PLAYER:{player_id}:{50.0}:{1.0}:{50.0}", sender_id=player_id)
    
    # Yangi o'yinchiga mavjud o'yinchilar haqida ma'lumot yuborish
    for pid, data in players_data.items():
        if pid != player_id:
            client_socket.sendall(f"NEW_PLAYER:{pid}:{data['position'][0]}:{data['position'][1]}:{data['position'][2]}\n".encode('utf-8'))

    # Ma'lumotlarni qabul qilish
    buffer = ""
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            
            buffer += data
            
            while '\n' in buffer:
                message, buffer = buffer.split('\n', 1)
                
                if message.startswith("POS:"):
                    try:
                        _, x, y, z = message.split(':')
                        x, y, z = float(x), float(y), float(z)
                        
                        # 100x100 maydon cheklovi
                        x = max(0.0, min(ARENA_SIZE - 1.0, x))
                        z = max(0.0, min(ARENA_SIZE - 1.0, z))
                        
                        players_data[player_id]['position'] = [x, y, z]
                        
                        # 100x100 maydon cheklovi (server tomonida ham)
                        players_data[player_id]['position'][0] = max(0.0, min(ARENA_SIZE - 1.0, players_data[player_id]['position'][0]))
                        players_data[player_id]['position'][2] = max(0.0, min(ARENA_SIZE - 1.0, players_data[player_id]['position'][2]))
                        
                        # Boshqa o'yinchilarga harakatni yuborish
                        broadcast(f"MOVE:{player_id}:{players_data[player_id]['position'][0]:.2f}:{players_data[player_id]['position'][1]:.2f}:{players_data[player_id]['position'][2]:.2f}", sender_id=player_id)
                    except ValueError:
                        print(f"Noto'g'ri POS formati: {message}")
                
                elif message.startswith("ATTACK:"):
                    # Hujum ma'lumotlarini qayta ishlash (keyinroq)
                    broadcast(f"ATTACK:{player_id}", sender_id=player_id)
                    
                elif message.startswith("CHAT:"):
                    broadcast(message)
                    
                elif message.startswith("CHAT:"):
                    broadcast(message)
                    
                elif message.startswith("DAMAGE:"):
                    # Zarar ma'lumotlarini qayta ishlash
                    try:
                        _, target_id, damage = message.split(':')
                        target_id = int(target_id)
                        damage = float(damage)
                        
                        if target_id in players_data:
                            # Server tomonida himoyani hisoblash (Agar defense serverda bo'lsa)
                            # Hozircha defense faqat klientda hisoblanadi, ammo xavfsizlik uchun serverga o'tkazish kerak.
                            # Hozircha faqat zararni qabul qilamiz.
                            
                            players_data[target_id]['health'] -= damage
                            broadcast(f"HEALTH:{target_id}:{players_data[target_id]['health']:.2f}")
                            
                            if players_data[target_id]['health'] <= 0:
                                broadcast(f"DEATH:{target_id}")
                                # O'yinchi o'limi logikasi (masalan, respawn)
                                players_data[target_id]['health'] = 20.0 # Vaqtincha respawn
                                players_data[target_id]['position'] = [50.0, 1.0, 50.0]
                                broadcast(f"RESPAWN:{target_id}:{50.0:.2f}:{1.0:.2f}:{50.0:.2f}")
                                broadcast(f"HEALTH:{target_id}:20.0") # Sog'liqni tiklash
                                
                    except ValueError:
                        print(f"Noto'g'ri DAMAGE formati: {message}")
                
                elif message.startswith("ROT:"):
                    try:
                        _, rot_y, rot_x = message.split(':')
                        rot_y, rot_x = float(rot_y), float(rot_x)
                        broadcast(f"ROT:{player_id}:{rot_y}:{rot_x}", sender_id=player_id)
                    except ValueError:
                        print(f"Noto'g'ri ROT formati: {message}")
                        
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Xato: {e}")
            break

    remove_client(client_socket, client_address)

def accept_connections():
    """Klient ulanishlarini qabul qilish."""
    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"Yangi ulanish: {client_address}")
            
            if len(clients) < MAX_PLAYERS:
                clients[client_socket] = client_address
                thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                thread.start()
            else:
                client_socket.sendall("SERVER_FULL\n".encode('utf-8'))
                client_socket.close()
        except Exception as e:
            print(f"Ulanishni qabul qilish xatosi: {e}")
            break

# Ulanishlarni qabul qilishni boshlash
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Serverni to'xtatish uchun oddiy loop
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Server to'xtatildi.")
    server.close()
    for client in list(clients.keys()):
        remove_client(client, clients[client])
