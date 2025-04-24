from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import Layout, HSplit
import ast
import autopep8
from termcolor import colored

# Define the code snippets
snippets = [
    'fruits = ["apple", "banana", "cherry"]\nfor f in fruits:\n    print(f)\n',
    'coords = (10, 20, 30)\nfor c in coords:\n    print(c)\n',
    'colors = {"red", "green", "blue"}\nfor col in colors:\n    print(col)\n',
    'person = {"name":"Alice","age":30}\nfor k, v in person.items():\n    print(k, ":", v)\n',
    'i = 0\nwhile i < 3:\n    print(i)\n    i += 1\n',
    'matrix = [[1,2],[3,4]]\nfor row in matrix:\n    for x in row:\n        print(x)\n'
]

kb = KeyBindings()
index = 0

# Create the text editor area
editor = TextArea(
    text='',
    multiline=True,
    wrap_lines=False,
    scrollbar=True,
)

# Create a frame to display the current snippet number
frame = Frame(editor, title=lambda: f"Snippet {index+1} of {len(snippets)}")

# Create the application layout
app = Application(
    layout=Layout(HSplit([frame])),
    key_bindings=kb,
    full_screen=True,
)

def show_message(msg: str, color='red'):
    """Print a colored message below the editor."""
    print(colored(msg, color), flush=True)

@kb.add('@')  # Bind Shift + @ to submit/check
def _(event):
    global index
    code = editor.text
    try:
        ast.parse(code)  # Syntax and indentation check
        show_message("✅ Correct! Moving to next snippet.", 'green')
    except (SyntaxError, IndentationError) as e:
        show_message(f"{type(e).__name__}: {e.msg} at line {e.lineno}, col {e.offset}")
        corrected = autopep8.fix_code(code)  # Auto-format the user's input
        show_message("Here is the auto-formatted correction:", 'yellow')
        print(corrected)
    # Advance to next snippet regardless
    index += 1
    if index >= len(snippets):
        app.exit()
        return
    editor.text = ''  # Clear editor
    frame.title = f"Snippet {index+1} of {len(snippets)}"

@kb.add('c-c')  # Ctrl-C to quit
def _(event):
    app.exit()

def main():
    print("Type the loop code, then press Shift + @ to check. Ctrl-C to quit.")
    app.run()

if __name__ == '__main__':
    main()

