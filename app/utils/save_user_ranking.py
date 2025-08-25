
def save_user(username, password, name, surname):
    saved_user: dict = {
        "username": username,
        "password": password,
        "name": name,
        "surname": surname,
        "beers": {
            "cl33": 0,
            "cl50": 0,
            "jarra_caña": 0,
            "total_beers": 0
        }
    }
    return saved_user

def save_ranking(username):
    ranking_user: dict = {
        "username": username,
        "total_beers": 0
    }
    return ranking_user