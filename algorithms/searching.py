def get_parcels_from_linked_list(parcel_list):
    parcels = []

    current = parcel_list.head

    while current is not None:
        parcels.append(current.data)
        current = current.next

    return parcels


def linear_search(parcels, parcel_id):
    for parcel in parcels:

        if str(parcel.parcel_id) == str(parcel_id):
            return parcel

    return None