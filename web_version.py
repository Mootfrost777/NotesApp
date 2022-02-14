from serializer import Serializer
from fastapi import FastAPI, Body
from fastapi.responses import PlainTextResponse
import uvicorn

app = FastAPI()
db = Serializer('notes.json')  # New serializer instance


def get_notes_list():
    """Returns the ID and title of all notes."""
    notes = db.load()
    notes_str = ''
    if len(notes) == 0:
        return 'You don\'t have any notes right now.'
    notes_str += 'Notes list:'
    for el in notes:
        notes_str += '\nID: ' + el + '. Name: ' + notes[el]['name']
    return notes_str


def view_note(note_id: str):
    """Returns note content by ID."""
    notes = db.load()
    notes_str = 'ID: ' + note_id + '\n'
    notes_str += 'Name: ' + notes[note_id]['name'] + '\n'
    notes_str += notes[note_id]['text']
    return notes_str


@app.get('/')
def index():
    return PlainTextResponse('''Notes app:
add - create note.
list - Notes list.
get - read note.
remove - delete note.
''')


@app.post('/add')
def _add(name: str = Body(..., embed=True), text: str = Body(..., embed=True)):
    """Adds new note."""
    note_id = db.add(name, text)
    return PlainTextResponse(f'Note with id {note_id} successfully added.')


@app.get('/list')
def _list():
    """Gets notes list."""
    return PlainTextResponse(get_notes_list())


@app.get('/get')
def _get(id: str):
    """Gets note by ID."""
    return PlainTextResponse(view_note(id))


@app.post('/append')
def _append(id: str = Body(..., embed=True), text: str = Body(..., embed=True),):
    return PlainTextResponse(f'The text was successfully added to the note with id {db.append(id, text)}.')


@app.post('/remove')
def _remove(id: str = Body(..., embed=True)):
    """Removes note by ID."""
    if db.delete(id) != 0:
        return 'Note with this ID not found. Try again.'
    else:
        return PlainTextResponse(f'Note with id {id} removed.')


db.configure_json({})  # Create new file and structure if not exists

uvicorn.run(app)
