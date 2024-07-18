from database.abstractions.abc_repository import Repository


class StoryRepository(Repository):
    def create(self, values: dict):
        pass

    def get(self, id):
        pass

    def get_all(self):
        pass

    def update(self, id, new_obj: object, partial=False):
        pass

    def delete(self, id):
        pass
