import tkinter as tk
import numpy as np

class TSPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TSP Solver - Greedy Best First Search")
        self.root.geometry("700x450")

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="lightgray", width=500, height=300)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=4, sticky="nsew")
        self.canvas.bind("<Button-1>", self.add_point)

        # Display Path and Total Distance
        self.table_frame = tk.Frame(self.root, bg="white", padx=10, pady=10)
        self.table_frame.grid(row=4, column=0, columnspan=2, sticky="ew")

        self.path_label = tk.Label(self.table_frame, text="Optimal Path:")
        self.path_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.distance_label = tk.Label(self.table_frame, text="Total Distance:")
        self.distance_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Solve and Clear Buttons
        self.solve_button = tk.Button(self.root, text="Find Optimal Path", command=self.solve_tsp, bg="green", fg="white")
        self.solve_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.root, text="Clear Points", command=self.clear_points, bg="red", fg="white")
        self.clear_button.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.points = []
        self.lines = []

    def add_point(self, event):
        x, y = event.x, event.y
        label = chr(65 + len(self.points))
        self.points.append((x, y))
        radius = 15  # Radius of the circle
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue")
        self.canvas.create_text(x, y, text=label, fill="white", font=("Arial", 10), anchor="center")

    def solve_tsp(self):
        if len(self.points) < 2:
            return

        # Calculate distances between points
        distance_matrix = np.zeros((len(self.points), len(self.points)))
        for i in range(len(self.points)):
            for j in range(i + 1, len(self.points)):
                distance_matrix[i, j] = distance_matrix[j, i] = np.sqrt(
                    (self.points[i][0] - self.points[j][0]) ** 2 +
                    (self.points[i][1] - self.points[j][1]) ** 2
                )

        # Start
        current_city = 0
        tour = [current_city]
        unvisited_cities = set(range(len(self.points)))
        unvisited_cities.remove(current_city)

        # Algorithm
        while unvisited_cities:
            nearest_index = min(unvisited_cities, key=lambda x: distance_matrix[current_city][x])
            tour.append(nearest_index)
            unvisited_cities.remove(nearest_index)
            current_city = nearest_index

        # Add the last step to return to the starting point
        tour.append(tour[0])

        # Draw path on canvas with distances
        for i in range(len(tour) - 1):
            x1, y1 = self.points[tour[i]]
            x2, y2 = self.points[tour[i + 1]]
            distance = distance_matrix[tour[i]][tour[i + 1]]

            # Draw line
            line = self.canvas.create_line(x1, y1, x2, y2, fill="purple", width=2)
            self.lines.append(line)

            # Display distance label
            label_x = (x1 + x2) / 2
            label_y = (y1 + y2) / 2
            distance_label = self.canvas.create_text(label_x, label_y, text=f"{distance:.2f}", fill="black")

            # Save line and distance label references for later deletion
            self.lines.append(line)
            self.lines.append(distance_label)

        # Display the path and total distance on the table
        path_str = " -> ".join([chr(65 + city) for city in tour])
        total_distance = self.total_distance(tour, distance_matrix)
        self.path_label.config(text="Optimal Path: " + path_str)
        self.distance_label.config(text="Total Distance: {:.2f}".format(total_distance))

    def total_distance(self, tour, distance_matrix):
        total_distance = sum(distance_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1))
        return total_distance

    def clear_points(self):
        self.canvas.delete("all")
        self.points = []
        for item in self.lines:
            self.canvas.delete(item)
        self.lines = []
        self.path_label.config(text="Optimal Path:")
        self.distance_label.config(text="Total Distance:")

if __name__ == "__main__":
    root = tk.Tk()
    app = TSPApp(root)
    root.mainloop()