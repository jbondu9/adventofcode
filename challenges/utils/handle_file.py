def read_file(filename: str) -> list[str]:
    try:
        with open(filename) as file:
            data = file.read()
            return data.split("\n")[:-1]
    except OSError:
        return ""
