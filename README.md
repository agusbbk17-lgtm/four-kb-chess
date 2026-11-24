# four-kb-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/agusbbk17-lgtm/four-kb-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/agusbbk17-lgtm/four-kb-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine for make.fun's "Build the strongest chess engine in 4 KB of Python"
bounty. `main.py` is 4,025 bytes as committed: the readable source, `engine.py`
(12,501 bytes), packed by the kit's own `makefun compress` command.

Board: a 0x88 mailbox, moves packed into one integer, Zobrist hashing from a fixed
linear congruence, and a make/unmake stack that restores every square and field a
move touched. Search: negamax with principal-variation windows, iterative
deepening under 25,000 nodes a move (an iteration past the budget is dropped
whole), a transposition table with depth and bound flags, quiescence over
captures and promotions that answers a check with every evasion, check
extensions, killer and history ordering, MVV-LVA capture sorting, and the
fifty-move draw rule. Eval: material plus piece-square tables, the king's table
tapered between middlegame and endgame by the material left, and a bishop-pair
bonus. It searches to a node count and never to a clock, so one position always
gives one move and a replay reproduces every choice in it.

Checked locally: perft on the start position gives 20, 400, 8,902 and 197,281 at
depths 1..4, and a seeded fuzz comparing the engine's legal move list, check
flag, king squares, en-passant square, castling rights and fifty-move clock
against `python-chess` ply by ply over whole random games reports no failures.
No practice Elo has been measured for this build yet, so none is claimed here;
the number the site reports for the entry stands until a real trial says
otherwise.

## Run it

```sh
# The env serves the game in play; the engine answers it move for move.
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=df1f97fc&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
