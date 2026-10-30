#!/usr/bin/env python3
"""Draw the 12 Houses of the Zodiac Tarot spread with OS entropy.

Each draw deals 12 houses with 1 Major Arcana card and 2 Minor Arcana
cards (36 cards total, each independently reversible). The Major and Minor
decks are shuffled independently with Fisher-Yates; reversals are
independent per card. Unseeded draws use the ``secrets`` module. ``--seed``
selects an isolated ``random.Random`` instance that replays the upstream
draw order (Major shuffle, Minor shuffle, reversals in house order) for
reproducible tests only and carries no entropy claim.

Every draw verifies all 92 assets first and fails closed: any missing
house/card/reference file is an error, never a placeholder.

Standard library only. Requires Python 3.11+.
"""

import json
import math
import os
import random
import secrets
import sys

SPREAD_NAME = "12 Houses of the Zodiac"


def _entropy_bits():
    major = math.log2(math.comb(22, 12))
    minor = math.log2(math.comb(56, 24))
    reversals = 36.0
    return {
        "major_arcana": round(major, 2),
        "minor_arcana": round(minor, 2),
        "reversals": reversals,
        "total": round(major + minor + 36.0, 2),
    }


ENTROPY_BITS = _entropy_bits()

MAJOR_ARCANA = (
    ("major", "00-the-fool"),
    ("major", "01-the-magician"),
    ("major", "02-the-high-priestess"),
    ("major", "03-the-empress"),
    ("major", "04-the-emperor"),
    ("major", "05-the-hierophant"),
    ("major", "06-the-lovers"),
    ("major", "07-the-chariot"),
    ("major", "08-strength"),
    ("major", "09-the-hermit"),
    ("major", "10-wheel-of-fortune"),
    ("major", "11-justice"),
    ("major", "12-the-hanged-man"),
    ("major", "13-death"),
    ("major", "14-temperance"),
    ("major", "15-the-devil"),
    ("major", "16-the-tower"),
    ("major", "17-the-star"),
    ("major", "18-the-moon"),
    ("major", "19-the-sun"),
    ("major", "20-judgement"),
    ("major", "21-the-world"),
)

RANKS = (
    "ace",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "page",
    "knight",
    "queen",
    "king",
)

SUITS = ("wands", "cups", "swords", "pentacles")

ZODIAC_HOUSES = (
    ("First House", "Self, identity, agency, and first motion", "01-first-house"),
    ("Second House", "Resources, values, constraints, and preservation", "02-second-house"),
    ("Third House", "Communication, learning, interfaces, and local connections", "03-third-house"),
    ("Fourth House", "Foundations, history, context, and hidden dependencies", "04-fourth-house"),
    ("Fifth House", "Creativity, experimentation, expressiveness, and delight", "05-fifth-house"),
    ("Sixth House", "Practice, service, quality, routine, and maintenance", "06-sixth-house"),
    ("Seventh House", "Partnership, contracts, users, and external counterparts", "07-seventh-house"),
    ("Eighth House", "Transformation, risk, shared state, secrets, and deep change", "08-eighth-house"),
    ("Ninth House", "Exploration, principles, standards, and broader strategy", "09-ninth-house"),
    ("Tenth House", "Delivery, reputation, public outcome, and long-term direction", "10-tenth-house"),
    ("Eleventh House", "Community, networks, systems, and shared aspirations", "11-eleventh-house"),
    ("Twelfth House", "Blind spots, hidden costs, endings, and unconscious assumptions", "12-twelfth-house"),
)

REFERENCE_FILES = (
    "references/INTERPRETATION_GUIDE.md",
    "references/TECHNICAL_CONTEXT_LENSES.md",
)


class _Entropy:
    """Bounded draw source: OS entropy by default, isolated PRNG on --seed."""

    def __init__(self, seed=None):
        self.seeded = seed is not None
        self._rng = random.Random(seed) if seed is not None else None

    def randbelow(self, n):
        if self._rng is None:
            return secrets.randbelow(n)
        return self._rng.randrange(n)

    def coin(self):
        if self._rng is None:
            return secrets.randbits(1) == 1
        return self._rng.getrandbits(1) == 1


def _skill_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_minor_deck():
    return [(suit, "%s-of-%s" % (rank, suit)) for suit in SUITS for rank in RANKS]


def build_deck():
    return list(MAJOR_ARCANA) + build_minor_deck()


def expected_asset_files():
    files = list(REFERENCE_FILES)
    files += ["houses/%s.md" % house_id for _, _, house_id in ZODIAC_HOUSES]
    files += ["cards/major/%s.md" % card_id for _, card_id in MAJOR_ARCANA]
    files += ["cards/%s/%s-of-%s.md" % (suit, rank, suit) for suit in SUITS for rank in RANKS]
    return files


def verify_assets():
    base = _skill_dir()
    return [rel for rel in expected_asset_files() if not os.path.isfile(os.path.join(base, rel))]


def fisher_yates_shuffle(deck, entropy):
    for i in range(len(deck) - 1, 0, -1):
        j = entropy.randbelow(i + 1)
        deck[i], deck[j] = deck[j], deck[i]
    return deck


def _read_skill_file(relative_file):
    path = os.path.join(_skill_dir(), relative_file)
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def card_record(suit, card_id, position, role, entropy, include_content=False):
    record = {
        "suit": suit,
        "card_id": card_id,
        "reversed": entropy.coin(),
        "position": position,
        "role": role,
        "file": "cards/%s/%s.md" % (suit, card_id),
    }
    if include_content:
        record["content"] = _read_skill_file(record["file"])
    return record


def _build_house_record(house_number, house_meta, major_card, minor_pair, position, entropy, include_content):
    house_name, focus, house_id = house_meta
    major_suit, major_id = major_card
    (m1_suit, m1_id), (m2_suit, m2_id) = minor_pair
    house_file = "houses/%s.md" % house_id
    record = {
        "house": house_number,
        "name": house_name,
        "focus": focus,
        "file": house_file,
        "cards": [
            card_record(major_suit, major_id, position, "major_arcana", entropy, include_content),
            card_record(m1_suit, m1_id, position + 1, "minor_arcana_1", entropy, include_content),
            card_record(m2_suit, m2_id, position + 2, "minor_arcana_2", entropy, include_content),
        ],
    }
    if include_content:
        record["content"] = _read_skill_file(house_file)
    return record


def draw_zodiac_spread(include_content=False, entropy=None):
    entropy = entropy or _Entropy()
    major_deck = list(MAJOR_ARCANA)
    minor_deck = build_minor_deck()
    fisher_yates_shuffle(major_deck, entropy)
    fisher_yates_shuffle(minor_deck, entropy)
    houses = []
    for i, house_meta in enumerate(ZODIAC_HOUSES):
        houses.append(
            _build_house_record(
                house_number=i + 1,
                house_meta=house_meta,
                major_card=major_deck[i],
                minor_pair=(minor_deck[2 * i], minor_deck[2 * i + 1]),
                position=1 + 3 * i,
                entropy=entropy,
                include_content=include_content,
            )
        )
    bits = ENTROPY_BITS
    return {
        "spread": SPREAD_NAME,
        "houses": houses,
        "entropy_bits": bits,
        "entropy_note": (
            "Assumes the draw source provides cryptographically secure "
            "bounded draws in unseeded mode. This is a conservative "
            "unordered-card budget: %s bits from Major Arcana selection, "
            "%s bits from Minor Arcana selection, and %s reversal bits. "
            "Ordered house assignment contains more entropy."
            % (bits["major_arcana"], bits["minor_arcana"], bits["reversals"])
        ),
    }


USAGE = "Usage: draw.py [--content] [--verify] [--seed N]"


def _parse_args(argv):
    args = list(argv)
    include_content = "--content" in args
    if include_content:
        args.remove("--content")
    verify_only = "--verify" in args
    if verify_only:
        args.remove("--verify")
    seed = None
    if "--seed" in args:
        idx = args.index("--seed")
        args.pop(idx)
        if idx >= len(args):
            print("Error: --seed requires an integer value. %s" % USAGE, file=sys.stderr)
            sys.exit(1)
        raw = args.pop(idx)
        try:
            seed = int(raw)
        except ValueError:
            print("Error: '--seed %s' is not a valid integer. %s" % (raw, USAGE), file=sys.stderr)
            sys.exit(1)
    if args:
        print("Error: unexpected argument '%s'. %s" % (args[0], USAGE), file=sys.stderr)
        sys.exit(1)
    return include_content, verify_only, seed


def _missing_exit(missing, detail):
    print(json.dumps({"status": "missing", "missing": missing}, indent=2))
    print("Error: %d reference files missing; %s." % (len(missing), detail), file=sys.stderr)
    return 2


def main(argv=None):
    include_content, verify_only, seed = _parse_args(sys.argv[1:] if argv is None else argv)
    missing = verify_assets()
    if verify_only:
        if missing:
            return _missing_exit(missing, "refusing to certify")
        print(json.dumps({"status": "ok", "cards": 78, "houses": 12, "references": 2}, indent=2))
        return 0
    if missing:
        return _missing_exit(missing, "refusing to draw")
    entropy = _Entropy(seed)
    try:
        result = draw_zodiac_spread(include_content=include_content, entropy=entropy)
    except OSError as exc:
        print("Error: failed to read entropy source or asset: %s" % exc, file=sys.stderr)
        return 1
    if seed is not None:
        result["seed"] = seed
        result["entropy_note"] = "Seeded test draw (--seed %d): reproducible and carrying no entropy claim." % seed
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(1)
    except Exception as exc:  # fail loudly, never invent a spread
        print("Error: draw.py failed: %s" % exc, file=sys.stderr)
        sys.exit(1)
