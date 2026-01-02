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
│    │◄────────── {user_id, B, salt} ────────────── │              │
│    │         (B = server public ephemeral)        │              │
│    │                                              │              │
│    │                                              │              │
│    │  [both sides compute shared session key      │              │
│    │   using password + ephemeral values]         │              │
│    │                                              │              │
│    │                                              │              │
│    │─────── POST /srp/verify {user_id, M} ──────► │              |
│    │         (M = client proof)                   │              │
│    │                                              │              │
│    │◄────────── {H_AMK, session_key} ──────────── │              │
│    │         (H_AMK = server proof)               │              │
│    │                                              │              │
│    │  [password never transmitted]                │              │
│    │  [MITM can't derive session key]             │              |
│    │                                              │              │
├──────────────────────────────────────────────────────────────────┤
│                        ENCRYPTED CHAT                            │
├──────────────────────────────────────────────────────────────────┤
│    │                                              │              │
│    │═══════ WebSocket /ws/chat?user_id ═════════► │              │
│    │         (authenticated session)              │              │
│    │                                              │              │
│    │◄═══════════ AES-encrypted messages ════════► │              │
│    │         (Fernet = AES-128-CBC + HMAC)        │              │
│    │                                              │              │
│    │                                              │              │
│    │  [on disconnect: keys wiped from RAM]        │              │
│    │                                              │              │
└──────────────────────────────────────────────────────────────────┘
```

**SRP (Secure Remote Password)** — password is never sent over the network. both sides prove they know it via zero-knowledge proof, then derive identical session keys.

## install

```bash
git clone https://github.com/emilycodestar/cmd-chat.git
cd cmd-chat
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

## license

MIT
