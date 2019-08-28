"""CSC108 A3 recommender starter code."""

from typing import TextIO, List, Dict

from recommender_constants import (MovieDict, Rating, UserRatingDict, 
                                   MovieUserDict)
from recommender_constants import (MOVIE_FILE_STR, RATING_FILE_STR,
                                   MOVIE_DICT_SMALL, USER_RATING_DICT_SMALL,
                                   MOVIE_USER_DICT_SMALL)

############## HELPER FUNCTIONS

def get_similarity(user1: Rating, user2: Rating) -> float:
    """Return the a similarity score between user1 and user2 based on their
    movie ratings. The returned similarity score is a number between 0 and 1
    inclusive. The higher the number, the more similar user1 and user2 are.

    For those who are curious, this type of similarity measure is called the
    "cosine similarity".

    >>> r1 = {1: 4.5, 2: 3.0, 3: 1.0}
    >>> r2 = {2: 4.5, 3: 3.5, 4: 1.5, 5: 5.0}
    >>> s1 = get_similarity(r1, r1)
    >>> abs(s1 - 1.0) < 0.0001 # s1 is close to 1.0
    True
    >>> s2 = get_similarity(r1, {6: 4.5})
    >>> abs(s2 - 0.0) < 0.0001 # s2 is close to 0.0
    True
    >>> round(get_similarity(r1, r2), 2)
    0.16
    """
    shared = 0.0
    for m_id in user1:
        if m_id in user2:
            shared += user1[m_id] * user2[m_id]
    norm1 = 0.0
    for m_id in user1:
        norm1 = norm1 + user1[m_id] ** 2
    norm2 = 0.0
    for m_id in user2:
        norm2 = norm2 + user2[m_id] ** 2
    return (shared * shared) / (norm1 * norm2)






############## STUDENT HELPER FUNCTIONS


def sort_dict(candidate_movies: List[int], 
              similar_users_to_movies: Dict[int, List[int]],
              similar_users: Dict[int, float], 
              movie_users: Dict[int, List[int]]) -> Dict[int, List[int]]:
    '''Return a dictionary where the keys are the contribution score and the 
    value is an ascending list of movie IDs. 
    '''

    score_to_movie_dict = {}
    
    for user in similar_users_to_movies:
    #for movie in candidate_movies:
        for movie in (candidate_movies and similar_users_to_movies[user]):
            #for user in similar_users_to_movies:
            c = 0
            c += (similar_users[user] / (len(similar_users_to_movies[user]) * 
                                         len(movie_users[movie])))

            if movie not in score_to_movie_dict:
                score_to_movie_dict[movie] = [c]

            else:
                score_to_movie_dict[movie].append(c)
        #score_to_movie_dict[c].sort()
        
        #dict{ movie_id : List[scores] } 
    
    
    for i in score_to_movie_dict:
        scores = score_to_movie_dict[i]
        movies_score = 0
        for num in scores:
            movies_score += num
        score_to_movie_dict[i] = movies_score
        # dict{movie_id : total score }
    
    end = len(score_to_movie_dict) - 1
    while end != 0:
        for index in range(end):
            if score_to_movie_dict[index] > score_to_movie_dict[index + 1]:
                score_to_movie_dict[index], score_to_movie_dict[index + 1] = score_to_movie_dict[index + 1], score_to_movie_dict[index]
        end = end - 1
        
        
        
    score_to_movie_dict = dict(sorted(score_to_movie_dict.items(), reverse=True))
        # sorts the keys in a dictionary from highest to lowest key
        
    ##for item in score_to_movie_dict:
      ##  score_to_movie_dict[item].sort()
        

    return score_to_movie_dict     



############## STUDENT FUNCTIONS

def read_movies(movie_file: TextIO) -> MovieDict:
    """Return a dictionary containing movie id to (movie name, movie genres)
    in the movie_file.

    >>> movfile = open('movies_tiny.csv')
    >>> movies = read_movies(movfile)
    >>> movfile.close()
    >>> 68735 in movies
    True
    >>> movies[124057]
    ('Kids of the Round Table', [])
    >>> len(movies)
    4
    >>> movies == MOVIE_DICT_SMALL
    True
    """
    movie_dict = {}
    
    movie_file.readline()
    
    for line in movie_file.readlines():
        movie_info = line.strip('\n').split(',')
        # list of movie info
        value_tuple = (movie_info[1], movie_info[4:])
        movie_dict[int(movie_info[0])] = value_tuple
    return movie_dict




def read_ratings(rating_file: TextIO) -> UserRatingDict:
    """Return a dictionary containing user id to {movie id: ratings} for the
    collection of user movie ratings in rating_file.

    >>> rating_file = open('ratings_tiny.csv')
    >>> ratings = read_ratings(rating_file)
    >>> rating_file.close()
    >>> len(ratings)
    2
    >>> ratings[1]
    {2968: 1.0, 3671: 3.0}
    >>> ratings[2]
    {10: 4.0, 17: 5.0}
    """
    
    user_rating = {}

    rating_file.readline()
    
    for line in rating_file.readlines():
        rating = {}
        rating_info = line.strip('\n').split(',')
        movie_id = int(rating_info[1])
        movie_rating = float(rating_info[2])
        user_id = int(rating_info[0])
        rating[movie_id] = movie_rating       
        
        if user_id in user_rating:
            user_rating[user_id][movie_id] = movie_rating
        else:
            user_rating[user_id] = rating   
            
    return user_rating
            

def remove_unknown_movies(user_ratings: UserRatingDict, 
                          movies: MovieDict) -> None:
    """Modify the user_ratings dictionary so that only movie ids that are in the
    movies dictionary is remaining. Remove any users in user_ratings that have
    no movies rated.

    >>> small_ratings = {1001: {68735: 5.0, 302156: 3.5, 10: 4.5}, 1002: {11: 3.0}}
    >>> remove_unknown_movies(small_ratings, MOVIE_DICT_SMALL)
    >>> len(small_ratings)
    1
    >>> small_ratings[1001]
    {68735: 5.0, 302156: 3.5}
    >>> 1002 in small_ratings
    False
    """
    
    movies_to_remove = [] 
    for user in user_ratings:
        for movie in user_ratings[user]:
            if movie not in movies:
                movies_to_remove.append(movie)
    # made a list of movies to be removed
    
    for movie_item in movies_to_remove:
        for key in user_ratings:
            if movie_item in user_ratings[key]:
                del user_ratings[key][movie_item]
                # delete movie in user
    
    users_to_remove = []
    for user_item in user_ratings:
        if user_ratings[user_item] == {}:
            users_to_remove.append(user_item)
    # made a list of users that have an empty dictionary value
             
    
    for user_item in users_to_remove:
        del user_ratings[user_item]
    # remove each user_item in user_ratings
        
                


def movies_to_users(user_ratings: UserRatingDict) -> MovieUserDict:
    """Return a dictionary of movie ids to list of users who rated the movie,
    using information from the user_ratings dictionary of users to movie
    ratings dictionaries.

    >>> result = movies_to_users(USER_RATING_DICT_SMALL)
    >>> result == MOVIE_USER_DICT_SMALL
    True
    """
    movie_dict = {}
    
    for user_id in user_ratings:
        movie_id = user_ratings[user_id]
        for entry in movie_id:
            if entry not in movie_dict:
                movie_dict[entry] = [user_id]
                # make a new key with new list value
            else:
                movie_dict[entry].append(user_id)
                # add onto the key's list value
                
    return movie_dict



def get_users_who_watched(movie_ids: List[int],
                          movie_users: MovieUserDict) -> List[int]:
    """Return the list of user ids in movie_users who watched at least one
    movie in movie_ids.

    >>> get_users_who_watched([293660], MOVIE_USER_DICT_SMALL)
    [2]
    >>> lst = get_users_who_watched([68735, 302156], MOVIE_USER_DICT_SMALL)
    >>> len(lst)
    2
    """
    
    user_list = []
    for movie in movie_ids:
        if movie in movie_users.keys():
            user_ids = movie_users[movie]
            for item in user_ids:
                if item not in user_list:
                    user_list.append(item)
    return user_list
            


def get_similar_users(target_rating: Rating, user_ratings: UserRatingDict,
                      movie_users: MovieUserDict) -> Dict[int, float]:
    """Return a dictionary of similar user ids to similarity scores between the
    similar user's movie rating in user_ratings dictionary and the
    target_rating. Only return similarites for similar users who has at least
    one rating in movie_users dictionary that appears in target_Ratings.

    >>> sim = get_similar_users({293660: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL)
    >>> len(sim)
    1
    >>> round(sim[2], 2)
    0.86
    """
    movie_ids = []
    return_dict = {}
    
    for item in target_rating:
        movie_ids.append(item)
    # a list of movies the target user watched
        
    user_list = get_users_who_watched(movie_ids, movie_users)
    
    for user in user_list:
        return_dict[user] = get_similarity(target_rating, user_ratings[user])
        # get_similiarity gives similiarity score 
    return return_dict


def recommend_movies(target_rating: Rating,
                     user_ratings: UserRatingDict,
                     movie_users: MovieUserDict,
                     num_movies: int) -> List[int]:
    """Return a list of num_movies movie id recommendations for a target user 
    with target_rating of previous movies. The recommendations are based on
    movies and "similar users" data from the user_ratings / movie_users 
    dictionaries.

    >>> recommend_movies({302156: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [68735]
    >>> recommend_movies({68735: 4.5}, USER_RATING_DICT_SMALL, MOVIE_USER_DICT_SMALL, 2)
    [302156, 293660]
    """

    
    similar_users = get_similar_users(target_rating, user_ratings, movie_users)
    
    similar_users_to_movies = {}
    candidate_movies = []
    for user in similar_users:
        l = [] 
        # accumulator for movies similar users watched
        movie_dict = user_ratings[user]
        # dict{ movie_id : rating }
        for movie in movie_dict:
            if movie not in target_rating and movie_dict[movie] >= 3.5:
                    l.append(movie)
                    # make a list of candidate movies that the similar users watched
                    if movie not in candidate_movies:
                        candidate_movies.append(movie)
        if l != []:   
            similar_users_to_movies[user] = l
            # ensures no empty list is being added into the dictionary
            # assign users as keys and candidate movie list as the value in dict

    score_to_movie = sort_dict(candidate_movies, similar_users_to_movies, 
                               similar_users, movie_users)

                    
    recommended_list = [] 
    for score_value in score_to_movie:
        for movie_item in score_to_movie[score_value]: 
        # gives movie_list
            recommended_list.append(movie_item)
        
   
    return recommended_list[:num_movies]
        
        

            
        
        


if __name__ == '__main__':
    """Uncomment to run doctest"""
    import doctest
    doctest.testmod()
