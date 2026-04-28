# 🎮 Tic-Tac-Toe Online
A multiplayer Tic-Tac-Toe game.
<img width="1542" height="862" alt="image" src="https://github.com/user-attachments/assets/0a6bdfcb-3927-48b0-ab5f-21c55b411943" />

## 🏗 System Architecture
    Backend (FastAPI): Handles REST API for authentication, user profiles, leaderboards and game history.
    Socket Server (Go): A server using WebSockets for real-time gameplay and matchmaking.
    Frontend (Vue.js 3): A reactive SPA built with Vite, TypeScript, and Pinia.

## 🚀 Tech Stack
    Backend: Python 3.14, FastAPI, asyncpg.
    Real-time: Go 1.26, Gorilla WebSocket.
    Frontend: Vue 3, TypeScript, Vite, Tailwind, HeadlessUI Vue, Pinia.
    Data: PostgreSQL (Primary DB), Redis (Caching).

## Some information about project
* ✅ **This is pet project, not the best website for playing tic tac toe**
* ✅ If website not avaliable now, that because i run out of money to continue pay for VPS.
 
## 📝 Getting Started
1. Clone the repository:
```bash
git clone https://github.com/Jud1k/tic-tac-toe.git
```
2. Install the dependencies:
```bash
cd tic-tac-toe
uv venv
```
3. Create a `.env` file in the root directory and add variables by following the `.env.example` file.

4. Apply migrations (need install <a href="[https://example.com](https://github.com/amacneil/dbmate)" target="_blank" rel="noopener noreferrer">dbmate</a>)
:
```bash
dbmate up
```

5. Run the FastAPI backend:
```bash
cd services/api-service
./scripts/dev.sh
```

6. Run the Socket Server:
```bash
cd services/socket-server
air
```

7. Run the frontend:
```bash
cd frontend
bun install
bun dev
```

or use Docker:
```bash
docker compose up
```

## 📝 License
This project is licensed under the MIT License. 
