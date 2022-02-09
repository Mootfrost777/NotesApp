from serializer import Serializer
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()
db = Serializer('notes.json')  # New serializer instance


def get_notes_list():
    """Prints the ID and title of all notes."""
    notes = db.load()
    notes_str = ''
    if len(notes) == 0:
        return 'You don\'t have any notes right now.'
    notes_str += 'Notes list:'
    for el in notes:
        notes_str += '\nID: ' + el + '. Name: ' + notes[el]['header']
    return notes_str


def view_note(note_id: str):
    """Prints note content by ID."""
    notes = db.load()
    notes_str = 'ID: ' + note_id + '\n'
    notes_str += 'Name: ' + notes[note_id]['header'] + '\n'
    notes_str += notes[note_id]['content']
    return notes_str


@app.get('/')
def index():
    return PlainTextResponse('''Notes app:
add - create note.
list - Notes list.
get - read note.
remove - delete note.
''')


@app.get('/add')
def _1(name: str, text: str):
    note_id = db.add(name, text)
    return PlainTextResponse(f'Note with id {note_id} successfully added.')


@app.get('/list')
def _2():
    return PlainTextResponse(get_notes_list())


@app.get('/get')
def _3(id: str):
    return PlainTextResponse(view_note(id))


@app.get('/remove')
def _4(id: str):
    if db.delete(id) != 0:
        return 'Note with this ID not found. Try again.'
    else:
        return PlainTextResponse(f'Note with id {id} removed.')


db.configure_json({})  # Create new file and structure if not exists

uvicorn.run(app)
