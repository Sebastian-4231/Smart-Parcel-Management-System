from models.parcel import Parcel
from data_structures.linked_list import ParcelLinkedList
from data_structures.stack import ParcelStack
from data_structures.queue import ParcelQueue
from data_structures.expression import evaluate_postfix
from data_structures.binary_tree import BinaryTree, TreeNode
from data_structures.bst import Hub, HubBST
from data_structures.graph import DeliveryGraph
from algorithms.searching import linear_search, get_parcels_from_linked_list
from algorithms.sorting import merge_sort_parcels
from algorithms.greedy import prioritize_parcels

RATE_PER_KG = 20.0


def main():
    parcel_list = ParcelLinkedList()
    delivery_queue = ParcelQueue()
    status_histories = {}
    hub_bst = HubBST()
    delivery_graph = DeliveryGraph()
    for h in [(201, "Kochi Hub", "Kochi"), (205, "Thrissur Hub", "Thrissur"), (210, "Palakkad Hub", "Palakkad"), (215, "Kozhikode Hub", "Kozhikode")]:
        hub_bst.insert(Hub(*h)); delivery_graph.add_location(h[1])
    delivery_graph.add_route("Kochi Hub", "Thrissur Hub")
    delivery_graph.add_route("Thrissur Hub", "Palakkad Hub")
    delivery_graph.add_route("Kochi Hub", "Kozhikode Hub")
    binary_tree = BinaryTree()

    while True:
        print("\n================================")
        print("          SMART PARCEL")
        print("================================")
        print("1. Add Parcel")
        print("2. Delete Parcel")
        print("3. Display All Parcels")
        print("4. Add Parcel to Delivery Queue")
        print("5. Process Next Parcel")
        print("6. Add Parcel Status")
        print("7. View Status History")
        print("8. Calculate Delivery Charge")
        print("9. Display Delivery Hubs (BST)")
        print("10. Search Delivery Hub using BST")
        print("11. Add Delivery Route")
        print("12. Display Delivery Network")
        print("13. BFS Traversal of Delivery Network")
        print("14. Binary Tree Traversals")
        print("15. Linear Search")
        print("16. Display Parcels Sorted by ID")
        print("17. Display Parcels by Delivery Priority")
        print("18. Exit")
        print("================================")

        choice = input("Enter your choice: ").strip()

        # 1. Add Parcel
        if choice == "1":
            parcel_id = input("Enter Parcel ID: ").strip()
            sender = input("Enter Sender Name: ").strip()
            receiver = input("Enter Receiver Name: ").strip()
            source = input("Enter Source: ").strip()
            destination = input("Enter Destination: ").strip()

            try:
                numeric_id = int(parcel_id)
                weight = float(input("Enter Weight (kg): "))
                if numeric_id <= 0 or weight <= 0: raise ValueError
            except ValueError:
                print("Invalid Parcel ID or weight. Both must be positive numbers.")
                continue

            priority = input("Enter Priority (High/Medium/Low): ").strip().title()
            if priority not in ("High", "Medium", "Low"):
                print("Invalid priority. Use High, Medium, or Low.")
                continue

            if parcel_list.search(numeric_id) is not None:
                print("Parcel ID already exists.")
                continue

            # Calculate delivery charge via postfix evaluation
            charge_result = evaluate_postfix(f"{weight} {RATE_PER_KG} *")
            delivery_charge = round(float(charge_result), 2) if charge_result is not None else round(weight * RATE_PER_KG, 2)

            parcel = Parcel(numeric_id, sender, receiver, source, destination, weight, priority, delivery_charge=delivery_charge)
            parcel_list.insert(parcel)
            delivery_graph.add_location(source)
            delivery_graph.add_location(destination)

            status_histories[numeric_id] = ParcelStack()
            status_histories[numeric_id].push("Created")
            print(f"Parcel added successfully with delivery charge: ₹{delivery_charge:.2f}")

        # 2. Delete Parcel
        elif choice == "2":
            parcel_id = input("Enter Parcel ID to delete: ").strip()
            existing_parcel = parcel_list.search(parcel_id)
            if existing_parcel is None:
                print("Parcel not found.")
            else:
                parcel_list.delete(existing_parcel.parcel_id)
                delivery_queue.remove(existing_parcel.parcel_id)
                status_histories.pop(existing_parcel.parcel_id, None)
                print("Parcel deleted successfully from Linked List and delivery queue.")

        # 3. Display All Parcels
        elif choice == "3":
            parcel_list.display()

        # 4. Add Parcel to Delivery Queue
        elif choice == "4":
            parcel_id = input("Enter Parcel ID: ").strip()
            parcel = parcel_list.search(parcel_id)
            if parcel is None:
                print("Parcel not found.")
            elif delivery_queue.contains(parcel.parcel_id):
                print(f"Parcel {parcel.parcel_id} is already in the delivery queue.")
            elif not delivery_graph.is_reachable(parcel.source, parcel.destination):
                print(f"Cannot dispatch: Destination '{parcel.destination}' is not reachable from Source '{parcel.source}'.")
            else:
                if parcel.status != "Ready for Dispatch":
                    parcel.status = "Ready for Dispatch"
                    if parcel.parcel_id not in status_histories: status_histories[parcel.parcel_id] = ParcelStack()
                    status_histories[parcel.parcel_id].push("Ready for Dispatch")
                delivery_queue.enqueue(parcel)
                print("Parcel added to delivery queue.")

        # 5. Process Next Parcel
        elif choice == "5":
            parcel = delivery_queue.dequeue()
            if parcel is not None:
                parcel.status = "Out for Delivery"
                if parcel.parcel_id not in status_histories:
                    status_histories[parcel.parcel_id] = ParcelStack()
                status_histories[parcel.parcel_id].push(parcel.status)
                print(f"\nParcel processed successfully.\nParcel ID: {parcel.parcel_id}\nStatus: {parcel.status}")

        # 6. Add Parcel Status
        elif choice == "6":
            parcel_id = input("Enter Parcel ID: ").strip()
            parcel = parcel_list.search(parcel_id)
            if parcel is None:
                print("Parcel not found.")
                continue
            status = input("Enter new status (Packed/Ready for Dispatch/Out for Delivery): ").strip()
            if not status:
                print("Status cannot be empty.")
                continue
            parcel.status = status
            if parcel.parcel_id not in status_histories:
                status_histories[parcel.parcel_id] = ParcelStack()
            status_histories[parcel.parcel_id].push(status)
            print("Status added successfully.")
            if status.lower() == "ready for dispatch":
                if not delivery_graph.is_reachable(parcel.source, parcel.destination):
                    print("Cannot dispatch: Destination is not reachable from Source in delivery network.")
                elif not delivery_queue.contains(parcel.parcel_id):
                    delivery_queue.enqueue(parcel)
                    print("Parcel automatically added to delivery queue.")
                else:
                    print("Parcel is already in the delivery queue.")

        # 7. View Status History
        elif choice == "7":
            parcel_id = input("Enter Parcel ID: ").strip()
            parcel = parcel_list.search(parcel_id)
            if parcel is None:
                print("Parcel not found.")
            elif parcel.parcel_id not in status_histories:
                print("No status history available for this parcel.")
            else:
                stack = status_histories[parcel.parcel_id]
                print(f"\nStatus History for Parcel ID: {parcel.parcel_id}")
                print(f"Top Status (Peek): {stack.peek()}")
                stack.display()
                if input("Pop top status from history stack? (y/n): ").strip().lower() == "y":
                    if stack.top and stack.top.next:
                        print(f"Safely popped: {stack.pop()}")
                    else:
                        print("Cannot pop initial 'Created' status.")

        # 8. Calculate Delivery Charge
        elif choice == "8":
            parcel_id = input("Enter Parcel ID: ").strip()
            parcel = parcel_list.search(parcel_id)
            if parcel is None:
                print("Parcel not found.")
                continue
            try:
                rate = float(input("Enter delivery rate per kg: "))
                if rate < 0:
                    print("Rate cannot be negative.")
                    continue
            except ValueError:
                print("Invalid rate.")
                continue

            expression = f"{parcel.weight} {rate} *"
            delivery_charge = evaluate_postfix(expression)
            if delivery_charge is not None:
                print(f"\n--- Delivery Charge ---\nParcel ID : {parcel.parcel_id}\nWeight    : {parcel.weight} kg\nRate      : ₹{rate} per kg\nCharge    : ₹{delivery_charge}")
            else:
                print("Unable to calculate delivery charge.")

        # 9. Display Delivery Hubs (BST)
        elif choice == "9":
            print("\n--- Delivery Hubs BST (In-Order) ---")
            hub_bst.display()

        # 10. Search Delivery Hub using BST
        elif choice == "10":
            hub_id = input("Enter Hub ID to search: ").strip()
            hub = hub_bst.search(hub_id)
            if hub is not None:
                print("\nDelivery Hub found using BST:")
                hub.display()
            else:
                print("Hub not found in BST.")

        # 11. Add Delivery Route
        elif choice == "11":
            loc1 = input("Enter first hub name: ").strip()
            loc2 = input("Enter second hub name: ").strip()
            hubs = {h.hub_name for h in hub_bst.get_inorder_hubs()}
            if not loc1 or not loc2 or loc1 == loc2:
                print("Invalid hub names or identical locations.")
            elif loc1 not in hubs or loc2 not in hubs:
                print("Both locations must be registered delivery hubs.")
            elif loc2 in delivery_graph.graph.get(loc1, []):
                print(f"Route between '{loc1}' and '{loc2}' already exists.")
            else:
                delivery_graph.add_route(loc1, loc2)
                print("Route added successfully.")

        # 12. Display Delivery Network
        elif choice == "12":
            delivery_graph.display()

        # 13. BFS Traversal of Delivery Network
        elif choice == "13":
            start = input("Enter starting location for BFS: ").strip()
            delivery_graph.bfs(start)

        # 14. Binary Tree Traversals
        elif choice == "14":
            binary_tree.root = TreeNode("Main Hub")
            binary_tree.root.left, binary_tree.root.right = TreeNode("Regional Hub A"), TreeNode("Regional Hub B")
            binary_tree.root.left.left, binary_tree.root.left.right = TreeNode("Hub 1"), TreeNode("Hub 2")
            binary_tree.root.right.left, binary_tree.root.right.right = TreeNode("Hub 3"), TreeNode("Hub 4")
            print("\n--- Delivery Center Hierarchy ---")
            print("\nInorder Traversal:"); binary_tree.inorder(binary_tree.root); print("END")
            print("\nPreorder Traversal:"); binary_tree.preorder(binary_tree.root); print("END")
            print("\nPostorder Traversal:"); binary_tree.postorder(binary_tree.root); print("END")

        # 15. Linear Search
        elif choice == "15":
            parcel_id = input("Enter Parcel ID to search: ").strip()
            parcels = get_parcels_from_linked_list(parcel_list)
            parcel = linear_search(parcels, parcel_id)
            if parcel is not None:
                print("\nParcel found using Linear Search:")
                parcel.display()
            else:
                print("Parcel not found using Linear Search.")

        # 16. Display Parcels Sorted by ID
        elif choice == "16":
            parcels = get_parcels_from_linked_list(parcel_list)
            sorted_parcels = merge_sort_parcels(parcels)
            if not sorted_parcels:
                print("No parcels available.")
            else:
                print("\n--- Parcels Sorted by ID ---")
                for p in sorted_parcels:
                    p.display()

        # 17. Display Parcels by Delivery Priority
        elif choice == "17":
            parcels = get_parcels_from_linked_list(parcel_list)
            prioritized = prioritize_parcels(parcels)
            if not prioritized:
                print("No parcels available.")
            else:
                print("\n--- Parcels by Delivery Priority ---")
                for p in prioritized:
                    print(f"Parcel ID: {p.parcel_id} | Priority: {p.priority} | Destination: {p.destination}")

        # 18. Exit
        elif choice == "18":
            print("Exiting Smart Parcel. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
