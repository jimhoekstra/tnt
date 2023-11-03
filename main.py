from src.note import Note
from src.tag import Tag


if __name__ == '__main__':
    note = Note(text='hello world!')
    note.save()
    print(note.pk)

    tag = Tag(name='python')
    print(tag.pk)
    