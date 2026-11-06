class Parcel:
    def __init__(
        self,
        parcel_id,
        sender,
        receiver,
        source,
        destination,
        weight,
        priority,
        delivery_charge=0.0
    ):
        self.parcel_id = parcel_id
        self.sender = sender
        self.receiver = receiver
        self.source = source
        self.destination = destination
        self.weight = weight
        self.priority = priority
        self.delivery_charge = delivery_charge
        self.status = "Created"

    def display(self):
        print("\n--- Parcel Details ---")
        print("Parcel ID   :", self.parcel_id)
        print("Sender      :", self.sender)
        print("Receiver    :", self.receiver)
        print("Source      :", self.source)
        print("Destination :", self.destination)
        print("Weight      :", self.weight, "kg")
        print("Priority    :", self.priority)
        print("Charge      : ₹", self.delivery_charge)
        print("Status      :", self.status)