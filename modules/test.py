from modules import *

a = Elo.AOE2ItaliaElo()

names = ["JohnBaudelaire", "ITA | Canazzo", "ITA | Born to be Brain", "ITA | Carma", "ITA | Francesco III", "ITA | GoldFish"]
print(a.get_steam_id("NAPS | L'Ammiraglio"))

b = aoe2net_API.Matches()

print(b.look_for_matches(76561197996386232,"ranked"))