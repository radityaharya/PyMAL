from ..util import *


class User:
    def get_user(self):
        """
        > Get user info (@me)
        
        Returns:
            dict: User info.
        
        ---
        https://myanimelist.net/apiconfig/references/api/v2#tag/user
        """
        return self.api_call.request("GET", "users/@me")

    def get_user_anime_list(
        self,
        username: str = "@me",
        status: str = None,
        sort: str = None,
        limit: int = 100,
        offset: int = None,
    ) -> list:
        """
        > Get user anime list.

        Args:
            username (str): Username.
            status (str): Status.
            sort (str): Sort.
            limit (int): Limit.
            offset (int): Offset.

        Returns:
            list: List of user anime list.

        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/users_user_id_animelist_get
        """
        status_values = ["watching", "completed", "on_hold", "dropped", "plan_to_watch"]
        sort_values = [
            "list_score",
            "list_updated_at",
            "anime_title",
            "anime_start_date",
            "anime_id",
        ]

        if status is not None:
            if status not in status_values:
                raise ValueError(f"status must be one of {status_values}")
        if sort is not None:
            if sort not in sort_values:
                raise ValueError(f"sort must be one of {sort_values}")
        if limit > 1000:
            raise ValueError("limit must be less than or equal to 1000")
        return reform_json(self.api_call.request(
            "GET",
            f"users/{username}/animelist",
            params={"status": status, "sort": sort, "limit": limit, "offset": offset},
        ))

    def update_user_anime_list(
        self,
        anime_id: int,
        status: str = "watching",
        is_rewatching: bool = None,
        score: int = None,
        num_watched_episodes: int = 1,
        priority: int = None,
        num_times_rewatched: int = None,
        rewatch_value: int = None,
        tags: str = None,
        comments: str = None,
    ):
        """
        > Update user anime list. Only fields that are not None will be updated.

        Args:
            anime_id (int): Anime ID.
            status (str): Status.
            is_rewatching (bool): Is rewatching.
            score (int): Score (0-10).
            num_watched_episodes (int): Number of watched episodes.
            priority (int): Priority (1-2).
            num_times_rewatched (int): Number of times rewatched.
            rewatch_value (int): Rewatch value (1-5).
            tags (str): Tags.
            comments (str): Comments.

        Returns:
            dict: Updated user anime list.

        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_my_list_status_put
        """

        status_values = ["watching", "completed", "on_hold", "dropped", "plan_to_watch"]
        priority_values = [1, 2, None]
        rewatch_value_values = [1, 2, 3, 4, 5, None]
        if status not in status_values:
            raise ValueError(f"status must be one of {status_values}")
        if priority not in priority_values:
            raise ValueError(f"priority must be one of {priority_values}")
        if rewatch_value not in rewatch_value_values:
            raise ValueError(f"rewatch_value must be one of {rewatch_value_values}")
        if score is not None:
            if score < 0 or score > 10:
                raise ValueError(f"score must be between 0 and 10")
        if num_watched_episodes < 1:
            raise ValueError(f"num_watched_episodes must be greater than or equal to 1")
        if num_times_rewatched != None:
            if num_times_rewatched < 0:
                raise ValueError(f"num_times_rewatched must be greater than or equal to 0")
            
        data = {
            "status": status,
            "is_rewatching": is_rewatching,
            "score": score,
            "num_watched_episodes": num_watched_episodes,
            "priority": priority,
            "num_times_rewatched": num_times_rewatched,
            "rewatch_value": rewatch_value,
            "tags": tags,
            "comments": comments,
        }

        data = {k: v for k, v in data.items() if v is not None}

        return self.api_call.request(
            "PATCH", f"anime/{anime_id}/my_list_status", data=data
        )

    def delete_user_anime_list(self, anime_id: int)->list:
        """
        > Delete an anime from user anime list.

        Args:
            anime_id (int): Anime ID.

        Returns:
            list: Deleted user anime list.

        ---
        https://myanimelist.net/apiconfig/references/api/v2#operation/anime_anime_id_my_list_status_delete
        """
        return (self.api_call.request("DELETE", f"anime/{anime_id}/my_list_status"))
