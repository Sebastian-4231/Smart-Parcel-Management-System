class Hub:
    def __init__(self, hub_id, hub_name, location):
        self.hub_id = int(hub_id)
        self.hub_name = hub_name
        self.location = location

    def display(self):
        print(f"Hub ID: {self.hub_id} | Name: {self.hub_name} | Location: {self.location}")


class BSTNode:
    def __init__(self, hub):
        self.hub = hub
        self.left = None
        self.right = None


class HubBST:
    def __init__(self):
        self.root = None

    # Insert a delivery hub based on Hub ID
    def insert(self, hub):
        new_node = BSTNode(hub)
        if self.root is None:
            self.root = new_node
            return True

        current = self.root
        while True:
            if int(hub.hub_id) < int(current.hub.hub_id):
                if current.left is None:
                    current.left = new_node
                    return True
                current = current.left
            elif int(hub.hub_id) > int(current.hub.hub_id):
                if current.right is None:
                    current.right = new_node
                    return True
                current = current.right
            else:
                return False  # Duplicate Hub ID

    # Search for a hub by Hub ID
    def search(self, hub_id):
        try:
            target_id = int(hub_id)
        except (ValueError, TypeError):
            return None

        current = self.root
        while current is not None:
            curr_id = int(current.hub.hub_id)
            if target_id == curr_id:
                return current.hub
            elif target_id < curr_id:
                current = current.left
            else:
                current = current.right
        return None

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def _delete(self, node, hub_id):
        if node is None:
            return None

        curr_id = int(node.hub.hub_id)
        if hub_id < curr_id:
            node.left = self._delete(node.left, hub_id)
        elif hub_id > curr_id:
            node.right = self._delete(node.right, hub_id)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._find_min(node.right)
            node.hub = successor.hub
            node.right = self._delete(node.right, int(successor.hub.hub_id))
        return node

    def delete(self, hub_id):
        try:
            target_id = int(hub_id)
        except (ValueError, TypeError):
            return False

        if self.search(target_id) is None:
            return False
        self.root = self._delete(self.root, target_id)
        return True

    # Retrieve all hubs sorted by Hub ID via in-order traversal
    def get_inorder_hubs(self, node=None, is_root=True):
        if is_root:
            node = self.root
        if node is None:
            return []
        hubs = []
        if node.left:
            hubs.extend(self.get_inorder_hubs(node.left, is_root=False))
        hubs.append(node.hub)
        if node.right:
            hubs.extend(self.get_inorder_hubs(node.right, is_root=False))
        return hubs

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(f"{node.hub.hub_id} ({node.hub.hub_name})", end=" -> ")
            self.inorder(node.right)

    def display(self):
        if self.root is None:
            print("Delivery Hub BST is empty.")
            return
        print("\n--- Delivery Hub BST (Inorder Traversal) ---")
        self.inorder(self.root)
        print("END")
