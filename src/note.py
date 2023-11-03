from .tag import Tag
from .db import database


class Note:

    pk: int | None
    text: str
    tags: list[Tag]

    def __init__(self, 
                 text: str, 
                 pk: int | None = None
            ) -> None:
        self.pk = pk
        self.text = text

    def save(self):
        if self.pk is None:
            return self._create()
        else:
            pass

    def _create(self):
        new_pk = database.create_note(text=self.text)
        self.pk = new_pk
