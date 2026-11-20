class Auth:
    MAX_ATTEMPTS = 3

    def __init__(self, users):
        self.users = users  # {login: password}
        self.failed = {}
        self.locked = set()

    def login(self, user, password):
        if user in self.locked:
            return "locked"
        if self.users.get(user) == password:
            self.failed[user] = 0
            return "ok"
        self.failed[user] = self.failed.get(user, 0) + 1
        if self.failed[user] >= self.MAX_ATTEMPTS:
            self.locked.add(user)
            return "locked"
        return "wrong password"
