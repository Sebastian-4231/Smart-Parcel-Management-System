from contextlib import redirect_stdout
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, flash

from models.parcel import Parcel
from data_structures.linked_list import ParcelLinkedList
from data_structures.queue import ParcelQueue
from data_structures.stack import ParcelStack
from data_structures.bst import Hub, HubBST
from data_structures.graph import DeliveryGraph
from data_structures.expression import evaluate_postfix
from algorithms.searching import linear_search, get_parcels_from_linked_list
from algorithms.sorting import merge_sort_parcels
from algorithms.greedy import prioritize_parcels
from data_structures.binary_tree import build_sample_tree, SAMPLE_TREE_NODES, TRAVERSAL_EXPLANATIONS

app = Flask(__name__)
app.secret_key = "smart-parcel-demo-key"
RATE_PER_KG = 20.0

parcel_list = ParcelLinkedList()
delivery_queue = ParcelQueue()
hub_bst = HubBST()
status_histories = {}
delivery_graph = DeliveryGraph()

for h in [(201, "Kochi Hub", "Kochi"), (205, "Thrissur Hub", "Thrissur"), (210, "Palakkad Hub", "Palakkad"), (215, "Kozhikode Hub", "Kozhikode")]:
    hub_bst.insert(Hub(*h)); delivery_graph.add_location(h[1]); delivery_graph.add_alias(h[2], h[1])
for r in [("Kochi Hub", "Thrissur Hub"), ("Thrissur Hub", "Palakkad Hub"), ("Kochi Hub", "Kozhikode Hub")]: delivery_graph.add_route(*r)

def run_bfs_traversal(start_loc):
    canon = delivery_graph.get_canonical(start_loc)
    if not canon or canon not in delivery_graph.graph: return None
    out = StringIO()
    with redirect_stdout(out): res = delivery_graph.bfs(canon)
    return res if res else None

@app.route("/")
def dashboard():
    parcels = get_parcels_from_linked_list(parcel_list)
    pending, curr = 0, delivery_queue.front
    while curr: pending += 1; curr = curr.next
    high = sum(1 for p in parcels if str(p.priority).strip().lower() == "high")
    return render_template("index.html", total_parcels=len(parcels), pending_count=pending, high_priority_count=high, total_hubs=len(hub_bst.get_inorder_hubs()))

@app.route("/parcels")
def parcels_page():
    parcels = get_parcels_from_linked_list(parcel_list)
    search_id = request.args.get("search", "").strip()
    if search_id: parcels = [p for p in parcels if str(p.parcel_id) == search_id]
    return render_template("parcels.html", parcels=parcels, search_id=search_id, delivery_queue=delivery_queue)

@app.route("/parcels/add", methods=["POST"])
def add_parcel():
    pid_str, sender, receiver = request.form.get("parcel_id", "").strip(), request.form.get("sender", "").strip(), request.form.get("receiver", "").strip()
    source, dest, priority = request.form.get("source", "").strip(), request.form.get("destination", "").strip(), request.form.get("priority", "").strip().title()
    try:
        weight, pid = float(request.form.get("weight", "")), int(pid_str)
        if weight <= 0 or pid <= 0 or not all([pid_str, sender, receiver, source, dest]) or priority not in ("High", "Medium", "Low"):
            raise ValueError
    except ValueError:
        flash("Please provide valid positive values and all required fields.", "danger")
        return redirect(url_for("parcels_page"))

    if parcel_list.search(pid) is not None:
        flash("This Parcel ID already exists.", "danger")
        return redirect(url_for("parcels_page"))

    charge = evaluate_postfix(f"{weight} {RATE_PER_KG} *")
    del_charge = round(float(charge), 2) if charge is not None else round(weight * RATE_PER_KG, 2)
    parcel = Parcel(pid, sender, receiver, source, dest, weight, priority, delivery_charge=del_charge)
    parcel_list.insert(parcel)
    delivery_graph.add_location(source); delivery_graph.add_location(dest)
    status_histories[pid] = ParcelStack(); status_histories[pid].push("Created")
    flash(f"Parcel {pid} added successfully. Delivery charge: ₹{del_charge:.2f}", "success")
    return redirect(url_for("parcels_page"))

@app.route("/parcels/delete/<int:parcel_id>", methods=["POST"])
def delete_parcel(parcel_id):
    if parcel_list.search(parcel_id):
        parcel_list.delete(parcel_id); delivery_queue.remove(parcel_id); status_histories.pop(parcel_id, None)
        flash("Parcel deleted successfully.", "success")
    else: flash("Parcel not found.", "danger")
    return redirect(url_for("parcels_page"))

@app.route("/hubs")
def hubs_page():
    sid = request.args.get("search_id", "").strip()
    return render_template("hubs.html", hubs=hub_bst.get_inorder_hubs(), searched_hub=hub_bst.search(sid) if sid else None, search_id=sid)

@app.route("/hubs/add", methods=["POST"])
def add_hub():
    hid, name, loc = request.form.get("hub_id", "").strip(), request.form.get("hub_name", "").strip(), request.form.get("location", "").strip()
    try:
        num_id = int(hid)
        if num_id <= 0 or not name or not loc: raise ValueError
    except ValueError:
        flash("Valid positive Hub ID, name, and location required.", "danger")
        return redirect(url_for("hubs_page"))
    if not hub_bst.insert(Hub(num_id, name, loc)):
        flash(f"Hub ID {num_id} already exists in BST.", "danger")
    else:
        delivery_graph.add_location(name); delivery_graph.add_alias(loc, name)
        flash(f"Hub {num_id} ({name}) registered into BST and added to Delivery Network. Connect routes in Network section.", "success")
    return redirect(url_for("hubs_page"))

@app.route("/hubs/delete/<int:hub_id>", methods=["POST"])
def delete_hub(hub_id):
    hub = hub_bst.search(hub_id)
    if not hub: flash(f"Hub {hub_id} not found in BST.", "danger")
    else:
        hname = hub.hub_name
        if hub_bst.delete(hub_id):
            delivery_graph.remove_location(hname)
            flash(f"Hub {hub_id} ({hname}) and its connected routes removed from network.", "success")
        else: flash(f"Hub {hub_id} not found in BST.", "danger")
    return redirect(url_for("hubs_page"))

@app.route("/queue")
def queue_page():
    parcels, curr = [], delivery_queue.front
    while curr: parcels.append(curr.data); curr = curr.next
    return render_template("queue.html", parcels=parcels)

@app.route("/queue/add/<int:parcel_id>", methods=["POST"])
def add_to_queue(parcel_id):
    parcel = parcel_list.search(parcel_id)
    if not parcel: flash("Parcel not found.", "danger")
    elif delivery_queue.contains(parcel_id): flash(f"Parcel {parcel_id} is already in the delivery queue.", "warning")
    elif not delivery_graph.is_reachable(parcel.source, parcel.destination):
        flash(f"Cannot dispatch: Destination '{parcel.destination}' is not reachable from Source '{parcel.source}'.", "warning")
    else:
        if parcel.status != "Ready for Dispatch":
            parcel.status = "Ready for Dispatch"
            if parcel.parcel_id not in status_histories: status_histories[parcel.parcel_id] = ParcelStack()
            status_histories[parcel.parcel_id].push("Ready for Dispatch")
        delivery_queue.enqueue(parcel)
        flash(f"Parcel {parcel_id} added to delivery queue.", "success")
    return redirect(url_for("parcels_page"))

@app.route("/queue/process", methods=["POST"])
def process_next():
    parcel = delivery_queue.dequeue()
    if parcel is None: flash("The delivery queue is empty.", "warning")
    else:
        parcel.status = "Out for Delivery"
        if parcel.parcel_id not in status_histories: status_histories[parcel.parcel_id] = ParcelStack()
        status_histories[parcel.parcel_id].push(parcel.status)
        flash(f"Parcel {parcel.parcel_id} is now out for delivery.", "success")
    return redirect(url_for("queue_page"))

@app.route("/queue/remove/<int:parcel_id>", methods=["POST"])
def remove_from_queue(parcel_id):
    flash(f"Parcel {parcel_id} removed from queue." if delivery_queue.remove(parcel_id) else "Parcel not found in queue.", "success" if parcel_id else "warning")
    return redirect(url_for("queue_page"))

@app.route("/status")
def status_page():
    parcels = get_parcels_from_linked_list(parcel_list)
    selected_id = request.args.get("parcel_id", "").strip()
    history, top_status = [], None
    if selected_id:
        parcel = parcel_list.search(selected_id)
        if parcel and parcel.parcel_id in status_histories:
            stack = status_histories[parcel.parcel_id]
            top_status, curr = stack.peek(), stack.top
            while curr: history.append(curr.data); curr = curr.next
    return render_template("status.html", parcels=parcels, selected_id=selected_id, history=history, top_status=top_status)

@app.route("/status/update", methods=["POST"])
def update_parcel_status():
    parcel_id, status = request.form.get("parcel_id", "").strip(), request.form.get("status", "").strip()
    parcel = parcel_list.search(parcel_id)
    if not parcel:
        flash("Parcel not found.", "danger")
        return redirect(url_for("status_page"))
    if status not in ("Packed", "Ready for Dispatch", "Out for Delivery"):
        flash("Please select a valid status.", "danger")
        return redirect(url_for("status_page"))
    if status == "Ready for Dispatch" and not delivery_graph.is_reachable(parcel.source, parcel.destination):
        flash(f"Cannot dispatch: Destination '{parcel.destination}' not reachable from '{parcel.source}'.", "warning")
        return redirect(url_for("status_page", parcel_id=parcel.parcel_id))

    if parcel.parcel_id not in status_histories:
        status_histories[parcel.parcel_id] = ParcelStack(); status_histories[parcel.parcel_id].push("Created")
    parcel.status = status; status_histories[parcel.parcel_id].push(status)
    msg = f"Status '{status}' pushed onto history Stack for parcel {parcel.parcel_id}."
    if status == "Ready for Dispatch":
        if not delivery_queue.contains(parcel.parcel_id):
            delivery_queue.enqueue(parcel); msg += f" Added parcel {parcel.parcel_id} to queue."
        else: msg += f" Parcel {parcel.parcel_id} is already in queue."
    flash(msg, "success")
    return redirect(url_for("status_page", parcel_id=parcel.parcel_id))

@app.route("/status/pop", methods=["POST"])
def pop_parcel_status():
    parcel_id = request.form.get("parcel_id", "").strip()
    parcel = parcel_list.search(parcel_id)
    if not parcel:
        flash("Parcel not found.", "danger")
        return redirect(url_for("status_page"))
    stack = status_histories.get(parcel.parcel_id)
    if not stack or not stack.top: flash("No status history available to pop.", "warning")
    elif stack.top.next is None: flash("Cannot pop the initial 'Created' status.", "warning")
    else: flash(f"Safely popped '{stack.pop()}' from status history Stack (LIFO).", "success")
    return redirect(url_for("status_page", parcel_id=parcel.parcel_id))

@app.route("/search")
def search_page():
    parcel_id = request.args.get("parcel_id", "").strip()
    linear_res, searched = None, bool(parcel_id)
    if parcel_id:
        parcels = get_parcels_from_linked_list(parcel_list)
        linear_res = linear_search(parcels, parcel_id)
    return render_template("search.html", parcel_id=parcel_id, linear_result=linear_res, searched=searched)

@app.route("/sorting")
def sorting_page():
    parcels = get_parcels_from_linked_list(parcel_list)
    return render_template("sorting.html", sorted_parcels=merge_sort_parcels(parcels.copy()), priority_parcels=prioritize_parcels(parcels.copy()))

@app.route("/network")
def network_page():
    parcels = get_parcels_from_linked_list(parcel_list)
    for p in parcels: delivery_graph.add_location(p.source); delivery_graph.add_location(p.destination)
    for h in hub_bst.get_inorder_hubs(): delivery_graph.add_location(h.hub_name); delivery_graph.add_alias(h.location, h.hub_name)
    locations, routes = list(delivery_graph.graph.keys()), []
    for loc, nbrs in delivery_graph.graph.items():
        for nbr in nbrs:
            if (nbr, loc) not in routes: routes.append((loc, nbr))

    sel_id, start_loc = request.args.get("parcel_id", "").strip(), request.args.get("start", "").strip()
    sel_parcel, p_traversal, p_err, p_warn, reachable = None, [], None, None, None
    if sel_id:
        sel_parcel = parcel_list.search(sel_id)
        if not sel_parcel: p_err = "Selected parcel not found."
        else:
            s, d = sel_parcel.source, sel_parcel.destination
            canon_s, canon_d = delivery_graph.get_canonical(s), delivery_graph.get_canonical(d)
            if not canon_s or canon_s not in delivery_graph.graph: p_err = f"Source '{s}' not found in network."
            elif not canon_d or canon_d not in delivery_graph.graph: p_err = f"Destination '{d}' not found in network."
            else:
                s_rts, d_rts = len(delivery_graph.graph.get(canon_s, [])), len(delivery_graph.graph.get(canon_d, []))
                if canon_s != canon_d and (s_rts == 0 or d_rts == 0): p_warn = f"Endpoint without routes: {canon_s if s_rts == 0 else canon_d}."
                trav = run_bfs_traversal(canon_s)
                p_traversal, reachable = (trav, delivery_graph.is_reachable(canon_s, canon_d)) if trav is not None else ([], False)

    traversal, err = [], None
    if start_loc:
        trav = run_bfs_traversal(start_loc)
        traversal, err = (trav, None) if trav is not None else ([], "Location not found.")

    return render_template("network.html", locations=locations, routes=routes, parcels=parcels, selected_parcel=sel_parcel, parcel_traversal=p_traversal, parcel_error=p_err, parcel_warning=p_warn, is_reachable=reachable, start_location=start_loc, traversal=traversal, error=err, registered_hubs=hub_bst.get_inorder_hubs())

@app.route("/network/add", methods=["POST"])
def add_network_route():
    loc1, loc2 = request.form.get("location1", "").strip(), request.form.get("location2", "").strip()
    valid_locs = {loc.lower(): loc for loc in delivery_graph.graph.keys()}
    for h in hub_bst.get_inorder_hubs():
        valid_locs[h.hub_name.lower()] = h.hub_name; valid_locs[h.location.lower()] = h.location

    if not loc1 or not loc2: flash("Please choose both delivery locations.", "danger")
    elif loc1.lower() == loc2.lower(): flash("Choose two different delivery locations.", "danger")
    elif loc1.lower() not in valid_locs or loc2.lower() not in valid_locs: flash("Both locations must be registered delivery hubs or parcel endpoints.", "danger")
    elif delivery_graph.has_route(loc1, loc2): flash(f"Route between '{loc1}' and '{loc2}' already exists.", "warning")
    else:
        delivery_graph.add_route(loc1, loc2)
        flash(f"Route '{loc1} ↔ {loc2}' added successfully.", "success")
    return redirect(url_for("network_page"))

@app.route("/binary-tree")
def binary_tree_page():
    t_type = request.args.get("traversal", "inorder").strip().lower()
    if t_type not in ("inorder", "preorder", "postorder"): t_type = "inorder"
    tree = build_sample_tree()
    sequence = tree.get_traversal_list(t_type)
    all_traversals = {k: {"sequence": tree.get_traversal_list(k), "sequence_str": " → ".join(str(x) for x in tree.get_traversal_list(k)), "explanation": TRAVERSAL_EXPLANATIONS[k]} for k in ("inorder", "preorder", "postorder")}
    return render_template("binary_tree.html", active_traversal=t_type, sequence=sequence, sequence_str=" → ".join(str(x) for x in sequence), explanation=TRAVERSAL_EXPLANATIONS.get(t_type), nodes=SAMPLE_TREE_NODES, all_traversals=all_traversals)

if __name__ == "__main__":
    app.run(debug=True)
