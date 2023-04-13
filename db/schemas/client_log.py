def client_log_schema(client) -> dict:
    return {"username": client[0],
            "profile": int(client[1]),
            "password": client[2],
            "status": int(client[3]),
            "id": int(client[4])}