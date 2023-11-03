from .db import database


class Tag:

    pk: int
    name: str

    def __init__(self, name: str, pk: int | None = None) -> None:
        self.name = name

        if pk is None:
            existing_pk = database.get_tag(name=self.name)
            
            if existing_pk is not None:
                self.pk = existing_pk
            
            else:
                new_id = database.create_tag(name=self.name)
                self.pk = new_id
