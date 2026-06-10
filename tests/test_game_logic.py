from logic_utils import check_guess, parse_guess, update_score

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
