import networkx as nx
import matplotlib.pyplot as plt
import random

# Define warehouse dimensions (multi-layer grid)
layers, rows, cols = 2, 15, 20  # 2 layers, 15x20 grid
G = nx.Graph()

# Create multi-layer graph
for layer in range(layers):
    for row in range(rows):
        for col in range(cols):
            node = f"L{layer}_{row}-{col}"
            G.add_node(node)
            if col > 0:
                G.add_edge(node, f"L{layer}_{row}-{col-1}")
            if row > 0:
                G.add_edge(node, f"L{layer}_{row-1}-{col}")
            if layer > 0:
                G.add_edge(node, f"L{layer-1}_{row}-{col}")

# Define positions for visualization
node_positions = {
    node: (int(node.split('-')[1]), -int(node.split('_')[1].split('-')[0]) - int(node[1]) * (rows + 2))
    for node in G.nodes
}

# Add obstacles and battery stations
obstacles = random.sample(list(G.nodes), 50)
for obstacle in obstacles:
    G.remove_node(obstacle)

battery_stations = random.sample(list(G.nodes), 8)

# Generate node numbering
node_map = {node: i+1 for i, node in enumerate(G.nodes)}

# A* heuristic: Manhattan distance
def heuristic(node1, node2):
    x1, y1 = node_positions[node1]
    x2, y2 = node_positions[node2]
    return abs(x1 - x2) + abs(y1 - y2)

# Robot class with A* pathfinding
class Robot:
    def __init__(self, id, start, final_position, color):
        self.id = id
        self.position = start
        self.final_position = final_position
        self.completed = False
        self.battery = 100
        self.recharging = False
        self.color = color
        self.path = self.calculate_path(self.final_position)

    def calculate_path(self, destination):
        try:
            return nx.astar_path(G, source=self.position, target=destination, heuristic=heuristic)
        except nx.NetworkXNoPath:
            print(f"Robot {self.id} has no path to {destination}.")
            return []

    def move(self, occupied_nodes):
        if self.completed:
            return

        # Low battery rerouting
        if self.battery <= 10 and not self.recharging:
            nearest_battery = min(
                battery_stations,
                key=lambda station: nx.shortest_path_length(G, source=self.position, target=station),
            )
            self.path = self.calculate_path(nearest_battery)
            self.recharging = True

        # Recharge battery
        if self.position in battery_stations and self.recharging:
            self.battery = 100
            self.recharging = False
            self.path = self.calculate_path(self.final_position)

        # Move to next position
        if self.path:
            next_position = self.path[1] if len(self.path) > 1 else self.path[0]
            if next_position not in occupied_nodes:
                self.position = next_position
                self.path = self.path[1:]
                self.battery -= 5
            else:
                print(f"Robot {self.id} waiting at {self.position} (blocked).")

        # Task completion
        if self.position == self.final_position and not self.recharging:
            self.completed = True

# Overlay node numbers in the visualization
def draw_warehouse(step):
    plt.clf()
    nx.draw(G, pos=node_positions, node_size=10, node_color="lightblue", edge_color="gray", with_labels=False)

    # Draw node labels (numerical ID + node name)
    for node, (x, y) in node_positions.items():
        if node not in obstacles:
            plt.text(x, y, f"{node_map[node]}", fontsize=6, ha='center', color="darkblue")

    # Draw battery stations
    for station in battery_stations:
        x, y = node_positions[station]
        plt.plot(x, y, "o", markersize=8, color="gray", label="Battery Station")

    # Draw obstacles
    for obstacle in obstacles:
        if obstacle in node_positions:
            x, y = node_positions[obstacle]
            plt.plot(x, y, "s", markersize=10, color="black", label="Obstacle")

    # Draw robots
    for robot in robots:
        x, y = node_positions[robot.position]
        plt.plot(x, y, "o", markersize=8, label=f"Robot {robot.id}", color=robot.color)

    # Add legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize="small")

    plt.title(f"Warehouse Simulation - Step {step}")
    plt.pause(0.5)

# Print Node Map Table
print("Node Map:")
print(f"{'ID':<5}{'Node Name':<15}")
for node, node_id in node_map.items():
    print(f"{node_id:<5}{node:<15}")

# Robots with user-defined destinations
colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "brown", "cyan", "magenta", "gray"]
robots = []
for i in range(10):
    start_node = random.choice(list(G.nodes))
    while True:
        try:
            final_position_id = int(input(f"Enter final destination for Robot {i+1} (Node ID 1-{len(node_map)}): "))
            final_position = [node for node, node_id in node_map.items() if node_id == final_position_id][0]
            if final_position != start_node:
                break
            else:
                print("Final position cannot be the same as the start position. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Enter a valid Node ID.")
    robots.append(Robot(i, start_node, final_position, colors[i % len(colors)]))

# Simulation loop
step = 0
while not all(robot.completed for robot in robots):
    step += 1
    occupied_nodes = {robot.position for robot in robots if not robot.completed}
    for robot in robots:
        robot.move(occupied_nodes)
    draw_warehouse(step)

print("All robots completed their tasks.")
plt.show()
