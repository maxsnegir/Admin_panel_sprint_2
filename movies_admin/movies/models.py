import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class BaseModel(models.Model):
    """ Базовый класс-миксин для наследования полей """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(BaseModel):
    """ Модель жанров """

    name = models.CharField(_('Название'), max_length=255, unique=True)
    description = models.TextField(_('Описание'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        db_table = "content\".\"genre"


class Person(BaseModel):
    """ Модель описывающая таблицу person """

    full_name = models.CharField(_("Полное имя"), max_length=255)
    birth_date = models.DateField(_("Дата рождения"), blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _("Персона")
        verbose_name_plural = _("Персоны")
        db_table = "content\".\"person"


class RoleType(models.TextChoices):
    DIRECTOR = 'director', _('Режиссёр')
    WRITER = 'writer', _('Сценарист')
    ACTOR = 'actor', _('Актёр')


class PersonFilmWork(models.Model):
    """ Модель описывающая связь меджду фильмом и персоной """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.CharField(_("Роль"), max_length=100, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'person', 'role'],
                                    name='film_work_person_role'),
        ]


class FilmWorkGenre(models.Model):
    """ Модель описывающая связь между фильмом и жанрами """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'],
                                    name='film_work_genre'),
        ]


class FilmWorkType(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('TV Show')


class FilmWork(BaseModel):
    """ Модель описывающая таблицу film_work """

    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    creation_date = models.DateField(_('Дата создания'), blank=True)
    certificate = models.TextField(_('Сертификат'), blank=True)
    file_path = models.FileField(_('Путь к файлу'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('Рейтинг'), validators=[MinValueValidator(0), MaxValueValidator(10)], blank=True)
    type = models.CharField(_('Тип'), max_length=20, choices=FilmWorkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmWorkGenre')
    person = models.ManyToManyField(Person, through='PersonFilmWork')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Фильм')
        verbose_name_plural = _('Фильмы')
        db_table = "content\".\"film_work"
