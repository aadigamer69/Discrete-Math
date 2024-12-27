This project presents a simulation framework for optimizing autonomous robot navigation in a multi-layered warehouse environment using graph-based pathfinding and visualization. The warehouse is modeled as a 3D grid represented by a graph, where nodes denote locations and edges define valid paths. Obstacles and battery stations are incorporated to mimic real-world constraints and operational requirements.

The system integrates an A* pathfinding algorithm with a Manhattan distance heuristic to compute optimal paths for robots from their starting positions to user-defined destinations. Robots dynamically adjust their paths in response to low battery levels, re-routing to the nearest battery station for recharging. A simulation loop tracks and visualizes the movement of multiple robots, highlighting their paths, interactions, and task completion statuses.

The visualization component provides real-time feedback, displaying the warehouse layout, obstacles, battery stations, and robot positions using a graph representation. Users interact with the system by specifying robot destinations via node IDs, ensuring flexibility in task assignment.

This project demonstrates the practical application of graph theory, pathfinding algorithms, and resource management in a controlled environment, offering insights into warehouse automation and multi-robot coordination strategies.
