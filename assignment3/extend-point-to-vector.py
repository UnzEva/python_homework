class Point:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def distance_to(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

class Vector(Point):
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

# Demonstration
if __name__ == "__main__":
    print("=== Point Demonstration ===")
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print(f"Point 1: {p1}")
    print(f"Point 2: {p2}")
    print(f"Are points equal? {p1 == p2}")
    print(f"Distance between points: {p1.distance_to(p2):.2f}")

    print("\n=== Vector Demonstration ===")
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print(f"Vector 1: {v1}")
    print(f"Vector 2: {v2}")
    v3 = v1 + v2
    print(f"Vector addition (v1 + v2): {v3}")

    print("\n=== Inheritance Check ===")
    print(f"Is Vector a subclass of Point? {issubclass(Vector, Point)}")
    print(f"Is v1 an instance of Point? {isinstance(v1, Point)}")