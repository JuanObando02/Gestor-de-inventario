class Category:
    def __init__(self, id_category, name, pasillo = None):
        self.id_category = id_category
        self.name = name
        self.pasillo = pasillo #Puede ser NULL

    def __repr__(self):
        return f"<Category {self.nombre} (Pasillo: {self.pasillo})>"
    