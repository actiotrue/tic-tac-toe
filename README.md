# 🎮 Tic-Tac-Toe Online
A multiplayer Tic-Tac-Toe game built with a microservices architecture.

## 🏗 System Architecture
    Backend (FastAPI): Handles REST API for authentication, user profiles, leaderboards and game history.
    Socket Server (Go): A server using WebSockets for real-time gameplay and matchmaking.
    Frontend (Vue.js 3): A reactive SPA built with Vite, TypeScript, and Pinia.

## 🚀 Tech Stack
    Backend: Python 3.14, FastAPI, asyncpg.
    Real-time: Go 1.26, Gorilla WebSocket.
    Frontend: Vue 3, TypeScript, Vite, Axios.
    Data: PostgreSQL (Primary DB), Redis (Caching & Queue).

## 📝 Getting Started
1. Clone the repository:
```bash
git clone https://github.com/Jud1k/tic-tac-toe.git
```
2. Install the dependencies:
```bash
cd tic-tac-toe
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add variables by following the `.env.example` file.

4. Run the FastAPI backend:
```bash
cd services/api-service
./scripts/dev.sh
```

5. Run the Socket Server:
```bash
cd services/socket-server
air
```

6. Run the frontend:
```bash
cd frontend
bun install
bun dev
```

## 📝 License
This project is licensed under the MIT License. 