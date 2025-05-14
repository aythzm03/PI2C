# PI2C
## Matricules des étudiants : 22294 et 22080

Ce fichier parlera de la stratégies utilisé par notre IA ainsi que les bibliothèques qu'elle utilise pour bien fonctionner et jouer au jeu QUARTO.

## Stratégies de l'IA

Tout d'abord dans ce code nous avons implémenter 3 stratégies qui correspondent aux différents degré de "force" de notre IA : "easy", "normal" et "hard".

### Mode "easy"
 le mode Easy de l'IA est juste un bot random qui donne et joue une pièce aléatoirement à l'adversaire sans faire de bad moves. A part ça il n'a rien de particulier.

### mode "normal"
Le mode "normal" est un peu plus poussé. Il a une stratégie plus défensive , il va par exemple éviter de donner des pièces à l'adversaire qui lui permettrait d'aligner 4 pièces qui ont une caractéristique commune.Il est aussi capable d'identifier une menace potentielle et la bloquer. Sinon elle joue aussi de manière aléatoire mais est meilleur que le mode "easy".

### mode "hard"
Le monde "hard", lui, bien sûr, est le meilleur des trois. Il possède des atouts défensifs et offensifs. On l'a doté de la capacité à detecter des opportunités de victoire. Il sait bien sûr bloquer stratégiquement l'adversaire pour l'empecher de gagner. Il peut detecter les lignes,colonnes,diagonales où l'adversaire pourrait gagner au prochain tour, il sait anticiper des coups à l'avance en simulant plusieurs scénario et déterminer la meilleure position du jeu. Et surtout il peut piéger l'adversaire en lui donnant une pièce qui semble utile mais est difficile à exploiter, le poussant à l'erreur.

## Bibliothèques
Ensuite pour les bibliothèques utilisées , il y a : random , itertools , json et socket.

- **Random** pour le choix aléatoire des pièces ou des positions sur le plateau.

- **Itertools** pour la génération de toutes les combinaisons -possibles de pièces.

- **Json** pour le formatage et lecture des données échangées avec le serveur.

- **Socket** pour la communication réseau TCP entre le client et le serveur , tout ce qui était inscription, réception des coups , envoi de réponses.
