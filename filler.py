"""
Скрипт заполнения базы данных с помощью модуля Faker

"""

from random import randint

from database.queries import BookQuery, StoryQuery, PageQuery
from faker import Faker


def launch_filler():
    fake = Faker('ru_RU')
    fake.seed_instance(1)

    # Создание книг
    for _ in range(10):
        BookQuery.insert_book(author=fake.name(), title=fake.catch_phrase())

    # Все id книг
    all_book_ids = BookQuery.select_all_id()

    # Создание историй для книг
    for book_id in all_book_ids:
        for _ in range(randint(1, 3)):
            StoryQuery.insert_story(title=fake.street_title(), book_id=book_id)

    # Все id историй
    all_stories_ids = StoryQuery.select_all_id()

    # Создание страниц для историй
    for story_id in all_stories_ids:
        for _ in range(randint(1, 20)):
            PageQuery.insert_page(page_text=fake.text(), story_id=story_id)


if __name__ == '__main__':
    launch_filler()
