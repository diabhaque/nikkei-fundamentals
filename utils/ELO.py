class EloRatingSystem:
    def __init__(self, k_factor=32, default_rating=1500, ratings={}):
        self.k_factor = k_factor
        self.default_rating = default_rating
        self.ratings = ratings  # Dictionary to store player ratings

    def add_player(self, player_id):
        if player_id not in self.ratings:
            self.ratings[player_id] = self.default_rating

    def get_rating(self, player_id):
        return self.ratings.get(player_id, self.default_rating)

    def expected_score(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def update_ratings(self, player_a_id, player_b_id, outcome):

        # Add players if they don't exist
        self.add_player(player_a_id)
        self.add_player(player_b_id)

        # Get current ratings
        rating_a = self.get_rating(player_a_id)
        rating_b = self.get_rating(player_b_id)

        # Calculate expected scores
        expected_a = self.expected_score(rating_a, rating_b)
        expected_b = self.expected_score(rating_b, rating_a)

        # Update ratings
        self.ratings[player_a_id] = rating_a + self.k_factor * (outcome - expected_a)
        self.ratings[player_b_id] = rating_b + self.k_factor * (
            (1 - outcome) - expected_b
        )

    def get_all_ratings(self):
        return self.ratings.copy()


def get_num_games(num_players):
    return int((num_players * (num_players - 1)) / 2)
