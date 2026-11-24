# four-kb-chess, safety-net entry: a complete engine in one file.
#
# Speaks the tiny-chess-01 env protocol: POST /game {} for the game in play,
# POST /move {game, move} with a UCI move, until the answer's status is not
# "your_move". Plays the legal move that wins the most material, so every game
# is at least a fair game of chess. Deterministic: no clock, no randomness.
import json, os, sys, urllib.request as U

E = os.environ.get("MAKEFUN_ENV_URL") or sys.exit("MAKEFUN_ENV_URL is not set")
V = {"p": 1, "n": 3, "b": 3, "r": 5, "q": 9, "k": 100}


def post(p, b):
    r = U.Request(E + p, data=json.dumps(b).encode(), headers={"content-type": "application/json"})
    return json.load(U.urlopen(r))


def pick(fen, legal):
    sq = {}
    n = 0
    for c in fen.split()[0]:
        if c.isdigit():
            n += int(c)
        else:
            sq["abcdefgh"[n % 8] + str(8 - n // 8)] = c
            n += 1

    def k(m):
        v = sq.get(m[2:4])
        g = V[v.lower()] if v else (1 if (m[0] != m[2] and sq[m[:2]].lower() == "p") else 0)
        return (-g - (V[m[4]] if len(m) > 4 else 0), V[sq[m[:2]].lower()], m)

    return min(legal, key=k)


while True:
    g = post("/game", {})
    if g["status"] == "done":
        break
    while g["status"] == "your_move":
        g = post("/move", {"game": g["game"], "move": pick(g["fen"], g["legal_moves"])})
    print("game %s: %s by %s" % (g["game"], g["outcome"], g["reason"]), file=sys.stderr)
print("done: %s won, %s drawn, %s lost" % (g.get("wins"), g.get("draws"), g.get("losses")), file=sys.stderr)
