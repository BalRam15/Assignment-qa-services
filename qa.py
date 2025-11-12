import re
from typing import List, Dict, Any, Optional
import dateparser

INTENT_TRIP = "trip_when"
INTENT_CARS = "car_count"
INTENT_RESTAURANTS = "favorite_restaurants"

def detect_intent(q: str) -> str:
    ql = q.lower()
    if ("trip to" in ql) or ("planning" in ql and "trip" in ql) or ("travel" in ql):
        return INTENT_TRIP
    if "how many" in ql and "car" in ql:
        return INTENT_CARS
    if ("favorite" in ql or "favourite" in ql) and ("restaurant" in ql or "restaurants" in ql):
        return INTENT_RESTAURANTS
    return "unknown"

def _text(m):
    # handle both dicts and plain strings
    if isinstance(m, str):
        return m
    for k in ("text", "message", "body", "content"):
        if isinstance(m.get(k), str):
            return m[k]
    return ""

def _member_match(m, name: Optional[str]) -> bool:
    # handle both dicts and strings
    if not name:
        return True
    if isinstance(m, str):
        return name.lower() in m.lower()
    cand = [m.get("memberName"), m.get("member_name"), m.get("sender"), m.get("fromName"), m.get("author")]
    if any(isinstance(x, str) and name.lower() in x.lower() for x in cand if x):
        return True
    t = _text(m)
    return isinstance(t, str) and name.lower() in t.lower()


def _find_member(q: str) -> Optional[str]:
    m = re.search(r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)’?s|([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", q)
    return (m.group(1) or m.group(2)) if m else None

def _find_location(q: str) -> Optional[str]:
    m = re.search(r"\btrip\s+to\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)", q, re.IGNORECASE)
    return m.group(1) if m else None

def _parse_date(text: str) -> Optional[str]:
    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    return dt.strftime("%Y-%m-%d") if dt else None

def answer_trip_when(q: str, messages: List[Dict[str, Any]]) -> Optional[str]:
    who = _find_member(q)
    where = _find_location(q)
    candidates = []
    for m in messages:
        if not _member_match(m, who):
            continue
        t = _text(m)
        if not t:
            continue
        if any(w in t.lower() for w in ["trip","travel","flight"]):
            if where is None or where.lower() in t.lower():
                dt = _parse_date(t)
                if dt:
                    candidates.append((dt, t))
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0])
    dt, _ = candidates[0]
    if who and where:
        return f"{who} is planning the trip to {where} on {dt}."
    if who:
        return f"{who} is planning the trip on {dt}."
    if where:
        return f"The trip to {where} is on {dt}."
    return f"The trip is on {dt}."

def answer_car_count(q: str, messages: List[Dict[str, Any]]) -> Optional[str]:
    who = _find_member(q)
    word_to_num = {"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10}
    best = None
    for m in messages:
        if not _member_match(m, who):
            continue
        t = _text(m)
        tl = t.lower()
        if "car" not in tl:
            continue
        m1 = re.search(r"\b(\d+)\s+cars?\b", t, re.IGNORECASE)
        if m1:
            best = int(m1.group(1))
            break
        m2 = re.search(r"\b(" + "|".join(word_to_num.keys()) + r")\s+cars?\b", t, re.IGNORECASE)
        if m2:
            best = word_to_num[m2.group(1).lower()]
            break
        if re.search(r"\bI\s+have\s+a\s+car\b", t, re.IGNORECASE):
            best = 1
            break
    if best is None:
        return None
    if who:
        return f"{who} has {best} car{'s' if best != 1 else ''}."
    return f"They have {best} car{'s' if best != 1 else ''}."

def answer_favorite_restaurants(q: str, messages: List[Dict[str, Any]]) -> Optional[str]:
    who = _find_member(q)
    spots = set()
    for m in messages:
        if not _member_match(m, who):
            continue
        t = _text(m)
        m1 = re.search(r"(?:favorite|favourite)\s+restaurants?\s+(?:are|:)\s+(.+)", t, re.IGNORECASE)
        if m1:
            tail = m1.group(1)
            for part in re.split(r",| and ", tail):
                name = part.strip(" .!?:;\"'()")
                if name:
                    spots.add(name.split(".")[0])
        else:
            m2 = re.search(r"(?:favorite|favourite)\s+restaurant\s+(?:is|:)\s+(.+)", t, re.IGNORECASE)
            if m2:
                spots.add(m2.group(1).strip(" .!?:;\"'()").split(".")[0])
    if not spots:
        return None
    listed = ", ".join(sorted(spots))
    return f"{(who + "'s ") if who else ''}favorite restaurants: {listed}."


def answer_question(q: str, messages: List[dict]) -> str:
    intent = detect_intent(q.strip())
    if intent == INTENT_TRIP:
        return answer_trip_when(q, messages) or "I couldn't find a trip date for that member/location in the messages."
    if intent == INTENT_CARS:
        return answer_car_count(q, messages) or "I couldn't find a car count for that member."
    if intent == INTENT_RESTAURANTS:
        return answer_favorite_restaurants(q, messages) or "I couldn't find favorite restaurants for that member."
    return "Sorry, I don't recognize that question type yet. Try trips, cars, or favorite restaurants."
