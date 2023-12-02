def read_file(filename: str) -> str:
    try:
        with open(filename) as file:
            return file.read()
    except OSError:
        return ""
