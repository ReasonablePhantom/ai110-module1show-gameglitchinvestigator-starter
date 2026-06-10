from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- New tests for the bugs fixed in this project ---

def test_blank_input_is_rejected():
    # Bug #3: blank / whitespace-only input must be treated as invalid (no attempt spent).
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err is not None

def test_non_number_is_rejected():
    # Bug #3: a non-numeric guess is invalid.
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."

def test_valid_number_is_parsed():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_wrong_guess_costs_five_points():
    # Bug #6: scoring is deterministic now. Any wrong guess loses a flat 5 points,
    # regardless of attempt number parity.
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95
    assert update_score(100, "Too Low", 4) == 95

def test_first_attempt_win_awards_full_points():
    # A win on the first attempt awards the full 100-point bonus.
    assert update_score(0, "Win", 1) == 100


# --- Edge cases ---

# parse_guess edge cases
def test_parse_guess_none():
    # None input (Streamlit can pass None before the user types anything).
    ok, value, _ = parse_guess(None)
    assert ok is False
    assert value is None

def test_parse_guess_float_string_truncates():
    # "3.7" should be accepted and truncated to int 3, not rejected.
    ok, value, _ = parse_guess("3.7")
    assert ok is True
    assert value == 3

def test_parse_guess_zero():
    # Zero is a valid integer — should not be treated as falsy/empty.
    ok, value, _ = parse_guess("0")
    assert ok is True
    assert value == 0

def test_parse_guess_leading_trailing_spaces():
    # "  42  " should parse to 42, not be rejected as blank.
    ok, value, _ = parse_guess("  42  ")
    assert ok is True
    assert value == 42

def test_parse_guess_below_range():
    # 0 is outside 1-100; should be rejected without burning an attempt.
    ok, value, err = parse_guess("0", low=1, high=100)
    assert ok is False
    assert value is None
    assert "1" in err and "100" in err

def test_parse_guess_above_range():
    # 101 is outside 1-100; should be rejected.
    ok, _, _ = parse_guess("101", low=1, high=100)
    assert ok is False

def test_parse_guess_negative_out_of_range():
    # Negative number outside 1-100 should be rejected.
    ok, _, _ = parse_guess("-5", low=1, high=100)
    assert ok is False

def test_parse_guess_boundary_low_is_valid():
    # The lowest value in range (1) should be accepted.
    ok, value, _ = parse_guess("1", low=1, high=100)
    assert ok is True
    assert value == 1

def test_parse_guess_boundary_high_is_valid():
    # The highest value in range (100) should be accepted.
    ok, value, _ = parse_guess("100", low=1, high=100)
    assert ok is True
    assert value == 100

def test_parse_guess_no_range_skips_check():
    # Without low/high, any valid integer passes (backward-compat for tests that
    # call parse_guess without range args).
    ok, value, _ = parse_guess("0")
    assert ok is True
    assert value == 0

# check_guess edge cases
def test_check_guess_one_below_secret():
    # Off-by-one below should still be "Too Low", not "Win".
    assert check_guess(49, 50) == "Too Low"

def test_check_guess_one_above_secret():
    # Off-by-one above should still be "Too High", not "Win".
    assert check_guess(51, 50) == "Too High"

# update_score edge cases
def test_update_score_late_win_floor():
    # A win on attempt 10 would give 100 - 10*9 = 10 (the minimum floor).
    assert update_score(0, "Win", 10) == 10

def test_update_score_very_late_win_stays_at_floor():
    # Past the floor (attempt 15 would give 100 - 10*14 = -40), clamped to 10.
    assert update_score(0, "Win", 15) == 10

def test_update_score_unknown_outcome_unchanged():
    # An unrecognised outcome should leave the score exactly as-is.
    assert update_score(77, "Banana", 3) == 77

# get_range_for_difficulty edge cases
def test_get_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_get_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_get_range_unknown_difficulty_defaults():
    # An unrecognised difficulty should fall back to the Normal range.
    assert get_range_for_difficulty("Impossible") == (1, 100)
