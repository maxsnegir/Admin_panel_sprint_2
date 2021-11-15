import sqlite3
from contextlib import contextmanager
from typing import List

from sqlite_to_postgres.dataclasses_models import FilmWork, Genre, Person, FilmWorkGenre, PersonFilmWork


@contextmanager
def sqlite_connection(database_path: str):
    """ Контекстный менеджер для соединения с sqlite """

    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteLoader:
    """ Класс получения данных из базы SqlLite """

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def get_all_movies(self) -> List[FilmWork]:
        """ Получение всех фильмов из базы """

        query = """SELECT * FROM film_work"""
        return [FilmWork(**movie) for movie in self.cursor.execute(query)]

    def get_all_genres(self) -> List[Genre]:
        """ Получение всех жанров из базы """

        query = """SELECT * FROM genre"""
        return [Genre(**genre) for genre in self.cursor.execute(query)]

    def get_all_persons(self) -> List[Person]:
        """ Получение всех персон из таблицы person """

        query = """SELECT * FROM person"""
        return [Person(**person) for person in self.cursor.execute(query)]

    def get_all_genre_films(self) -> List[FilmWorkGenre]:
        """ Получение всех персон из таблицы genre_film_work """

        query = """SELECT * FROM genre_film_work"""
        return [FilmWorkGenre(**genre_film_work) for genre_film_work in self.cursor.execute(query)]

    def get_all_person_film_work(self) -> List[PersonFilmWork]:
        """ Получение всех персон из таблицы person_film_work """

        query = """SELECT * FROM person_film_work"""
        return [PersonFilmWork(**person_film_work) for person_film_work in self.cursor.execute(query)]

    def load_movies(self) -> dict:
        """ Возвращает словарь с данными из таблиц person, film_work, genre... """

        return {
            "film_work": self.get_all_movies(),
            "genre": self.get_all_genres(),
            "person": self.get_all_persons(),
            "genre_film_work": self.get_all_genre_films(),
            "person_film_work": self.get_all_person_film_work()
        }
