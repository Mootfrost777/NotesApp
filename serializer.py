import json
import os.path


def check_success(element_id):
    """Returns 0 if the id is not empty, another number if empty or not suitable."""
    if element_id != '':
        return 0
    else:
        return -1


class Serializer:
    path: str  # JSON file path

    def __init__(self, path: str):
        self.path = path

    def add(self, name: str, text: str):
        """Adds a new element to the dict."""
        el = {'name': name, 'text': text}
        elements = self.load()
        element_id = len(elements) + 1
        elements[element_id] = el
        self.dump(elements)
        return element_id

    def delete(self, element_id: str):
        """Removes an element from a dict by its ID."""
        elements = self.load()
        try:
            elements.pop(element_id)
        except KeyError:
            return -1
        self.dump(elements)
        self.index_id()
        return 0

    def append(self, element_id: str, text: str):
        """Appends text to an existing element by ID."""
        elements = self.load()
        output = {}
        output_id = ''
        for note in elements:
            output[note] = elements[note]
            if note == element_id:
                output[note]['text'] += text
                output_id = note
        self.dump(output)
        return check_success(output_id)

    def change_name(self, element_id: str, name: str):
        """Changes the name of the note by ID."""
        elements = self.load()
        output = {}
        output_id = ''
        for el in elements:
            output[el] = elements[el]
            if el == element_id:
                output[el]['name'] = name
                output_id = el
        self.dump(output)
        return check_success(output_id)

    def index_id(self):
        """Shifts dict element IDs."""
        elements = self.load()
        output = {}
        i = 1
        for el in elements:
            output[i] = elements[el]
            i += 1
        self.dump(output)

    def load(self):
        """Dict serialization."""
        with open(self.path) as f:
            elements = json.load(f)
        return elements

    def dump(self, elements: dict):
        """Dict deserialization."""
        with open(self.path, "w") as f:
            json.dump(elements, f)

    def configure_json(self, structure: dict):
        """Creates a JSON file and a structure in it if it doesn't exist."""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump(structure, f)
