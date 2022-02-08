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
    notes_str = ''
    notes_str += 'ID: ' + note_id + '\n'
    notes_str += 'Name: ' + notes[note_id]['header'] + '\n'
    notes_str += notes[note_id]['content']
    return notes_str


@app.get('/')
def index():
    return PlainTextResponse('''Notes app:
1.Create note.
2.Notes list.
3.Read note.
4.Delete note.
5.Exit.
''')


@app.get('/1')
def _1(header: str, content: str):
    db.add(header, content)
    return PlainTextResponse('OK')


@app.get('/2')
def _2():
    return PlainTextResponse(get_notes_list())


@app.get('/3')
def _3(id: str):
    return PlainTextResponse(view_note(id))


@app.get('/4')
def _4(id: str):
    if db.delete(id) != 0:
        return 'Note with this ID not found. Try again.'
    else:
        return PlainTextResponse('OK')


db.configure_json({})  # Create new file and structure if not exists

uvicorn.run(app)