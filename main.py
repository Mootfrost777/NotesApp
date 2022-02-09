from serializer import Serializer
import colorama as c

db = Serializer('notes.json')  # New serializer instance


def select_action():
    """Requests an action selection."""
    try:
        return int(input('Choose action: '))
    except ValueError:
        print(c.Fore.RED + 'Please enter correct action number.' + c.Fore.RESET)
        select_action()


def print_notes_list():
    """Prints the ID and title of all notes."""
    notes = db.load()
    if len(notes) == 0:
        print(c.Fore.LIGHTGREEN_EX + 'You don\'t have any notes right now.' + c.Fore.RESET)
    for el in notes:
        print(c.Fore.GREEN + 'ID: ' + el + c.Fore.YELLOW + '. Name: ' + notes[el]['header'])
        print(c.Fore.RESET, end='')


def view_note(note_id: str):
    """Prints note content by ID."""
    notes = db.load()
    print(c.Fore.GREEN + 'ID: ' + note_id)
    print(c.Fore.YELLOW + 'Name: ' + notes[note_id]['header'])
    print(c.Fore.CYAN + notes[note_id]['content'] + c.Fore.RESET)


db.configure_json({})  # Create new file and structure if not exists

print('''Notes app:
1.Create note.
2.Notes list.
3.Read note.
4.Delete note.
5.Exit.
''')

while True:
    choose = select_action()
    match choose:
        case 1:  # Create new note
            name = input('Enter note name: ')
            text = input('Enter note text: ')
            note_id = db.add(name, text)
            print(c.Fore.LIGHTGREEN_EX + 'Note with id {note_id} successfully added.' + c.Fore.RESET)
        case 2:  # Show notes list
            print_notes_list()
        case 3:  # Show note content by ID
            view_note(input('Enter note ID: '))
        case 4:  # Delete note by ID
            note_id = input('Enter note ID: ')
            if db.delete(note_id) != 0:
                print(c.Fore.RED + f'Note with id {note_id} not found. Try again.' + c.Fore.RESET)
            else:
                print(c.Fore.LIGHTGREEN_EX + 'Note with id {note_id} removed.' + c.Fore.RESET)
        case 5:
            exit(0)
