
def prioritize_parcels(parcels):
    priority_order = {
        "high": 1,
        "medium": 2,
        "low": 3
    }

    return sorted(
        parcels,
        key=lambda parcel: priority_order.get(
            str(parcel.priority).strip().lower(),
            4
        )
    )

