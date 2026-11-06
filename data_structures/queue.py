
class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class ParcelQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    # Add a parcel to the queue
    def enqueue(self, parcel):
        new_node = QueueNode(parcel)

        if self.rear is None:
            self.front = new_node
            self.rear = new_node
            return

        self.rear.next = new_node
        self.rear = new_node

    # Remove the parcel from the front
    def dequeue(self):
        if self.front is None:
            print("Delivery queue is empty.")
            return None

        parcel = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return parcel

    # View the first parcel without removing it
    def peek(self):
        if self.front is None:
            print("Delivery queue is empty.")
            return None

        return self.front.data

    # Remove a specific parcel from anywhere in the queue
    def remove(self, parcel_id):
        current = self.front
        previous = None

        while current is not None:
            if str(current.data.parcel_id) == str(parcel_id):

                # Removing the front node
                if previous is None:
                    self.front = current.next
                else:
                    previous.next = current.next

                # If removing the rear node
                if current == self.rear:
                    self.rear = previous

                # Ensure both pointers are empty when queue is empty
                if self.front is None:
                    self.rear = None

                return True

            previous = current
            current = current.next

        return False

    # Check if a parcel is already in the queue
    def contains(self, parcel_id):
        current = self.front
        while current is not None:
            if str(current.data.parcel_id) == str(parcel_id):
                return True
            current = current.next
        return False

    # Display all parcels in the queue
    def display(self):
        if self.front is None:
            print("Delivery queue is empty.")
            return

        current = self.front
        print("\n--- Pending Delivery Queue ---")

        while current is not None:
            print(
                "Parcel ID:",
                current.data.parcel_id,
                "| Destination:",
                current.data.destination
            )
            current = current.next
