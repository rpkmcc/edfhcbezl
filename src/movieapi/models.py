from sqlalchemy.orm import registry

mapper_registry = registry()

metadata = mapper_registry.metadata


class Movie:
    def __init__(self, movie_id: int, title: str, year: int):
        self.movie_id: int = movie_id
        self.title: str = title
        self.year: int = year


class Genre:
    def __init__(self, name: str):
        self.name: str = name


class Rating:
    def __init__(self, user_id: int, rating: float, timestamp: int):
        self.user_id: int = user_id
        self.rating: float = rating
        self.timestamp: int = timestamp
