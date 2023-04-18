def is_numeric(flag : str):
    try:
        complex(flag)
        return True
    except:
        return False