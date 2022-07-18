import json

from flask import current_app as app, request
from flask_restx import Api, Namespace, Resource

from application.models import db
from application import models, schema
from application.utils import convert_and_register_model

api: Api = app.config['api']
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

movies_schema = schema.MovieSchema(many=True)
movie_schema = schema.MovieSchema()

director_schema = schema.DirectorSchema()
directors_schema = schema.DirectorSchema(many=True)

genre_schema = schema.GenreSchema()
genres_schema = schema.GenreSchema(many=True)

convert_and_register_model('movie', movie_schema)
convert_and_register_model('movies', movies_schema)
convert_and_register_model('director', director_schema)
convert_and_register_model('directors', directors_schema)
convert_and_register_model('genre', genre_schema)
convert_and_register_model('genres', genres_schema)


@movies_ns.route('/<int:movie_id>')
class MovieView(Resource):
    @movies_ns.response(200, description='Возвращает фильм по ID.', model=api.models['movie'])
    @movies_ns.response(404, description='Фильм не найден.')
    def get(self, movie_id):
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

        if movie is None:
            return None, 404

        return movie_schema.dump(movie), 200

    @movies_ns.response(200, description='Фильм обновлён.')
    @movies_ns.response(404, description='Неправильный ID фильма.')
    def put(self, movie_id):
        update_rows = db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)
        if update_rows != 1:
            return None, 400

        db.session.commit()
        return None, 204

    @movies_ns.response(204, description='Фильм удалён.')
    @movies_ns.response(404, description='Неправильный ID фильма.')
    def delete(self, movie_id):
        delete_rows = db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()
        if delete_rows != 1:
            return None, 400

        db.session.commit()

        return None, 204


@movies_ns.route('/')
class MoviesView(Resource):

    @movies_ns.response(200, description='Возвращает все фильмы.', model=api.models['movies'])
    def get(self):
        movies_query = db.session.query(models.Movie)

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    @movies_ns.expect(api.models['movie'])
    @movies_ns.response(200, description='Фильм успешно создан.')
    def post(self):

        movie = movie_schema.load(request.json)  # ??
        # request.json - падает с ошибкой, request.args - добавляет (null) пустые поля
        db.session.add(models.Movie(**movie))

        db.session.commit()

        return None, 201


@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):
    @directors_ns.response(200, description='Возвращает режиссеров по ID.', model=api.models['director'])
    @directors_ns.response(404, description='Режиссер не найден.')
    def get(self, director_id):
        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()

        if director is None:
            return None, 404

        return director_schema.dump(director), 200

    @directors_ns.response(200, description='Режиссер обновлён.')
    @directors_ns.response(404, description='Неправильный ID режиссера.')
    def put(self, director_id):
        update_rows = db.session.query(models.Director).filter(models.Director.id == director_id).update(request.json)
        if update_rows != 1:
            return None, 400

        db.session.commit()
        return None, 204

    @directors_ns.response(204, description='Режиссер удалён.')
    @directors_ns.response(404, description='Неправильный ID режиссера.')
    def delete(self, director_id):
        delete_rows = db.session.query(models.Director).filter(models.Director.id == director_id).delete()
        if delete_rows != 1:
            return None, 400

        db.session.commit()

        return None, 204


@directors_ns.route('/')
class DirectorsView(Resource):

    @directors_ns.response(200, description='Возвращает всех режиссеров.', model=api.models['directors'])
    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    @directors_ns.expect(api.models['director'])
    @directors_ns.response(200, description='Режиссер успешно добавлен.')
    def post(self):
        director = director_schema.load(request.args)  # ??

        db.session.add(models.Director(**director))

        db.session.commit()

        return None, 201


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):
    @genres_ns.response(200, description='Возвращает жанры по ID.', model=api.models['genre'])
    @genres_ns.response(404, description='Жанр не найден.')
    def get(self, genre_id):
        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()

        if genre is None:
            return None, 404

        return genre_schema.dump(genre), 200

    @genres_ns.response(200, description='Жанр обновлён.')
    @genres_ns.response(404, description='Неправильный ID жанра.')
    def put(self, genre_id):
        update_rows = db.session.query(models.Genre).filter(models.Genre.id == genre_id).update(request.json)
        if update_rows != 1:
            return None, 400

        db.session.commit()
        return None, 204

    @genres_ns.response(204, description='Жанр удалён.')
    @genres_ns.response(404, description='Неправильный ID жанра.')
    def delete(self, genre_id):
        delete_rows = db.session.query(models.Genre).filter(models.Genre.id == genre_id).delete()
        if delete_rows != 1:
            return None, 400

        db.session.commit()

        return None, 204


@genres_ns.route('/')
class GenresView(Resource):
    @genres_ns.response(200, description='Возвращает все жанры.', model=api.models['genres'])
    def get(self):
        genre = db.session.query(models.Genre).all()

        return genres_schema.dump(genre), 200

    @genres_ns.expect(api.models['genre'])
    @genres_ns.response(200, description='Жанр успешно добавлен.')
    def post(self):
        genre = genre_schema.load(request.args)  # ??

        db.session.add(models.Genre(**genre))

        db.session.commit()

        return None, 201
