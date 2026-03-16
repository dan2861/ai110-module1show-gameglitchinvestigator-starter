import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ---------------------------------------------------------------------------
# Existing tests (fixed: check_guess returns a tuple, not a bare string)
# ---------------------------------------------------------------------------

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# Bug 1 — Backwards hints
# The original code returned "Go HIGHER!" when the guess was too high and
# "Go LOWER!" when it was too low. Both messages were swapped.
# ---------------------------------------------------------------------------

def test_hint_says_go_lower_when_guess_is_too_high():
    """Guessing above the secret should tell the player to go lower."""
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint, got: {message!r}"

def test_hint_says_go_higher_when_guess_is_too_low():
    """Guessing below the secret should tell the player to go higher."""
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint, got: {message!r}"


# ---------------------------------------------------------------------------
# Bug 2 — Decimal inputs silently truncated
# "3.7" used to be accepted and converted to 3 without any warning.
# ---------------------------------------------------------------------------

def test_decimal_input_is_rejected():
    ok, _, err = parse_guess("3.7")
    assert not ok
    assert err is not None

def test_decimal_zero_is_rejected():
    ok, _, err = parse_guess("5.0")
    assert not ok
    assert err is not None


# ---------------------------------------------------------------------------
# Bug 2 (continued) — Out-of-range inputs accepted without error
# Negative numbers and values above the upper bound passed validation.
# ---------------------------------------------------------------------------

def test_negative_number_is_rejected():
    ok, _, err = parse_guess("-1", low=1, high=100)
    assert not ok
    assert err is not None

def test_zero_is_rejected_when_range_starts_at_one():
    ok, _, err = parse_guess("0", low=1, high=100)
    assert not ok
    assert err is not None

def test_value_above_high_is_rejected():
    ok, _, err = parse_guess("101", low=1, high=100)
    assert not ok
    assert err is not None

def test_boundary_values_are_accepted():
    """Lowest and highest values in range must still be valid."""
    ok_low, val_low, _ = parse_guess("1", low=1, high=100)
    ok_high, val_high, _ = parse_guess("100", low=1, high=100)
    assert ok_low and val_low == 1
    assert ok_high and val_high == 100

def test_non_numeric_input_is_rejected():
    ok, _, err = parse_guess("abc")
    assert not ok
    assert err is not None

def test_empty_input_is_rejected():
    ok, _, err = parse_guess("")
    assert not ok


# ---------------------------------------------------------------------------
# Bug 3 — Hard difficulty had a smaller range than Normal (1–50 vs 1–100)
# ---------------------------------------------------------------------------

def test_hard_range_is_wider_than_normal():
    normal_low, normal_high = get_range_for_difficulty("Normal")
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert (hard_high - hard_low) > (normal_high - normal_low), (
        f"Hard range ({hard_low}–{hard_high}) should be wider than "
        f"Normal range ({normal_low}–{normal_high})"
    )

def test_hard_range_is_not_1_to_50():
    """Regression: the original broken value was 1–50."""
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high != 50, "Hard difficulty still has the original broken range of 50"


# ---------------------------------------------------------------------------
# Bug 4 — Score could go negative
# The original update_score subtracted 5 points on every wrong guess.
# ---------------------------------------------------------------------------

def test_score_does_not_decrease_on_wrong_guess():
    score_after_too_high = update_score(0, "Too High", 1)
    score_after_too_low = update_score(0, "Too Low", 1)
    assert score_after_too_high >= 0
    assert score_after_too_low >= 0

def test_score_only_increases_on_win():
    """A win should always add points, never subtract."""
    starting_score = 50
    new_score = update_score(starting_score, "Win", 1)
    assert new_score > starting_score

def test_score_minimum_win_points_is_ten():
    """Even on the last attempt, a win should award at least 10 points."""
    new_score = update_score(0, "Win", 100)
    assert new_score >= 10
