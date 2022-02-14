import json
import os.path


class Serializer:
    path: str  # JSON file path

    def __init__(self, path: str):
        self.path = path

    def add(self, name: str, text: str):
        """Adds a new element to the end of the dict."""
        note = {'name': name, 'text': text}
        notes = self.load()
        note_id = len(notes) + 1
        notes[note_id] = note
        self.dump(notes)
        return note_id

    def delete(self, element_id: str):
        """Removes an element from a dict by its ID."""
        notes = self.load()
        try:
            notes.pop(element_id)
        except KeyError:
            return -1
        self.dump(notes)
        self.index_id()
        return 0

    def append(self, element_id: str, text: str):
        """Appends text to an existing element by id"""
        notes = self.load()
        output = {}
        output_id = ''
        for note in notes:
            output[note] = notes[note]
            if note == element_id:
                output[note]['text'] += text
                output_id = note
        self.dump(output)
        return output_id

    def index_id(self):
        """Shifts dict element IDs."""
        notes = self.load()
        output = {}
        i = 1
        for note in notes:
            output[i] = notes[note]
            i += 1
        self.dump(output)

    def load(self):
        """Dict serialization."""
        with open(self.path) as f:
            notes = json.load(f)
        return notes

    def dump(self, notes: dict):
        """Dict deserialization."""
        with open(self.path, "w") as f:
            json.dump(notes, f)

    def configure_json(self, structure: dict):
        """Creates a JSON file and a structure in it if it doesn't exist."""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump(structure, f)
