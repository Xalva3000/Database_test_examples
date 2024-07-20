
BookID = type('Book', (object,), {'title': str, "author":str})

print(BookID)


class BookConcept(BookID):
    def __init__(self, title, page_size=1050):
        self.title = title
        self.page_size = page_size
        self.stories = []
        self.pages: dict[int, str] = {}
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

    def _get_part_text(self, text, start, page_size):
        char_end = ',.!:;?'
        part = text[start:start + page_size]
        for i_b in range(-1, -len(part) - 1, -1):
            if part[i_b] in char_end:
                end = (start + page_size + i_b + 1) if (start + page_size + i_b + 1) <= len(text) else len(text)
                result = text[start:end]
                if result[-1] in char_end and result[-2] in char_end and result[-3] not in char_end:
                    result = self._get_part_text(text, start, page_size - 2)[0]
                return result, len(result)

    def prepare_book(self) -> None:
        indent = 0
        count = 1
        while indent < len(self.text):
            tpl = self._get_part_text(self.text, indent, self.page_size)
            if tpl[0]:
                self.pages[count] = tpl[0].lstrip()
                indent += tpl[1]
                count += 1
            else:
                break