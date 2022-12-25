from datetime import datetime
from ..util import *


class Anime:
    def __init__(self):
        pass

    def search_anime(self, query: str, limit: int = 10, offset: int = 0) -> list:
        """
        > Search for anime.

        Args:
            query (str): Search query.
            limit (int): Maximum number of results to return.
            offset (int): Offset of results to return.

        Returns:
            list: List of search results.

        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_get
        """
        return reform_json(
            self.api_call.request(
                "GET",
                "anime",
                params={
                    "q": query,
                    "limit": limit,
                    "offset": offset,
                    "fields": ",".join(self.anime_fields),
                },
            )
        )

    def get_anime_details(self, anime_id: int):
        """
        > Get anime details by ID.

        Args:
            anime_id (int): MAL Anime ID.

        Returns:
            dict: Anime details.

        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_get
        """
        params = {"fields": ",".join(self.anime_fields)}
        return self.api_call.request("GET", f"anime/{anime_id}", params=params)

    def get_anime_ranking(
        self, ranking_type: str = "all", limit: int = 10, offset: int = 0
    ) -> list:
        ranking_type_values = [
            "all",
            "airing",
            "upcoming",
            "tv",
            "ova",
            "movie",
            "special",
            "bypopularity",
            "favorite",
        ]
        if ranking_type not in ranking_type_values:
            raise ValueError(f"ranking_type must be one of {ranking_type_values}")
        params = {
            "ranking_type": ranking_type,
            "fields": ",".join(self.anime_fields),
            "limit": limit,
            "offset": offset,
        }
        return reform_json(self.api_call.request("GET", "anime/ranking", params=params))

    def get_seasonal_anime(
        self,
        season: str = None,
        year: int = None,
        sort: str = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list:
        """
        > Get seasonal anime.

        winter: January, February, March
        spring: April, May, June
        summer: July, August, September
        fall: October, November, December

        if season is None, returns current season,
        if year is None, returns current year

        Args:
            season (str): Season.
            year (int): Year.
            sort (str): Sort.
            limit (int): Maximum number of results to return.
            offset (int): Offset of results to return.

        Returns:
            list: List of seasonal anime.

        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_ranking_get
        """
        season_values = ["winter", "spring", "summer", "fall", None]
        sort_values = ["anime_score", "anime_num_list_users", None]
        if season not in season_values:
            raise ValueError(f"season must be one of {season_values}")
        if sort not in sort_values:
            raise ValueError(f"sort must be one of {sort_values}")

        if season is None:
            month = datetime.now().month
            if month in [1, 2, 3]:
                season = "winter"
            elif month in [4, 5, 6]:
                season = "spring"
            elif month in [7, 8, 9]:
                season = "summer"
            elif month in [10, 11, 12]:
                season = "fall"
        if year is None:
            year = datetime.now().year

        params = {
            "sort": sort,
            "limit": limit,
            "offset": offset,
            "fields": ",".join(self.anime_fields),
        }
        return reform_json(
            self.api_call.request("GET", f"anime/season/{year}/{season}", params=params)
        )

    def get_suggested_anime(self, limit: int = 10, offset: int = 0) -> list:
        """
        Returns suggested anime for the authorized user.

        If the user is new comer, this endpoint returns an empty list.
        
        Args:
            limit (int): Maximum number of results to return.
            offset (int): Offset of results to return.
        
        Returns:
            list: List of suggested anime.
        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_suggestions_get
        """
        params = {
            "limit": limit,
            "offset": offset,
            "fields": ",".join(self.anime_fields),
        }
        return reform_json(self.api_call.request("GET", "anime/suggestions", params=params))
