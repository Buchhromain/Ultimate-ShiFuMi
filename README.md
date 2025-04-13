# Ultimate ShiFuMi

![Python](https://img.shields.io/badge/Python-99.8%25-blue)

Ultimate ShiFuMi is a **Rock-Paper-Scissors** game project developed in Python.

---

## 🚀 Features

- Two-player gameplay.
- Players can choose between rock, paper, or scissors.
- Real-time communication between the client and the server using WebSockets.
- Players can either create a new game room or join an existing one.

---

## How It Works
1. Player 1 (Owner):
    - Creates a new game room.
    - Provides their name to the server.
    - Waits for Player 2 to join.
2. Player 2:
    - Joins an existing game room by entering the room ID.
    - Provides their name to the server.
3. GamePlay
    - Once both players are connected, the game starts.
    - Each player selects their move (rock, paper, or scissors).
    - The server determines the winner and sends the result to both players.
4. End of Game
    - The game ends when a winner is determined.
---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   cd Ultimate-ShiFuMi
   ```
2. Navigate to the project directory:
   ```bash
   git clone https://github.com/Buchhromain/Ultimate-ShiFuMi.git
   ```
3. Install dependencies (if required)
   ```bash
   pip install -r requirements.txt
   ```
   uvicorn main:app --reload
## 📖 Usage
- Run the main script in a terminal:
   ```bash
   uvicorn main:app --reload
   ```
- then the player in other termianl (with your own python's version):
  ```bash
    clear && python3 ./test_player.py
   ```
## Limitations

- **Two Players Only**: The game currently supports only two players. Additional players cannot join the same game room.
- **No Persistent Storage**: Game data is not stored persistently. Once the game ends, all data is lost.
- **Local Server**: The WebSocket server must be running locally on `127.0.0.1:8000`.

## Future Improvements

- Add support for more players.
- Implement a graphical user interface (GUI).
- Add persistent storage for game history.
- Deploy the WebSocket server to a public domain for remote gameplay.
