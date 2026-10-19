# Tests for the one-question-at-a-time flow (frontend/flow.py).
# Streamlit is replaced by a tiny fake, so no browser is needed.

import pytest

from frontend import flow


class State(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


class FakeSt:
    def __init__(self):
        self.session_state = State()


@pytest.fixture
def fake(monkeypatch):
    f = FakeSt()
    monkeypatch.setattr(flow, "st", f)
    flow.init()
    return f


def choose(fake, i, label):
    fake.session_state[f"qr{i}"] = label
    flow._pick(i)


def test_there_are_24_questions_in_the_right_groups(fake):
    assert flow.TOTAL == 24
    phq, gad, stress, skin = flow.collected()
    assert (len(phq), len(gad), len(stress), len(skin)) == (9, 7, 4, 4)


def test_picking_an_answer_moves_to_the_next_question(fake):
    choose(fake, 0, flow.QUESTIONS[0]["labels"][2])
    assert fake.session_state.answers[0] == 2
    assert fake.session_state.qi == 1


def test_item9_above_zero_stays_so_the_support_message_is_seen(fake):
    fake.session_state.qi = flow.SAFETY_INDEX
    choose(fake, flow.SAFETY_INDEX, flow.QUESTIONS[flow.SAFETY_INDEX]["labels"][1])
    assert fake.session_state.qi == flow.SAFETY_INDEX


def test_item9_zero_moves_on(fake):
    fake.session_state.qi = flow.SAFETY_INDEX
    choose(fake, flow.SAFETY_INDEX, flow.QUESTIONS[flow.SAFETY_INDEX]["labels"][0])
    assert fake.session_state.qi == flow.SAFETY_INDEX + 1


def test_back_stops_at_the_first_question(fake):
    flow._back()
    assert fake.session_state.qi == 0


def test_next_stops_at_the_end(fake):
    for _ in range(40):
        flow._next()
    assert fake.session_state.qi == flow.TOTAL


def test_answers_are_kept_when_going_back_and_forth(fake):
    choose(fake, 0, flow.QUESTIONS[0]["labels"][3])
    flow._back()
    flow._next()
    assert fake.session_state.answers[0] == 3


def test_changing_an_answer_clears_old_results(fake):
    fake.session_state["result"] = {"old": True}
    choose(fake, 0, flow.QUESTIONS[0]["labels"][1])
    assert "result" not in fake.session_state


def test_unanswered_count_goes_down(fake):
    assert flow.unanswered_count() == 24
    choose(fake, 0, flow.QUESTIONS[0]["labels"][1])
    assert flow.unanswered_count() == 23


def test_empty_selection_is_ignored(fake):
    fake.session_state["qr0"] = None
    flow._pick(0)
    assert fake.session_state.answers[0] is None


def test_goto_jumps_to_that_question(fake):
    flow._goto(7)
    assert fake.session_state.qi == 7