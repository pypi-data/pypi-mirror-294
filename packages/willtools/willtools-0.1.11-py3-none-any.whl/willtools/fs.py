import os


def list_subdirectories(path: str, reverse: bool = True):
    try:
        subdirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        subdirs.sort(reverse=reverse)
        return subdirs
    except FileNotFoundError:
        return []
