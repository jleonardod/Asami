def mark_schema(mark) -> list:
    return [int(mark[0]),
            mark[1]]

def mark_schema_json(mark) -> dict:
    return {"id" : int(mark[0]),
            "name" : mark[1]}

def marks_schema(marks) -> list:
    return [mark_schema(mark) for mark in marks]