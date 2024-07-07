from pytest import mark

from modules.constants import ELO_K
from modules.elo import Elo

elo1 = Elo(1000)
elo2 = Elo(2000)


def test_private_attribute():
    elo = Elo(1000)
    try:
        elo.elo = 10
    except AttributeError:
        pass


def test_update_elo():
    elo = Elo(1000)
    elo.update_elo(100)
    assert elo.elo == 1100
    elo.update_elo(-600)
    assert elo.elo == 500


@mark.parametrize(
    argnames=["elo_w", "elo_l", "change_w"],
    argvalues=[(1000, 1000, ELO_K / 2), (1100, 1000, 10.8)],
)
def test_compute_change(elo_w, elo_l, change_w):
    elo_w = Elo(elo_w)
    elo_l = Elo(elo_l)
    change = Elo.compute_elo_change(elo_w, elo_l)
    assert abs(change - change_w) < 0.1


def test_update_win_other():
    elo_w = Elo(1000)
    other = Elo(1000)
    elo_w.update_win(other=other)
    other.update_loss(other=elo_w)
    assert elo_w.elo == (1000 + ELO_K / 2)
    assert abs(other.elo - (1000 - ELO_K / 2)) < 1


def test_update_win_others():
    elo_w = Elo(1000)
    others = [Elo(i) for i in [0, 750, 1250, 2000]]
    elo_w.update_win(others=others)
    assert elo_w.elo == (1000 + ELO_K / 2)


def test_team_elo():
    players = [Elo(i) for i in [0, 750, 1250, 2000]]
    assert Elo.team_elo(players).elo == 1000
