class StoryConcept:


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

    def prepare_book(self, path: str) -> None:
        indent = 0
        count = 1
        with open(path, 'rt', encoding='UTF-8') as file_in:
            content = file_in.read()
        while indent < len(content):
            tpl = self._get_part_text(content, indent, self.page_size)
            if tpl[0]:
                self.book[count] = tpl[0].lstrip()
                indent += tpl[1]
                count += 1
            else:
                break