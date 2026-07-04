<div align="center">

# 🤐 CMD-CHAT

### encrypted terminal chat. no servers. no logs. ram only.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

peer-to-peer encrypted chat that runs in your terminal. you host, you control. close the window — everything's gone.

## why

every "secure" messenger still stores metadata somewhere. this doesn't. it's just two terminals talking over an encrypted tunnel. nothing written to disk, ever.

## how it works

```
┌──────────────────────────────────────────────────────────────────┐
│                        SRP AUTHENTICATION                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CLIENT                                         SERVER           │
│    │                                              │              │
│    │─────── POST /srp/init {username, A} ───────► │              │
│    │         (A = client public ephemeral)        │              │
│    │                                              │              │
│    │◄──── {user_id, B, salt, room_salt} ───────── │              │
│    │         (B = server public ephemeral)        │              │
│    │         (room_salt = E2E key derivation)     │              │
│    │                                              │              │
│    │  [client derives room_key via HKDF:          │              │
│    │   room_key = HKDF(password, room_salt)]      │              │
│    │                                              │              │
│    │  [both sides compute SRP session key         │              │
│    │   using password + ephemeral values]         │              │
│    │                                              │              │
│    │─────── POST /srp/verify {user_id, M} ──────► │              │
│    │         (M = client proof)                   │              │
│    │                                              │              │
│    │◄────────── {H_AMK, session_key} ──────────── │              │
│    │         (H_AMK = server proof)               │              │
│    │                                              │              │
│    │  [password never transmitted]                │              │
│    │  [MITM can't derive session key]             │              │
│    │                                              │              │
├──────────────────────────────────────────────────────────────────┤
│                      E2E ENCRYPTED CHAT                          │
├──────────────────────────────────────────────────────────────────┤
│    │                                              │              │
│    │═══════ WebSocket /ws/chat?user_id ═════════► │              │
│    │         (authenticated session)              │              │
│    │                                              │              │
│    │                                              │              │
│  ┌─┴─┐                                        ┌──┴──┐            │
│  │ C │──── encrypt(msg, room_key) ───────────►│  S  │            │
│  │ L │                                        │  E  │            │
│  │ I │◄─── ciphertext (broadcast) ────────────│  R  │            │
│  │ E │                                        │  V  │            │
│  │ N │     decrypt(ciphertext, room_key)      │  E  │            │
│  │ T │                                        │  R  │            │
│  └─┬─┘                                        └──┬──┘            │
│    │                                              │              │
│    │  [server stores ONLY ciphertext]             │              │
│    │  [server CANNOT read messages]               │              │
│    │  [all clients with same password             │              │
│    │   derive identical room_key]                 │              │
│    │                                              │              │
│    │  Encryption: Fernet (AES-128-CBC + HMAC)     │              │
│    │  Key derivation: HKDF-SHA256                 │              │
│    │                                              │              │
│    │  [on disconnect: keys wiped from RAM]        │              │
│    │                                              │              │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                      KEY HIERARCHY                               │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  password ──┬──► SRP ──► session_key (per-user, auth only)       │
│             │                                                    │
│             └──► HKDF(password, room_salt) ──► room_key (shared) │
│                                                                  │
│  room_salt: generated once at server start                       │
│  room_key:  deterministic, same for all clients with same pwd    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**SRP (Secure Remote Password)** — password is never sent over the network. both sides prove they know it via zero-knowledge proof, then derive identical session keys.

## install

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

windows:

```bash
python -m venv venv ; .\venv\Scripts\activate ; pip install -r requirements.txt
```

## usage

start server:

```bash
python cmd_chat.py serve 0.0.0.0 3000 --password mysecret
```

connect:

```bash
python cmd_chat.py connect SERVER_IP 3000 username mysecret
```

![Example](example.gif)

## features

- **ram only** — nothing touches disk
- **rsa + aes** — key exchange + symmetric encryption
- **no central server** — direct p2p connection
- **srp auth** — password never sent over network

## 🚀 How to Setup and Run (Windows Guide)

Follow these exact steps to clone the repository, set up your environment, and start chatting.

### 1. Clone and Navigate to the Repository
Clone the repository to your local machine and move into the project folder:
```powershell
git clone https://github.com
cd cmd-chat
```

### 2. Set Up the Environment
Bypass the Windows PowerShell script execution policy so you can activate scripts:
```powershell
set-executionpolicy -executionpolicy bypass -scope process
```

Create your Python virtual environment:
```powershell
python -m venv venv
```

Activate the virtual environment:
```powershell
.\venv\Scripts\activate
```

Install all the required package dependencies:
```powershell
pip install -r requirements.txt
```

---

## 💬 How to Chat

### Step 3: Start the Server (Host)
Open a PowerShell tab to host the chat room. Run the python script using the `serve` command, your chosen local IP, a port number, and a secure password:
```powershell
python cmd_chat.py serve 127.0.0.1 8000 --password mysecretpassword
```

### Step 4: Connect Locally
Open a **new** PowerShell tab, navigate to the folder, activate the virtual environment, and connect by passing the host IP, port, your username, and the password:
```powershell
python cmd_chat.py connect 127.0.0.1 8000 local_user mysecretpassword
```

### Step 5: Connect Globally Across the Internet (Optional)
If you want to chat with someone outside your local network (e.g., in another part of the world), you can expose your local port securely using **ngrok**.

1. Download and install [ngrok](https://ngrok.com).
2. Keep your server from **Step 3** running.
3. Open a **new** terminal window and expose port 8000:
   ```powershell
   ngrok http 8000
   ```
4. Ngrok will generate a public forwarding URL that looks like `0.tcp.ngrok.io` along with a unique port number (e.g., `14832`).
5. Your friend can now connect from anywhere in the world by running:
   ```powershell
   python cmd_chat.py connect 0.tcp.ngrok.io 14832 friend_username mysecretpassword
   ```

