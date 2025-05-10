import socket
import json

def subscribe_to_server():
    server_host = "172.17.10.36"  # Adresse IP du serveur (à adapter si besoin)
    server_port = 3000            # Port du serveur

    subscribe_message = {
        "request": "subscribe",
        "port": 8888,  # Port d'écoute de ton client (il doit être en écoute dessus)
        "name": "AyatChampion2",  # Nom de ton IA
        "matricules": ["22088", "22292"]  # Tes matricules
    }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_host, server_port))
            s.send(json.dumps(subscribe_message).encode())
            response = s.recv(1024).decode()
            print("Réponse du serveur :", response)
    except ConnectionRefusedError:
        print("❌ Impossible de se connecter au serveur.")

subscribe_to_server()
def listen_for_requests():
    import socket
    import json

    host = "0.0.0.0"
    port = 8888  # Doit être le même que dans subscribe

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"✅ Client en écoute sur le port {port}...")

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
                        # Exemple de réponse automatique :
                        response = {
                            "response": "move",
                            "move": "example",  # À adapter au jeu
                            "message": "Let's go!"
                        }
                        print("🎮 Coup joué : example")
                        conn.send(json.dumps(response).encode())

                    else:
                        print("⚠️ Requête inconnue.")
subscribe_to_server()
listen_for_requests()
