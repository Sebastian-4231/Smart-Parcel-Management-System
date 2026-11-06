from contextlib import redirect_stdout
from io import StringIO


class TreeNode:
    def __init__(self, data, hub_name="", location=""):
        self.data = data
        self.hub_name = hub_name
        self.location = location
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.data, end=" -> ")
            self.inorder(node.right)

    def preorder(self, node):
        if node is not None:
            print(node.data, end=" -> ")
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node):
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.data, end=" -> ")

    def get_traversal_list(self, traversal_type):
        out = StringIO()
        with redirect_stdout(out):
            if traversal_type == "inorder":
                self.inorder(self.root)
            elif traversal_type == "preorder":
                self.preorder(self.root)
            elif traversal_type == "postorder":
                self.postorder(self.root)
        val = out.getvalue().strip()
        return [int(x.strip()) for x in val.split("->") if x.strip()]


def build_sample_tree():
    tree = BinaryTree()
    tree.root = TreeNode(100, "Central Hub", "Kochi")
    tree.root.left = TreeNode(50, "West Hub", "Kozhikode")
    tree.root.right = TreeNode(150, "East Hub", "Thrissur")
    tree.root.left.left = TreeNode(25, "North Hub", "Kannur")
    tree.root.left.right = TreeNode(75, "South Hub", "Alappuzha")
    tree.root.right.left = TreeNode(125, "Mid Hub", "Palakkad")
    tree.root.right.right = TreeNode(175, "City Hub", "Bengaluru")
    return tree


SAMPLE_TREE_NODES = [
    {"hub_id": 100, "hub_name": "Central Hub", "location": "Kochi", "position": "Root Node (Level 0)"},
    {"hub_id": 50, "hub_name": "West Hub", "location": "Kozhikode", "position": "Left Child of 100 (Level 1)"},
    {"hub_id": 150, "hub_name": "East Hub", "location": "Thrissur", "position": "Right Child of 100 (Level 1)"},
    {"hub_id": 25, "hub_name": "North Hub", "location": "Kannur", "position": "Left Child of 50 (Level 2)"},
    {"hub_id": 75, "hub_name": "South Hub", "location": "Alappuzha", "position": "Right Child of 50 (Level 2)"},
    {"hub_id": 125, "hub_name": "Mid Hub", "location": "Palakkad", "position": "Left Child of 150 (Level 2)"},
    {"hub_id": 175, "hub_name": "City Hub", "location": "Bengaluru", "position": "Right Child of 150 (Level 2)"},
]

TRAVERSAL_EXPLANATIONS = {
    "inorder": {
        "title": "Inorder Traversal (Left → Root → Right)",
        "rule": "Visit the left subtree, then the root, then the right subtree.",
        "description": "In a binary tree, an inorder traversal first recursively processes all nodes in the left subtree, visits the current root node, and finally recursively processes the right subtree. In a Binary Search Tree hierarchy, this visits keys in ascending order."
    },
    "preorder": {
        "title": "Preorder Traversal (Root → Left → Right)",
        "rule": "Visit the root, then the left subtree, then the right subtree.",
        "description": "In a binary tree, a preorder traversal visits the root node first before descending into its subtrees. This top-down traversal is ideal for cloning trees, generating hierarchical listings, or serializing delivery network dispatch structures."
    },
    "postorder": {
        "title": "Postorder Traversal (Left → Right → Root)",
        "rule": "Visit the left subtree, then the right subtree, then the root.",
        "description": "In a binary tree, a postorder traversal visits all descendant nodes in the left and right subtrees before visiting their root parent. This bottom-up traversal is commonly used for deletion, freeing resources, and evaluating dependency trees."
    }
}