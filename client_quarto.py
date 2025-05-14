import random
from itertools import product
import json
import socket
import itertools
DIFFICULTY = "hard"  # "easy", "normal", "hard"
def log(message):
    print("[LOG]", message)

# Liste de toutes les pièces possibles
ALL_PIECES = [''.join(p) for p in itertools.product('BS', 'DL', 'EF', 'CP')]

# Liste des pièces déjà utilisées
used_pieces = set()
# Liste des pièces données à l'adversaire
given_pieces = set()

def generate_all_pieces():
    return [''.join(p) for p in product('BS', 'DL', 'EF', 'CP')]

def choose_random_position(board):
    empty_indices = [i for i, cell in enumerate(board) if cell is None]
    return random.choice(empty_indices) if empty_indices else None

def choose_random_piece(state):
    all_pieces = set(generate_all_pieces())
    used_pieces = set(p for p in state['board'] if p) | {state["piece"]}
    remaining_pieces = list(all_pieces - used_pieces)
    return random.choice(remaining_pieces) if remaining_pieces else None

def get_free_positions(board):
    """Récupère les positions libres sur le plateau"""
    return [i for i, val in enumerate(board) if val is None]

def get_used_pieces(board):
    """Récupère les pièces déjà placées sur le plateau"""
    return set(p for p in board if p is not None)

def get_threats(board, piece_to_play):
    """Renvoie les positions où poser la pièce permettrait à l'adversaire de gagner,
    en détectant les alignements dangereux basés sur les attributs."""
    threats = []

    def check_line(line_indices):
        # Récupère les pièces présentes
        line_pieces = [board[i] for i in line_indices]
        if line_pieces.count(None) != 1:
            return None  # Il faut exactement une case vide

        # On récupère les pièces non vides
        pieces = [p for p in line_pieces if p is not None]
        common_attributes = set(pieces[0])

        # On garde uniquement les attributs communs à toutes les pièces
        for p in pieces[1:]:
            common_attributes &= set(p)

        # Si un ou plusieurs attributs sont communs à toutes les pièces
        if common_attributes:
            # Retourner l'index de la case vide (menace)
            return line_indices[line_pieces.index(None)]
        return None

    # Lignes
    for i in range(4):
        idxs = [i * 4 + j for j in range(4)]
        threat = check_line(idxs)
        if threat is not None:
            threats.append(threat)

    # Colonnes
    for j in range(4):
        idxs = [i * 4 + j for i in range(4)]
        threat = check_line(idxs)
        if threat is not None:
            threats.append(threat)

    # Diagonale principale
    diag1 = [i * 5 for i in range(4)]  # 0, 5, 10, 15
    threat = check_line(diag1)
    if threat is not None:
        threats.append(threat)

    # Diagonale inverse
    diag2 = [3 + 4 * i for i in range(4)]  # 3, 6, 9, 12
    threat = check_line(diag2)
    if threat is not None:
        threats.append(threat)

    return threats


def choose_piece_to_give(state):
    all_pieces = set(generate_all_pieces())
    used_pieces = set(p for p in state['board'] if p) | {state["piece"]}
    remaining_pieces = list(all_pieces - used_pieces)
    board = state["board"]

    if DIFFICULTY == "easy":
        return random.choice(remaining_pieces)

    if DIFFICULTY == "normal":
        threats = get_threats(board, state["piece"])
        return random.choice([p for p in remaining_pieces if p not in threats]) or random.choice(remaining_pieces)

    if DIFFICULTY == "hard":
        return choose_piece_with_trap_strategy(state)

    # Par défaut
    return random.choice(remaining_pieces)


def choose_move(state):
    board = state["board"]
    current_piece = state["piece"]

    # 1. Voir si on peut gagner immédiatement
    winning_moves = get_opportunities(board, current_piece)
    if winning_moves:
        pos = winning_moves[0]
        print(f"L'IA peut gagner en jouant à la position {pos}")
    else:
        # 2. Sinon, vérifier si l’adversaire peut gagner (menace)
        threats = get_threats(board, current_piece)
        if threats:
            pos = threats[0]
            print(f"⚠️ L'IA bloque une menace en jouant à la position {pos}")
        else:
        # 3. Anticipation intelligente
            pos = choose_best_position_with_anticipation(state)
            if pos is not None:
                log(f"L'IA anticipe les coups et joue à la position {pos}")
            else:
                free_positions = get_free_positions(board)
                pos = random.choice(free_positions) if free_positions else None
                log(f"Aucun bon coup anticipé, l'IA joue au hasard à la position {pos}")

    # Choix de la pièce à donner
    next_piece = choose_piece_to_give(state)

    return {
        "pos": pos,
        "piece": next_piece
    }

def check_win(board):
    """Vérifie si un alignement de 4 pièces a été formé (victoire)"""
    def same(L):
        if None in L:
            return False
        common = frozenset(L[0])
        for elem in L[1:]:
            common = common & frozenset(elem)
        return len(common) > 0

    # Vérifie les lignes et les colonnes
    for i in range(4):
        if same([board[i * 4 + j] for j in range(4)]):  # Ligne
            return True
        if same([board[j * 4 + i] for j in range(4)]):  # Colonne
            return True

    # Vérifie les diagonales
    if same([board[i * 4 + i] for i in range(4)]):  # Diagonale principale
        return True
    if same([board[i * 4 + (3 - i)] for i in range(4)]):  # Diagonale inverse
        return True

    return False


def subscribe_to_server():
    server_host = "192.168.1.52"  # Adresse IP du serveur
    server_port = 3000            # Port du serveur

    subscribe_message = {
        "request": "subscribe",
        "port": 8888,  # Port d'écoute du client
        "name": "BOT1",  # Nom de l'IA
        "matricules": ["22911", "22005"]
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            s.send(json.dumps(subscribe_message).encode())
            response = s.recv(1024).decode()
            print("Réponse du serveur :", response)
    except ConnectionRefusedError:
        print("❌ Impossible de se connecter au serveur.")

def listen_for_requests():
    host = "0.0.0.0"
    port = 8888


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"✅ Client en écoute sur le port {port}...")

        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(4096).decode()
                if data:
                    print("Requête reçue :", data)
                    request = json.loads(data)

                    if request["request"] == "ping":
                        response = {"response": "pong"}
                        print("↪️ Réponse : pong")
                        conn.send(json.dumps(response).encode())

                    elif request["request"] == "play":
                        state = request["state"]
                        move = choose_move(state)

                        response = {
                            "response": "move",
                            "move": move,
                            "message": "IA stratégique : analyse des menaces et des opportunités"
                        }
                        print("Coup joué :", move)
                        conn.send(json.dumps(response).encode())

                    else:
                        print("⚠️ Requête inconnue.")

def get_opportunities(board, current_piece):
    """Renvoie les positions où poser la pièce actuelle permettrait à l'IA de gagner (alignement d'attributs communs)."""
    opportunities = []

    def is_winning_line(line_indices):
        line_pieces = [board[i] for i in line_indices]
        if line_pieces.count(None) != 1:
            return None  # Une seule case doit être vide

        # Récupérer les pièces présentes
        pieces = [p for p in line_pieces if p is not None]
        pieces.append(current_piece)  # Ajouter la pièce qu'on va poser

        # Vérifier s’il existe un attribut commun entre toutes les pièces
        common_attributes = set(pieces[0])
        for p in pieces[1:]:
            common_attributes &= set(p)

        if common_attributes:
            # Retourne l’index de la case vide
            return line_indices[line_pieces.index(None)]
        return None

    # Vérifie lignes
    for i in range(4):
        idxs = [i * 4 + j for j in range(4)]
        opp = is_winning_line(idxs)
        if opp is not None:
            opportunities.append(opp)

    # Vérifie colonnes
    for j in range(4):
        idxs = [i * 4 + j for i in range(4)]
        opp = is_winning_line(idxs)
        if opp is not None:
            opportunities.append(opp)

    # Diagonales
    diag1 = [i * 5 for i in range(4)]
    opp = is_winning_line(diag1)
    if opp is not None:
        opportunities.append(opp)

    diag2 = [3 + 4 * i for i in range(4)]
    opp = is_winning_line(diag2)
    if opp is not None:
        opportunities.append(opp)

    return opportunities


def choose_best_position_with_anticipation(state):
    board = state["board"]
    current_piece = state["piece"]
    all_pieces = set(generate_all_pieces())
    used_pieces = set(p for p in board if p) | {current_piece}
    remaining_pieces = list(all_pieces - used_pieces)

    best_pos = None
    best_score = float('-inf')

    for pos in get_free_positions(board):
        simulated_board = board.copy()
        simulated_board[pos] = current_piece

        # Score de base : on gagne directement ?
        if check_win(simulated_board):
            return pos  # victoire immédiate, pas besoin d'anticiper

        # Score initial du coup
        score = 0

        # On suppose qu'on donne une pièce au hasard à l'adversaire
        for piece in remaining_pieces:
            for adv_pos in get_free_positions(simulated_board):
                adv_board = simulated_board.copy()
                adv_board[adv_pos] = piece
                if check_win(adv_board):
                    score -= 5  # danger : l’adversaire pourrait gagner
                else:
                    score += 1  # coup relativement sûr

        if score > best_score:
            best_score = score
            best_pos = pos

    return best_pos

def choose_piece_with_trap_strategy(state):
    board = state["board"]
    all_pieces = set(generate_all_pieces())
    used_pieces = set(p for p in board if p) | {state["piece"]}
    remaining_pieces = list(all_pieces - used_pieces)

    safe_pieces = []
    trap_pieces = []

    for piece in remaining_pieces:
        danger = False
        trap = True  # On suppose que c’est un piège sauf preuve du contraire

        for pos in get_free_positions(board):
            simulated_board = board.copy()
            simulated_board[pos] = piece

            if check_win(simulated_board):
                danger = True  # L'adversaire pourrait gagner
                trap = False   # Pas un bon piège, trop risqué
                break

            # Le piège ne marche pas si un alignement dangereux est en construction
            if count_common_attributes_in_line(simulated_board, pos) >= 2:
                trap = False

        if not danger:
            safe_pieces.append(piece)
        elif trap:
            trap_pieces.append(piece)

    if trap_pieces:
        chosen = random.choice(trap_pieces)
        log(f"Piège tendu avec la pièce : {chosen}")
        return chosen

    if safe_pieces:
        return random.choice(safe_pieces)

    return random.choice(remaining_pieces)


def count_common_attributes_in_line(board, index):
    """Retourne combien d'attributs sont communs sur la ligne, colonne ou diagonale de la case index."""
    i, j = divmod(index, 4)
    directions = [
        [i * 4 + k for k in range(4)],  # ligne
        [k * 4 + j for k in range(4)],  # colonne
    ]
    if i == j:
        directions.append([k * 5 for k in range(4)])  # diagonale principale
    if i + j == 3:
        directions.append([3 + 4 * k for k in range(4)])  # diagonale secondaire

    max_common = 0
    for line in directions:
        pieces = [board[k] for k in line if board[k] is not None]
        if len(pieces) < 2:
            continue
        common = set(pieces[0])
        for p in pieces[1:]:
            common &= set(p)
        max_common = max(max_common, len(common))

    return max_common

# Exécution
subscribe_to_server()
listen_for_requests()
