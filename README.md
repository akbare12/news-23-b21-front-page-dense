# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b21-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b21-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout that hit Asian
markets, the UN chief's call to regulate AI before it's too late, and the US lead
over China falling to a record low — plus 28 more stories, a map of where it
happened, and a date check that keeps out stories from other days.

31 stories · 6 regions · drawn illustrations, not photographs.

## Run

```
python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR (default: out/)
```

`main.py` is stdlib-only: it validates the PNG header (signature, IHDR 1024x1024,
IEND trailer, <= 1 MiB) and copies `entry.png` to the output directory. It never
writes next to itself. `draw.py` (Pillow) regenerates `entry.png` from scratch.
