from modules.Elo_csv import AOE2ItaliaElo
from modules.reliclink_API import relicAPI
import requests

# a = AOE2ItaliaElo()

b = relicAPI()
#print(b.getElos(a.get_steam_id("HSL | Muca")) )

print(b.findLobby_byID(254830248))


msg = requests
print(msg)
