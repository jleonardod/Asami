def client_schema(client) -> dict:
    return {"id": int(client[0]),
            "create_time": client[1],
            "name": client[2],
            "last_name": client[3],
            "identification": client[4],
            "username": client[5],
            "email": client[6],
            "phone": client[7],
            "city": client[8],
            "country": client[9],
            "location": client[10],
            "type": client[11],
            "status": client[12]}

def clients_schema(clients) -> list:
    return [client_schema(client) for client in clients]