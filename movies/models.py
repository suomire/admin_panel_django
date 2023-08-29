import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import MyUserManager


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(TimeStampedMixin, UUIDMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"

        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Person(TimeStampedMixin, UUIDMixin):
    full_name = models.CharField(_('name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"

        verbose_name = _('Person')
        verbose_name_plural = _('Persons')


class Filmwork(TimeStampedMixin, UUIDMixin):
    class FilmworkTypes(models.TextChoices):
        TV_SHOW = _('tv_show')
        MOVIE = _('movie')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True)
    rating = models.FloatField(_('rating'), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    type = models.CharField(max_length=7, choices=FilmworkTypes.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through="PersonFilmwork")
    certificate = models.CharField(_('certificate'), max_length=512, blank=True)
    file_path = models.FileField(_('file'), blank=True, upload_to='movies/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "content\".\"film_work"

        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

        indexes = [
            models.Index(fields=['creation_date'], name='film_work_creation_date_idx'),
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"

        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='genre_film_work_idx')
        ]


class PersonFilmwork(UUIDMixin):
    class PersonRolesTypes(models.TextChoices):
        DIRECTOR = _('director')
        ACTOR = _('actor')
        WRITER = _('writer')

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', choices=PersonRolesTypes.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"

        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_idx')
        ]


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)


    # строка с именем поля модели, которая используется в качестве уникального идентификатора
    USERNAME_FIELD = 'login'
    
    # менеджер модели
    objects = MyUserManager()

    def __str__(self):
        return f'{self.email} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True