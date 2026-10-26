from dataclasses import dataclass


@dataclass
class Passenger:
    name: str
    age: int


@dataclass
class TravelClass:
    name: str
    rate_per_km: float
    reservation_fee: float


# Example fare rules; replace these with the railway's actual policy.
DISTANCE_SLABS = [
    (100, 1.00),       # First 100 km
    (400, 0.80),       # Next 300 km
    (float("inf"), 0.60),  # Remaining distance
]

SENIOR_AGE = 60
SENIOR_CONCESSION_RATE = 0.40
CHILD_AGE = 12
CHILD_FARE_RATE = 0.50
CANCELLATION_PENALTY_RATE = 0.20


def distance_charge(distance_km: float, class_rate: float) -> float:
    if distance_km <= 0 or class_rate < 0:
        raise ValueError("Distance must be positive and class rate cannot be negative.")

    charge = 0.0
    previous_limit = 0.0

    for limit, slab_rate in DISTANCE_SLABS:
        slab_distance = min(distance_km, limit - previous_limit)
        charge += slab_distance * slab_rate * class_rate
        distance_km -= slab_distance
        previous_limit = limit

        if distance_km <= 0:
            break

    return charge


def passenger_fare(
    passenger: Passenger,
    distance_km: float,
    travel_class: TravelClass,
) -> float:
    if passenger.age < 0:
        raise ValueError(f"Invalid age for {passenger.name}.")
    if travel_class.reservation_fee < 0:
        raise ValueError("Reservation fee cannot be negative.")

    base_fare = distance_charge(distance_km, travel_class.rate_per_km)

    if passenger.age < CHILD_AGE:
        base_fare *= CHILD_FARE_RATE
    elif passenger.age >= SENIOR_AGE:
        base_fare *= 1 - SENIOR_CONCESSION_RATE

    return base_fare + travel_class.reservation_fee


def calculate_booking(
    passengers: list[Passenger],
    distance_km: float,
    travel_class: TravelClass,
    cancelled: bool = False,
) -> dict:
    if not passengers:
        raise ValueError("At least one passenger is required.")

    fares = [
        {
            "name": passenger.name,
            "fare": passenger_fare(passenger, distance_km, travel_class),
        }
        for passenger in passengers
    ]

    total_fare = sum(item["fare"] for item in fares)
    cancellation_penalty = (
        total_fare * CANCELLATION_PENALTY_RATE if cancelled else 0.0
    )
    refund = total_fare - cancellation_penalty if cancelled else 0.0

    return {
        "class": travel_class.name,
        "distance_km": distance_km,
        "passenger_fares": fares,
        "total_fare": round(total_fare, 2),
        "cancelled": cancelled,
        "cancellation_penalty": round(cancellation_penalty, 2),
        "refund": round(refund, 2) if cancelled else None,
    }


if __name__ == "__main__":
    passengers = [
        Passenger("Asha", 34),
        Passenger("Ravi", 67),
        Passenger("Mina", 9),
    ]

    second_class = TravelClass(
        name="Second Class",
        rate_per_km=1.0,
        reservation_fee=20.0,
    )

    booking = calculate_booking(
        passengers=passengers,
        distance_km=550,
        travel_class=second_class,
        cancelled=False,
    )

    print(f"Class: {booking['class']}")
    print(f"Distance: {booking['distance_km']} km")
    for item in booking["passenger_fares"]:
        print(f"{item['name']}: {item['fare']:.2f}")
    print(f"Total fare: {booking['total_fare']:.2f}")

    # To calculate cancellation, set cancelled=True.
    cancelled_booking = calculate_booking(
        passengers, 550, second_class, cancelled=True
    )
    print(f"Cancellation penalty: {cancelled_booking['cancellation_penalty']:.2f}")
    print(f"Refund: {cancelled_booking['refund']:.2f}")