import json
import os.path

path: str  # JSON file path


def add(header: str, content: str):
    """Adds a new element to the end of the dict."""
    note = {'header': header, 'content': content}
    notes = load_dict()
    notes[len(notes)] = note
    dump_dict(notes)


def delete(element_id: str):
    """Removes an element from a dict by its ID."""
    notes = load_dict()
    try:
        notes.pop(element_id)
    except KeyError:
        return -1
    dump_dict(notes)
    index_id()
    return 0


def index_id():
    """Shifts dict element IDs."""
    notes = load_dict()
    output = {}
    i = 1
    for el in notes:
        output[i] = notes[el]
        i += 1
    dump_dict(output)


def load_dict():
    """Dict serialization."""
    with open(path) as f:
        notes = json.load(f)
    return notes


def dump_dict(notes: dict):
    """Dict deserialization."""
    with open(path, "w") as f:
        json.dump(notes, f)


def configure_json(structure: dict):
    """Creates a JSON file and a structure in it if it doesn't exist."""
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump({}, f)
