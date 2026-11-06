
def merge_sort_parcels(parcels):
    if len(parcels) <= 1:
        return parcels

    mid = len(parcels) // 2

    left_half = merge_sort_parcels(parcels[:mid])
    right_half = merge_sort_parcels(parcels[mid:])

    return merge(left_half, right_half)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_id = int(left[i].parcel_id)
        right_id = int(right[j].parcel_id)

        if left_id <= right_id:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result
