from app.constants import CATEGORIES
from app.models import Genre, Application

for category in CATEGORIES:
    ids = []
    for genre in Genre.objects.filter(name=category):
        if Application.objects.filter(genreapplication__genre=genre).count():
            ids.append(genre.genre_id)
    if ids:
        print "'{category}' : {id}," .format(category=category, id=ids)