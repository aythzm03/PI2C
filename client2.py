import random
from itertools import product
import socket
import json
import itertools

# Génère toutes les pièces possibles
def generate_all_pieces():
    return [''.join(p) for p in product('BS', 'DL', 'EF', 'CP')]

# Choisit une position libre aléatoirement
def choose_random_position(board):
    empty_indices = [i for i, cell in enumerate(board) if cell is None]
    return random.choice(empty_indices) if empty_indices else None

# Choisit une pièce encore disponible aléatoirement
def choose_random_piece(state):
    all_pieces = set(generate_all_pieces())
    used_pieces = set(p for p in state['board'] if p) | {state["piece"]}
    remaining_pieces = list(all_pieces - used_pieces)
    return random.choice(remaining_pieces) if remaining_pieces else None

# Effectue un coup aléatoire valide
def make_move(state):
    return {
        "pos": choose_random_position(state["board"]),
        "piece": choose_random_piece(state)
    }

# Toutes les pièces possibles
ALL_PIECES = [''.join(p) for p in itertools.product('BS', 'DL', 'EF', 'CP')]

# S’abonner au serveur (Client 2 avec un port et nom différents)
def subscribe_to_server():
    server_host = "172.17.82.125"  # Adresse IP du serveur
    server_port = 3000

    subscribe_message = {
        "request": "subscribe",
        "port": 8889,  # ⚠️ Port différent pour le client 2
        "name": "WIAME2",  # ⚠️ Nom différent pour éviter les conflits
        "matricules": ["22088", "22292"]
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            s.send(json.dumps(subscribe_message).encode())
            response = s.recv(1024).decode()
            print("Réponse du serveur :", response)
    except ConnectionRefusedError:
        print("❌ Impossible de se connecter au serveur.")

# Donne les positions libres
def get_free_positions(board):
    return [i for i, val in enumerate(board) if val is None]

# Donne les pièces déjà jouées
def get_used_pieces(board):
    return set(p for p in board if p is not None)

# Choix aléatoire (comme Client 1, mais isolé ici)
def choose_move(board, current_piece):
    free_positions = get_free_positions(board)
    used_pieces = get_used_pieces(board)
    used_pieces.add(current_piece)

    remaining_pieces = [p for p in ALL_PIECES if p not in used_pieces]

    pos = random.choice(free_positions) if free_positions else None
    next_piece = random.choice(remaining_pieces) if remaining_pieces else None

    return {"pos": pos, "piece": next_piece}

# Réception et traitement des requêtes
def listen_for_requests():
    host = "0.0.0.0"
    port = 8889  # ⚠️ Port différent

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"✅ Client 2 en écoute sur le port {port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096).decode()
                if data:
                    print("📩 Requête reçue :", data)
                    request = json.loads(data)

                    if request["request"] == "ping":
                        response = {"response": "pong"}
                        print("↪️ Réponse : pong")
                        conn.send(json.dumps(response).encode())

                    elif request["request"] == "play":
                        state = request["state"]
                        board = state["board"]
                        piece_to_play = state["piece"]

                        move = choose_move(board, piece_to_play)

                        response = {
                            "response": "move",
                            "move": move,
                            "message": "🤖 Client 2 : coup aléatoire joué"
                        }
                        print("🎮 Coup joué :", move)
                        conn.send(json.dumps(response).encode())

                    else:
                        print("⚠️ Requête inconnue.")

# Lancement
subscribe_to_server()
listen_for_requests()