from typing import Any


def _safe_budget(value: Any) -> float:
    try:
        budget = float(value)
        return max(budget, 0.0)
    except (TypeError, ValueError):
        return 0.0


def interior_fallback(data: dict[str, Any]) -> dict[str, Any]:
    budget = _safe_budget(data.get("budget"))
    room_type = data.get("room_type", "room")
    style = data.get("style", "modern")
    room_size = data.get("room_size", "medium")

    furniture = round(budget * 0.35, 2)
    lighting = round(budget * 0.12, 2)
    decor = round(budget * 0.18, 2)
    storage = round(budget * 0.20, 2)
    contingency = round(budget * 0.15, 2)

    return {
        "source": "fallback",
        "title": f"{style.title()} {room_type.title()} Interior Plan",
        "summary": (
            f"A practical {style} interior plan for a {room_size} "
            f"{room_type}, keeping the total budget near ₹{budget:,.0f}."
        ),
        "suggestions": [
            f"Choose space-saving furniture suitable for a {room_size} room.",
            f"Use a {style} design theme with a consistent color palette.",
            "Prefer multipurpose furniture when the available space is limited.",
            "Use layered lighting with one main light and smaller accent lights.",
            "Keep a portion of the budget for unexpected expenses.",
        ],
        "budget_breakdown": {
            "Furniture": furniture,
            "Lighting": lighting,
            "Decor": decor,
            "Storage": storage,
            "Contingency": contingency,
        },
        "tips": [
            "Measure the room before purchasing large furniture.",
            "Compare prices from multiple sellers.",
            "Prioritize essential furniture before decorative items.",
        ],
        "marketplace_searches": [
            f"{style} {room_type} furniture",
            f"{style} room lights",
            f"{style} home decor",
            f"{room_type} storage furniture",
        ],
    }


def party_fallback(data: dict[str, Any]) -> dict[str, Any]:
    budget = _safe_budget(data.get("budget"))
    guests = max(int(data.get("guests", 1)), 1)
    occasion = data.get("occasion", "party")
    location = data.get("location", "your location")

    food = round(budget * 0.40, 2)
    venue = round(budget * 0.20, 2)
    decoration = round(budget * 0.15, 2)
    entertainment = round(budget * 0.10, 2)
    contingency = round(budget * 0.15, 2)

    per_guest = round(budget / guests, 2)

    return {
        "source": "fallback",
        "title": f"{occasion.title()} Party Budget Plan",
        "summary": (
            f"A practical budget plan for {guests} guests in {location}, "
            f"with an estimated budget of ₹{budget:,.0f}."
        ),
        "guests": guests,
        "budget_per_guest": per_guest,
        "suggestions": [
            f"Plan food quantities based on approximately {guests} guests.",
            "Confirm the venue capacity before making bookings.",
            "Keep decorations simple and reusable where possible.",
            "Compare catering packages instead of ordering individual items.",
            "Keep a contingency amount for last-minute expenses.",
        ],
        "budget_breakdown": {
            "Food & Catering": food,
            "Venue": venue,
            "Decoration": decoration,
            "Entertainment": entertainment,
            "Contingency": contingency,
        },
        "tips": [
            "Create the guest list before finalizing food quantities.",
            "Ask vendors about package discounts.",
            "Book important services early.",
        ],
        "marketplace_searches": [
            f"{occasion} party decorations",
            "party catering services",
            "party return gifts",
            "party lights decoration",
        ],
    }


def jewelry_fallback(data: dict[str, Any]) -> dict[str, Any]:
    budget = _safe_budget(data.get("budget"))
    occasion = data.get("occasion", "occasion")
    jewelry_type = data.get("jewelry_type", "jewelry")
    outfit_color = data.get("outfit_color", "neutral")

    jewelry_budget = round(budget * 0.80, 2)
    accessories = round(budget * 0.10, 2)
    contingency = round(budget * 0.10, 2)

    return {
        "source": "fallback",
        "title": f"{jewelry_type.title()} Recommendation",
        "summary": (
            f"A {jewelry_type} suggestion for a {occasion} with a "
            f"{outfit_color} outfit, staying within approximately "
            f"₹{budget:,.0f}."
        ),
        "suggestions": [
            f"Choose {jewelry_type} that complements the {outfit_color} outfit.",
            "Keep the jewelry style consistent with the occasion.",
            "Avoid using too many statement pieces together.",
            "Check the material, size and return policy before purchasing.",
            "Compare similar designs from multiple sellers.",
        ],
        "style_notes": [
            f"{outfit_color.title()} outfits can be paired with contrasting or complementary jewelry tones.",
            f"For a {occasion}, choose a level of detailing appropriate for the event.",
            "Balance statement jewelry with simpler pieces.",
        ],
        "budget_breakdown": {
            "Main Jewelry": jewelry_budget,
            "Additional Accessories": accessories,
            "Contingency": contingency,
        },
        "tips": [
            "Check jewelry dimensions before ordering online.",
            "Look for verified seller ratings and product reviews.",
            "Keep the total purchase within the planned budget.",
        ],
        "marketplace_searches": [
            f"{jewelry_type} for {occasion}",
            f"{jewelry_type} {outfit_color}",
            f"affordable {jewelry_type}",
        ],
        "image_generated": False,
        "image_url": None,
    }


def fallback_recommendation(
    kind: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    if kind == "interior":
        return interior_fallback(data)

    if kind == "party":
        return party_fallback(data)

    if kind == "jewelry":
        return jewelry_fallback(data)

    return {
        "source": "fallback",
        "title": "PocketSmart AI Recommendation",
        "summary": "We could not identify the requested planner type.",
        "suggestions": [],
        "budget_breakdown": {},
        "tips": [],
        "marketplace_searches": [],
    }