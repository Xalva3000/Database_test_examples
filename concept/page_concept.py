from functools import total_ordering

from concept.book_concept import BookConcept


@total_ordering
class PageConcept:
    def __init__(self, page_num, text='', pk=None, book=None):
        self.page_num = page_num
        self.text = text
        self.pk = pk
        self.book: BookConcept = book

    def __eg__(self, other):
        if other.__class__ == self.__class__:
            return self.page_num == other.page_num

    def __gt__(self, other):
        if other.__class__ == self.__class__:
            return self.page_num > other.page_num

    def __str__(self):
        return f"{self.book}<{self.page_num}>"

    def __repr__(self):
        return f"Book<{self.book}>Page<{self.page_num}>"



