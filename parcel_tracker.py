“”“Parcel tracking system with improved security and code quality.”””

import secrets
import shutil
import subprocess
import tempfile
from datetime import date
from typing import Optional

STATUS_FLOW = [
“Booked”,
“Picked Up”,
“In Transit”,
“Out for Delivery”,
“Delivered”,
]

parcels = {}

def book_parcel(
sender: str,
receiver: str,
weight_kg: float,
history: Optional[list] = None,
) -> str:
“”“Book a parcel and return its tracking ID.”””
if not sender or not receiver:
raise ValueError(“Sender and receiver must not be empty.”)

if weight_kg <= 0:
    raise ValueError("Parcel weight must be greater than zero.")
tracking_id = f"TRK{10001 + len(parcels)}"
parcels[tracking_id] = {
    "sender": sender,
    "receiver": receiver,
    "weight": weight_kg,
    "status": 0,
    "booked": str(date.today()),
}
if history is not None:
    history.append(tracking_id)
return tracking_id

def advance_status(tracking_id: str) -> str:
“”“Advance a parcel to its next delivery status.”””
parcel = parcels.get(tracking_id)

if parcel is None:
    return f"Unknown tracking id {tracking_id}"
if parcel["status"] < len(STATUS_FLOW) - 1:
    parcel["status"] += 1
return STATUS_FLOW[parcel["status"]]

def shipping_cost(weight_kg: float) -> float:
“”“Calculate shipping cost based on parcel weight.”””
if weight_kg <= 0:
raise ValueError(“Parcel weight must be greater than zero.”)

cost = 50.0
if weight_kg > 1:
    cost += (weight_kg - 1) * 30
return round(cost, 2)

def track_parcel(tracking_id: str) -> str:
“”“Return the route and current status of a parcel.”””
parcel = parcels.get(tracking_id)

if parcel is None:
    return f"Unknown tracking id {tracking_id}"
route = f"{parcel['sender']} -> {parcel['receiver']}"
status = STATUS_FLOW[parcel["status"]]
return f"{route}: {status}"

def is_with_courier(tracking_id: str) -> bool:
“”“Check whether a parcel is picked up or in transit.”””
parcel = parcels.get(tracking_id)

if parcel is None:
    return False
status = STATUS_FLOW[parcel["status"]]
return status in ("Picked Up", "In Transit")

def label_path() -> str:
“”“Create a temporary label file and return its path.”””
with tempfile.NamedTemporaryFile(
mode=“w”,
suffix=”.txt”,
delete=False,
encoding=“utf-8”,
) as temp_file:
return temp_file.name

def ping_hub(hub_address: str) -> str:
“”“Ping a hub without invoking a shell.”””
if not hub_address or hub_address.startswith(”-”):
raise ValueError(“Invalid hub address.”)

ping_executable = shutil.which("ping")
if ping_executable is None:
    raise RuntimeError("The ping executable was not found.")
return subprocess.check_output(
    [ping_executable, "-c", "1", hub_address],
    text=True,
    timeout=5,
    shell=False,
)

def main() -> None:
“”“Demonstrate parcel booking, tracking, and delivery.”””
first = book_parcel(“Bengaluru Books”, “Ravi Kumar”, 2.5)
second = book_parcel(“Gadget Hub”, “Sneha Rao”, 0.8)
third = book_parcel(“Spice Store”, “Imran Khan”, 4)

advance_status(first)
advance_status(first)
advance_status(second)
for _ in range(6):
    advance_status(third)
for tracking_id in (first, second, third):
    print(track_parcel(tracking_id))
    print("  with courier:", is_with_courier(tracking_id))
    print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
print(track_parcel("TRK00000"))
delivery_otp = secrets.randbelow(9000) + 1000
print("Delivery OTP for", third, "is", delivery_otp)
print("Parcels booked today:", len(parcels))

if name == “main”:
main()