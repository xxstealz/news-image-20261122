[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/xxstealz/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/xxstealz/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# The Daily Globe — Sunday, 22 November 2026

One image summing up the world's news of Sunday 22 November 2026, drawn as a
newspaper front page: a lead story plus 11 illustrated story cards across
seven regions. Every story below was reported on 22 November 2026.

## The stories

1. **COP31 collapses (Antalya)** — No climate deal: nearly 200 nations leave
   Antalya without a pact after two weeks of talks and two days of overtime;
   fossil fuels the breaking point. *(UN News, CNN, Reuters)*
2. **Warship sunk in Benghazi (Libya)** — Suspected Ukrainian sea drones hit
   the Russian corvette Merkury; it capsizes, 10 hurt. *(Reuters, AP, CNN)*
3. **14 missing near Kyiv (Ukraine)** — A Russian drone collapses a
   five-storey block in Dymer; 2 dead, 9 evacuated. *(Reuters, AP)*
4. **Settler arson in the West Bank** — Cars torched in four villages near
   Ramallah; police open an inquiry, the opposition leader calls it
   "terrorism". *(Reuters, CNN)*
5. **Drones hit Khartoum (Sudan)** — Four killed as strikes hit homes and a
   UN building; the army blames Ethiopia — unverified. *(AFP, UN OCHA)*
6. **Poland: second plot vs rapper (Europe)** — Russia "twice tried to kill"
   US-Ukrainian star Kyivstoner; Denmark expelled an attaché. *(AP)*
7. **186 drones in one night (Ukraine)** — Ukraine says it downed 161 of 186
   Russian drones in an overnight barrage. *(Ukraine Air Force, via press)*
8. **Factory fire toll rises (Indonesia)** — 3 dead, 37 missing after a blaze
   at a candy factory in Cikande. *(AP)*
9. **Mercury arrival — with a glitch (Space)** — BepiColombo reaches Mercury
   orbit after 8 years; ESA reports a thruster fault. *(Reuters, ESA)*
10. **Youth take to the streets (Europe)** — Cost-of-living protests in 400
    cities across 20+ European countries. *(press reports, 22 Nov)*
11. **Shuri Castle rises again (Japan)** — Okinawa celebrates the restored
    hall, seven years after fire destroyed it. *(AP)*
12. **Eisenkot courts Likud (Israel)** — The opposition leader invites
    Netanyahu's party to coalition talks. *(press reports, 22 Nov)*

## How it is made

`draw_entry.py` draws `entry.png` (1024×1024, pure PIL, no network, no
random input, no timestamps — two runs write identical bytes). `main.ts`
copies `entry.png` to the output directory.

Run it:

```
python3 draw_entry.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.
