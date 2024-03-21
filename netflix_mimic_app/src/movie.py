from netflix_mimic_app.src.commons import send_request
class MoviesHandler:
    """
    A class to handle movies, including adding and deleting movies.
    """

    @send_request(request_type="post")
    def add_movies(
            self,
            language=None,
            number_of_movies=None

    ):
        """
            Add the specified number of movies.
            Parameters:
                language: str, optional (default=None)
                    The language of the movies to be added. If None, raises ValueError.
                number_of_movies: int, optional (default=None)
                    The number of movies to add. If None, raises ValueError.
            Returns:
                str: The relative URL for adding the movies with specified parameters.
                """
        # relative path to base url
        rel_url = "/movies/set_n_movies_availability_by_language/{}?number_of_movies={}" \
            .format(language, number_of_movies)

        if language is None or number_of_movies is None:
            raise ValueError("Please provide both language and number_of_movies.")

        return rel_url

    @send_request(request_type="delete")
    def delete_movies(
            self,
            language=None,
            number_of_movies=None
    ):
        """
        Delete the specified number of movies.

        Parameters:
            language: str, optional (default=None)
                The language of the movies to be deleted. If None, raises ValueError.
            number_of_movies: int, optional (default=None)
                The number of movies to delete. If None, raises ValueError.

        Returns:
            str: The relative URL for deleting the movies with specified parameters.
        """
        # relative path to base url
        rel_url = "/movies/delete_movies/{}?number_of_movies={}" \
            .format(language, number_of_movies)

        if language is None or number_of_movies is None:
            raise ValueError("Please provide both language and number_of_movies.")

        return rel_url
    @send_request(request_type='get')
    def get_random_avail_movie(self,language: str = 'english'):
        rel_url = "/movies/random_movie_by_language/?language={}".format(
            language
        )
        return rel_url

if __name__ == "__main__":
    a = MoviesHandler()
    # print(a.add_movies('english', 10))
    # print(a.delete_movies('english', 10))
    a = a.get_random_avail_movie('english')
    print(a)

