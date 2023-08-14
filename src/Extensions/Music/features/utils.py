

def get_stream(link:str):
    if (not link.startswith("https://") or not link.startswith("http://")):
        return link
    if link.startswith("https://"):
        stripped = link.strip("https://")
    if link.startswith("http://"):
        stripped = link.strip("http://")
    if stripped.startswith("www"):
        stripped = stripped.strip("www.")
    stripped = stripped.split(".")
    return stripped[0]