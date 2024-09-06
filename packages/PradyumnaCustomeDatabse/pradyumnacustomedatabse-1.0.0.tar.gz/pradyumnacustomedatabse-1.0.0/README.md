# Notes Database Package

This package provides functionality to create, read, update, and delete notes in a simple database using Python's `pickle` module.

## Features

- Create new notes with a title and content.
- Edit and delete existing notes.
- Store notes persistently in a local file.

## Installation

You can install the package using:
pip install .

## Usage

```python
from notes_database import NotesDatabase

db = NotesDatabase()
db.create_note("12345", {"title": "My First Note", "content": "This is a note."})
notes = db.get_notes()
print(notes)
