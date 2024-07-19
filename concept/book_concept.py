
BookID = type('Book', (object,), {'title': str, "author":str})

print(BookID)


class BookConcept(BookID):
    def __init__(self, title, author, page_size=1050):
        self.title = title
        self.author = author
        self.page_size = page_size
        self.stories = []
        self.book: dict[int, str] = {}
        self._file_path = None


    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value

    @file_path.deleter
    def file_path(self):
        self._file_path = None

