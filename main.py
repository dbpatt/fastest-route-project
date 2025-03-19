import heapq  # Min-Heap (Priority Queue) for Dijkstra's Algorithm

class FlightNetwork:
    """Graph-based airport network where nodes are airports and edges are flight routes with travel times."""

    def __init__(self):
        """Initializes an empty flight network using an adjacency list."""
        self.network = {}  # Dictionary where keys = airport codes, values = list of (destination, flight time)

    def add_airport(self, airport):
        """Adds an airport to the network."""
        if airport not in self.network:
            self.network[airport] = []
            print(f"Airport {airport} added.")
        else:
            print(f"Airport {airport} already exists.")

    def add_flight(self, origin, destination, time):
        """
        Adds a bidirectional flight route between two airports with a given flight time.
        - Airports must already exist in the network.
        - Time is measured in minutes.
        """
        if origin not in self.network or destination not in self.network:
            print("Error: Both airports must exist in the network.")
            return
        if time <= 0:
            print("Error: Flight time must be a positive integer.")
            return

        self.network[origin].append((destination, time))
        self.network[destination].append((origin, time))
        print(f"Flight added: {origin} ✈ {destination} ({time} min)")

    def find_fastest_route(self, start, destination):
        """
        Uses Dijkstra's Algorithm to find the fastest flight route between two airports.
        - A Min-Heap (Priority Queue) is used to always explore the shortest path first.
        """
        if start not in self.network or destination not in self.network:
            print("Error: Both airports must exist in the network.")
            return None

        # Min-Heap stores (travel time, airport) tuples
        min_heap = [(0, start)]  # Start with the origin airport (0 minutes)
        shortest_times = {airport: float('inf') for airport in self.network}  # Initialize all times as infinite
        shortest_times[start] = 0  # Set starting airport travel time to 0
        previous_airport = {}  # Tracks the path taken

        while min_heap:
            current_time, current_airport = heapq.heappop(min_heap)  # Get airport with the shortest travel time

            # If we reached the destination, reconstruct the path
            if current_airport == destination:
                path = []
                while current_airport in previous_airport:
                    path.append(current_airport)
                    current_airport = previous_airport[current_airport]
                path.append(start)
                path.reverse()
                print(f"Fastest route from {start} to {destination}: {' → '.join(path)} (Total Time: {shortest_times[destination]} min)")
                return path

            # Process all connecting flights
            for neighbor, flight_time in self.network[current_airport]:
                new_time = current_time + flight_time
                if new_time < shortest_times[neighbor]:  # If found a shorter route
                    shortest_times[neighbor] = new_time
                    previous_airport[neighbor] = current_airport
                    heapq.heappush(min_heap, (new_time, neighbor))  # Push updated time into heap

        print(f"No route found from {start} to {destination}.")
        return None

    def display_airport_network(self):
        """Displays all airports and their direct flight connections."""
        print("\nAirport Flight Network:")
        for airport, routes in self.network.items():
            connections = ', '.join([f"{dest} ({time} min)" for dest, time in routes])
            print(f"{airport} → {connections}")
