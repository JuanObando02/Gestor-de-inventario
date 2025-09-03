class User:
    def __init__(self,id_user,username,password,role):
        self.id_user = id_user
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"User {self.username} ({self.role})"
    
    