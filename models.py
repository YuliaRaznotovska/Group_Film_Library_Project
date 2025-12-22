from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(255), nullable=False)
    login = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(120), unique=True)
    phone_number = Column(String(50))
    additional_info = Column(String(255))
    birth_date = Column(Date)

    def __repr__(self):
        return f'<User {self.name!r}>'


class Actor(Base):
    __tablename__ = 'actor'
    id = Column(Integer, primary_key=True)
    actor_first_name = Column(String(50), nullable=False)
    actor_last_name = Column(String(255), nullable=False)
    birth_date = Column(Date)
    death_date = Column(Date)
    description = Column(String(255))

    films = relationship("Film", secondary="actor_film", back_populates="actors")


class ActorFilm(Base):
    __tablename__ = 'actor_film'
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('actor.id'))
    film_id = Column(Integer, ForeignKey('film.id'))


class Country(Base):
    __tablename__ = 'country'
    country_name = Column(String(255), primary_key=True, unique=True)

    films = relationship("Film", back_populates="country_selection")


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    film_id = Column(Integer, ForeignKey('film.id'), unique=True)
    grade = Column(Integer)
    description = Column(String(255))


class Film(Base):
    __tablename__ = 'film'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    poster = Column(String(255))
    description = Column(String(255))
    rating = Column(Integer)
    duration = Column(Integer, nullable=False)
    country = Column(String(255), ForeignKey('country.country_name'), nullable=False)
    added_info = Column(String(255), nullable=False)

    actors = relationship("Actor", secondary="actor_film", back_populates="films")

    genres = relationship("Genre", secondary="genre_film", back_populates="films")

    country_selection = relationship("Country", back_populates="films")

    def __repr__(self):
        return f'<Film {self.name!r}>'


class FilmList(Base):
    __tablename__ = 'film_list'
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey('film.id'), unique=True)
    list_id = Column(Integer, ForeignKey('list.id'), unique=True)


class Genre(Base):
    __tablename__ = 'genre'
    genre = Column(String(255), primary_key=True, nullable=False)

    films = relationship("Film", secondary="genre_film", back_populates="genres")

    def __repr__(self):
        return f'<Genre {self.genre!r}>'


class GenreFilm(Base):
    __tablename__ = 'genre_film'
    id = Column(Integer, primary_key=True)
    genre_id = Column(String(255), ForeignKey('genre.genre'))
    film_id = Column(Integer, ForeignKey('film.id'))


class List(Base):
    __tablename__ = 'list'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
