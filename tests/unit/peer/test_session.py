"""PeerSession: handshake gate, turn handlers, protocol-violation collapse (PLAN §4–§5)."""

from pathlib import Path

import pytest

from copthief_core.domain.state_machine import GameState
from copthief_core.peer.session import NegotiationError, PeerSession
from copthief_core.shared.config import load_all

CONSTITUTION, PRIVATE, _LIMITS = load_all(Path("config"), counted=False)


def _pair() -> tuple[PeerSession, PeerSession]:
    police = PeerSession(CONSTITUTION, PRIVATE, role="police", seed=11)
    thief = PeerSession(CONSTITUTION, PRIVATE, role="thief", seed=22)
    return police, thief


def _handshake(police: PeerSession, thief: PeerSession) -> None:
    thief.handle_negotiate(police.negotiate_payload())
    police.handle_negotiate(thief.negotiate_payload())


def test_handshake_locks_the_same_game_uid_on_both_peers() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    assert police.game_uid is not None
    assert police.game_uid == thief.game_uid


def test_handshake_refuses_value_drifted_terms() -> None:
    police, thief = _pair()
    proposal = police.negotiate_payload()
    proposal["terms"]["board_size"] = 9  # their terms no longer value-equal ours
    with pytest.raises(NegotiationError, match="terms"):
        thief.handle_negotiate(proposal)


def test_handshake_refuses_a_bad_signature() -> None:
    police, thief = _pair()
    proposal = police.negotiate_payload()
    proposal["signature"] = "0" * 64
    with pytest.raises(NegotiationError, match="signature"):
        thief.handle_negotiate(proposal)


def test_thief_moves_first_police_waits() -> None:
    # M2 F2 (oracle sha 960499fd): the reference's runtime gives the THIEF the first
    # game turn; the police peer starts in the receive loop.
    police, thief = _pair()
    assert thief.machine.state is GameState.COMPUTING_MOVE
    assert police.machine.state is GameState.WAITING_FOR_OPPONENT


def test_turn_exchange_advances_both_state_machines() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    outbound = thief.take_turn(now=1000.0)
    assert outbound["step"] == 1
    assert thief.machine.state is GameState.AWAITING_REVEAL
    police.handle_receive_turn(outbound)
    assert police.machine.state is GameState.COMPUTING_MOVE
    reply = police.take_turn(now=1000.5)
    thief.handle_receive_turn(reply)
    assert thief.machine.state is GameState.WAITING_FOR_OPPONENT


def _play_to_survival(police: PeerSession, thief: PeerSession) -> dict:
    """Alternate turns thief-first until the thief's survival turn; return that message."""
    threshold = CONSTITUTION.movement.survival_threshold
    for step in range(1, threshold + 1):
        message = thief.take_turn(now=float(step))
        if step == threshold:
            return message
        police.handle_receive_turn(message)
        thief.handle_receive_turn(police.take_turn(now=step + 0.5))
    raise AssertionError("unreachable")


def test_thief_survival_turn_carries_win_claim_and_ends_its_game() -> None:
    # Reference semantics: the thief's threshold-reaching turn carries
    # win_claim {"type": "survival"} and the thief's own game ends with it.
    police, thief = _pair()
    _handshake(police, thief)
    final = _play_to_survival(police, thief)
    assert final["win_claim"] == {"type": "survival"}
    assert thief.machine.state is GameState.GAME_OVER
    assert thief.outcome == "thief_survival"


def test_receiving_a_win_claim_ends_the_receiver_game() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    final = _play_to_survival(police, thief)
    police.handle_receive_turn(final)
    assert police.machine.state is GameState.GAME_OVER
    assert police.outcome == "thief_survival"


def test_no_win_claim_before_the_survival_threshold() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    first = thief.take_turn(now=1.0)
    assert first["win_claim"] is None
    police.handle_receive_turn(first)
    assert police.machine.state is GameState.COMPUTING_MOVE


def test_malformed_inbound_turn_collapses_to_technical_loss() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    outbound = thief.take_turn(now=1000.0)
    del outbound["commit"]
    with pytest.raises(Exception, match="commit"):
        police.handle_receive_turn(outbound)
    assert police.machine.state is GameState.TECHNICAL_LOSS


def test_step_discontinuity_collapses_to_technical_loss() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    outbound = thief.take_turn(now=1000.0)
    outbound["step"] = 7  # replay/skip: police expects step 1
    with pytest.raises(Exception, match="step"):
        police.handle_receive_turn(outbound)
    assert police.machine.state is GameState.TECHNICAL_LOSS


def test_turn_arriving_mid_computation_collapses_to_technical_loss() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    outbound = thief.take_turn(now=1.0)
    police.handle_receive_turn(outbound)  # police now COMPUTING_MOVE
    duplicate = dict(outbound)
    duplicate["step"] = 2  # passes continuity, arrives in a state that cannot accept it
    with pytest.raises(Exception, match="arrived in state"):
        police.handle_receive_turn(duplicate)
    assert police.machine.state is GameState.TECHNICAL_LOSS


class _ScriptedPolicy:
    """Deterministic stand-in: plays a scripted move list, then STAYs."""

    def __init__(self, moves: list[str]) -> None:
        self._moves = list(moves)

    def pick_move(self, board, position, move_set):  # noqa: ANN001, ANN201 - test stub
        return self._moves.pop(0) if self._moves else "STAY"

    def next_hint(self, *, hint_max_words: int) -> str:
        return "scripted"


def test_police_move_turn_carries_its_landing_cell_as_capture_claim() -> None:
    # SQ2 (oracle sha 960499fd): the reference police claims its OWN landing cell on
    # EVERY moving turn — free, automatic, answered honestly by the thief.
    police, thief = _pair()
    _handshake(police, thief)
    police.machine.state = GameState.COMPUTING_MOVE  # as if the thief's turn arrived
    police.policy = _ScriptedPolicy(["S"])
    message = police.take_turn(now=1.0)
    assert message["capture_claim"] == list(police.position)


def test_police_stay_turn_claims_nothing() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    police.machine.state = GameState.COMPUTING_MOVE
    police.policy = _ScriptedPolicy(["STAY"])
    assert police.take_turn(now=1.0)["capture_claim"] is None


def test_thief_answers_a_missed_claim_honestly_and_plays_on() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    first = thief.take_turn(now=1.0)
    police.handle_receive_turn(first)
    police.policy = _ScriptedPolicy(["S"])
    claim_turn = police.take_turn(now=1.5)
    assert claim_turn["capture_claim"] is not None
    thief.handle_receive_turn(claim_turn)
    reply = thief.take_turn(now=2.0)
    assert reply["claim_response"] == {"claim": claim_turn["capture_claim"], "caught": False}
    assert thief.machine.state is GameState.AWAITING_REVEAL  # game continues


def test_caught_thief_sends_the_final_message_and_both_games_end_capture() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    first = thief.take_turn(now=1.0)
    police.handle_receive_turn(first)
    police.policy = _ScriptedPolicy(["S"])
    claim_turn = police.take_turn(now=1.5)
    claim_turn["capture_claim"] = list(thief.position)  # the claim lands on the thief
    thief.handle_receive_turn(claim_turn)
    final = thief.take_turn(now=2.0)
    assert final["claim_response"] == {"claim": list(thief.position), "caught": True}
    assert final["capture_claim"] is None and final["win_claim"] is None
    assert thief.machine.state is GameState.GAME_OVER
    assert thief.outcome == "cop_capture"
    police.handle_receive_turn(final)
    assert police.machine.state is GameState.GAME_OVER
    assert police.outcome == "cop_capture"


def test_control_message_is_answered_without_touching_game_state() -> None:
    police, thief = _pair()
    _handshake(police, thief)
    before = thief.machine.state
    response = thief.handle_receive_control({"sender": "police", "kind": "status"})
    assert response["status"] == "ok"
    assert thief.machine.state is before
