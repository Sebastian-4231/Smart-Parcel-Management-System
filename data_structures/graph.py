class DeliveryGraph:
    def __init__(self):
        self.graph = {}
        self.display_names = {}
        self.aliases = {}

    @staticmethod
    def _normalize(location):
        if location is None:
            return ""
        return " ".join(str(location).strip().split()).lower()

    def add_alias(self, alias, canonical):
        norm_a = self._normalize(alias)
        norm_c = self._normalize(canonical)
        if norm_a and norm_c and norm_a != norm_c:
            canon = self.get_canonical(canonical) or canonical
            self.aliases[norm_a] = canon

    def get_canonical(self, location):
        norm = self._normalize(location)
        if not norm:
            return None
        if norm in self.display_names:
            return self.display_names[norm]
        if norm in self.aliases:
            canon = self.aliases[norm]
            return self.display_names.get(self._normalize(canon), canon)
        return None

    # Add a location to the graph
    def add_location(self, location):
        norm = self._normalize(location)
        if not norm:
            return None
        if norm in self.aliases:
            canon = self.aliases[norm]
            return self.display_names.get(self._normalize(canon), canon)
        if norm not in self.display_names:
            display = " ".join(str(location).strip().split())
            self.display_names[norm] = display
            self.graph[display] = []
        return self.display_names[norm]

    # Remove a location and all its incident routes safely
    def remove_location(self, location):
        canon = self.get_canonical(location)
        if canon and canon in self.graph:
            for neighbor in list(self.graph[canon]):
                if canon in self.graph.get(neighbor, []):
                    self.graph[neighbor].remove(canon)
            del self.graph[canon]
            norm = self._normalize(location)
            norm_c = self._normalize(canon)
            self.display_names.pop(norm, None)
            self.display_names.pop(norm_c, None)
            self.aliases = {a: c for a, c in self.aliases.items() if self._normalize(c) != norm_c and a != norm}
            return True
        return False

    # Add a route between two locations
    def add_route(self, location1, location2):
        norm1 = self._normalize(location1)
        norm2 = self._normalize(location2)
        if not norm1 or not norm2 or norm1 == norm2:
            return False

        c1 = self.add_location(location1)
        c2 = self.add_location(location2)

        # Prevent duplicate route insertion case-insensitively
        norm_c1 = self._normalize(c1)
        norm_c2 = self._normalize(c2)
        if norm_c1 == norm_c2:
            return False

        if not any(self._normalize(nbr) == norm_c2 for nbr in self.graph[c1]):
            self.graph[c1].append(c2)
        if not any(self._normalize(nbr) == norm_c1 for nbr in self.graph[c2]):
            self.graph[c2].append(c1)
        return True

    # Check if a direct route exists between two locations
    def has_route(self, location1, location2):
        c1 = self.get_canonical(location1)
        c2 = self.get_canonical(location2)
        if not c1 or not c2 or c1 not in self.graph:
            return False
        norm2 = self._normalize(c2)
        return any(self._normalize(nbr) == norm2 for nbr in self.graph[c1])

    # Display the graph
    def display(self):
        if not self.graph:
            print("No delivery locations available.")
            return

        print("\n--- Delivery Network ---")
        for location in self.graph:
            print(location, "->", ", ".join(self.graph[location]))

    # Breadth First Search (prints traversal and returns visited node list)
    def bfs(self, start):
        c_start = self.get_canonical(start)
        if not c_start or c_start not in self.graph:
            print("Location not found.")
            return []

        visited_norms = {self._normalize(c_start)}
        queue = [c_start]
        traversal = []

        print("\nBFS Traversal:")
        while queue:
            current = queue.pop(0)
            traversal.append(current)
            print(current, end=" ")

            for neighbour in self.graph.get(current, []):
                norm_nbr = self._normalize(neighbour)
                if norm_nbr not in visited_norms:
                    visited_norms.add(norm_nbr)
                    queue.append(neighbour)
        print()
        return traversal

    # Check if destination is reachable from source using BFS
    def is_reachable(self, source, destination):
        c_src = self.get_canonical(source)
        c_dest = self.get_canonical(destination)
        if not c_src or not c_dest or c_src not in self.graph or c_dest not in self.graph:
            return False

        norm_src = self._normalize(c_src)
        norm_dest = self._normalize(c_dest)
        if norm_src == norm_dest:
            return True

        visited_norms = {norm_src}
        queue = [c_src]

        while queue:
            current = queue.pop(0)
            if self._normalize(current) == norm_dest:
                return True
            for neighbour in self.graph.get(current, []):
                norm_nbr = self._normalize(neighbour)
                if norm_nbr not in visited_norms:
                    visited_norms.add(norm_nbr)
                    queue.append(neighbour)

        return False