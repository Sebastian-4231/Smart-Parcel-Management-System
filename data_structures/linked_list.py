class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class ParcelLinkedList:
    def __init__(self):
        self.head = None

    # Insert a parcel at the end of the linked list
    def insert(self, parcel):
        new_node = Node(parcel)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    # Delete a parcel using Parcel ID
    def delete(self, parcel_id):
        if self.head is None:
            print("No parcels available.")
            return

        # If the first parcel is the one to delete
        if str(self.head.data.parcel_id) == str(parcel_id):
            self.head = self.head.next
            print("Parcel deleted successfully.")
            return

        current = self.head

        while current.next is not None:

            if str(current.next.data.parcel_id) == str(parcel_id):
                current.next = current.next.next
                print("Parcel deleted successfully.")
                return

            current = current.next

        print("Parcel not found.")

    # Search for a parcel by ID
    def search(self, parcel_id):
        current = self.head

        while current is not None:

            if str(current.data.parcel_id) == str(parcel_id):
                return current.data

            current = current.next

        return None

    # Display all parcels
    def display(self):
        if self.head is None:
            print("No parcels available.")
            return

        current = self.head

        while current is not None:
            current.data.display()
            current = current.next