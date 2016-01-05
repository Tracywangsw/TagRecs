from imdb import IMDb
ia = IMDb()

the_matrix = ia.get_movie('0114709')
# print the_matrix['director']

# for person in ia.search_person('Mel Gibson'):
#   print person.personID, person['name']
print the_matrix.keys()
print the_matrix.get('plot')
