class StoryConcept:
    def __init__(self, author, title, text=None):
        self.title = title
        self.author = author
        self.text = text
        self._file_path = None

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        self._file_path = path

    @file_path.deleter
    def file_path(self):
        self._file_path = None

    def load_txt(self, path=None):
        source = self.file_path or path
        with open(source, 'r', encoding='utf-8') as file:
            # content = [line.strip() for line in file.readlines()]
            content = file.read()
        self.text = content

    def __str__(self):
        return f"{self.title}. {self.author}"
