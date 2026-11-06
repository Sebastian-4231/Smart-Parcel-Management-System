class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class ParcelStack:
    def __init__(self):
        self.top = None

    # Push a new status onto the stack
    def push(self, status):
        new_node = StackNode(status)

        new_node.next = self.top
        self.top = new_node

    # Remove the latest status
    def pop(self):
        if self.top is None:
            print("Stack is empty.")
            return None

        status = self.top.data
        self.top = self.top.next

        return status

    # View the latest status without removing it
    def peek(self):
        if self.top is None:
            print("Stack is empty.")
            return None

        return self.top.data

    # Display all statuses
    def display(self):
        if self.top is None:
            print("No status history available.")
            return

        current = self.top

        print("\n--- Parcel Status History ---")

        while current is not None:
            print(current.data)
            current = current.next