from concept.story_concept import StoryConcept


# BookID = type('Book', (object,), {'title': str, "author":str})

class BookConcept:
    def __init__(self, title, page_size=1050):
        self.title = title
        self.page_size = page_size
        self.stories = []
        self.pages: dict[int, str] = {}

    def append_story(self, story: StoryConcept):
        if isinstance(story, StoryConcept):
            self.stories.append(story)
        return f"{story.title} appended"

    def delete_story(self, title: StoryConcept):
        for index, story in self.stories:
            if story.title == title:
                del self.stories[index]
                return f"{story.title} deleted"

    def prepare(self):
        if self.stories:
            for story in self.stories:
                self.__sew_story(story.text)
            return f"{len(self.stories)} stories are sewn in."
        else:
            return f"No story to sew in."


    def __sew_story(self, text) -> None:
        indent = 0
        count = 1 if not self.pages else max(self.pages) + 1
        while indent < len(text):
            tpl = self._get_part_text(text, indent, self.page_size)
            if tpl[0]:
                self.pages[count] = tpl[0].lstrip()
                indent += tpl[1]
                count += 1
            else:
                break

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


