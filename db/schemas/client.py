def client_schema(client) -> dict:
    return {"id": int(client[0]),
            "name": client[1],
            "last_name": client[2],
            "identification": client[3],
            "email": client[4],
            "phone": client[5],
            "city": client[6],
            "country": client[7],
            "location": client[8],
            "type": client[9]}

def clients_schema(clients) -> list:
    return [client_schema(client) for client in clients]