# Order of Battle

A WWII audiobook finder for Dad. He sorts a shelf of real WWII nonfiction, and it learns
his taste, finds books he hasn't come across, and points to places to listen besides
Audible. Built for a listener with weak eyes: big type, a text-size control, a bright
yellow highlight, and full arrow-key control so he never needs the touchpad. On a phone
the answer buttons stay pinned to the bottom of the screen.

## Running it

Open `index.html` in a browser. Run `node build.js` after editing `src/artifact.html`;
`index.html` is generated from it. Opened as a plain file, it saves to that browser only
and the Claude features (descriptions, finding books) are off. The published claude.ai
artifact has both.

## Phone app (`phone/`)

A simpler version for Dad's Android phone: one book at a time with a large description,
and four big buttons: **Good Book**, **Read, Don't Remember**, **Pass**, and **Save /
Haven't Heard**. No tags or scores on screen. A **Saved** tab lists what he wants to hear,
led by confirmed audiobooks with a **Get it on Audible** button, then BARD; library
apps (Libby) come last, since they depend on a working library card. Books with a
confirmed Audible edition always rank ahead of books without one, and each card says
which it is. Audiobook status lives in `phone/curation.json` under `audio`.

- **Install:** open https://erinfinnegan.github.io/order-of-battle/phone/ in Chrome on the
  phone, then menu (⋮) → **Add to Home screen** / **Install app**. It opens full-screen
  from its own icon and works offline.
- **Shelf:** built from his answers in the desktop app. Books his answers say won't land
  are dropped, and new picks are added, in `phone/curation.json`. The phone keeps
  learning as he answers and re-orders what's left.
- **Answers stay on the phone** until he taps **Send my answers to Erin** on the Saved
  tab. That opens Android's share sheet with a readable list plus a code. Paste the
  whole message into the desktop app's **Find more** box and press either button to
  bring the answers in.
- **Refreshing his shelf:** export the shared database (ratings/, extra/, about/ as JSON
  files), then run `node tools/build-phone-data.js <export-dir>` and push. The phone
  picks up the new list the next time he opens the app. `tools/make-icons.py` redraws
  the icons.

## The tabs

- **Sort the shelf**: one book at a time, or the whole list. Each card shows a short
  description of what the book covers. Seven answers in two groups:
  - *He's read it*: Liked it · It was OK · Didn't like it · Read it, don't remember
  - *He hasn't*: Haven't heard it · Not this book · Not this battle

  Keyboard: arrows to move (down from the bottom row reaches **Skip for now**), Enter to
  choose, 1–7 to answer directly, S to skip, Backspace to undo. After a thumbs-down
  there's an optional "why" (felt like the news, too dry, bad narrator…). The whole-list
  view filters by answer, so you can go back through, say, every "Not this book".
- **Up next**: unheard books ranked by predicted match, with reasons and search links
  for Libby, Hoopla, Libro.fm, Chirp, Open Library and BARD. The **Tonight** box narrows
  the list to one battle (e.g. "Leyte Gulf") and skips subjects he doesn't want today
  (e.g. "8th Air Force"). Tonight's choices never change what it has learned. Filters:
  new (2021+), older gems (pre-1980), authors he likes, re-listens.
- **His list**: everything he's marked "Haven't heard it", in large print, best match
  first, plus the ones he read but doesn't remember.
- **Authors**: his authors ranked by verdicts, with their unheard books; Claude can look
  up what else they wrote.
- **What it's learned**: what draws him in or puts him off, the reasons he's given,
  **In his own words** (things he's said about his taste, which Claude reads every time
  it looks for books), and a plain-English description of his taste.
- **Find more**: Claude suggests books (new, older, by favorite authors, or on a battle)
  that aren't on the shelf yet. Paste a list (his Audible library, typed-up paperbacks)
  to mark books read, or paste any web list (a Goodreads shelf, say) to add its books
  for sorting. A shelf photo also works.
- **Where to listen**: NLS Talking Books / BARD first (free with a vision impairment, and
  it has many old WWII recordings), then library apps and paid options.

## How it learns

Every book has features: its feel (up close like an action movie, or big picture like
watching the news), theater, branch, kind of book, author, the era it was written in, and
subject tags (battles, aircraft, ships). Each answer moves an affinity score for that
book's features, shrunk toward neutral so one book never becomes a rule:

| answer | effect |
| --- | --- |
| Liked it | +1 on every feature |
| It was OK | +0.1 |
| Didn't like it | −1 |
| Read it, don't remember | +0.2 |
| Already read (from a pasted list) | +0.25 |
| Not this book | −0.2, a light nudge |
| Not this battle | −1 on its subjects and −0.3 on its theater only |
| Haven't heard it | no taste signal; goes on his list |

A book's match blends its feature scores, with author and feel weighted highest.

## The catalog

About 240 seed titles live as a pipe-delimited block at the top of the script:

```
Title|Author|Year|Theater|Branch|Form|tags
```

They were put together from memory as a starting set; spot-check details before buying.
The up-close / big-picture feel for seed titles is set in `FEEL_BIG` and `FEEL_CLOSE`.
Books Claude finds or you paste go into the shared store, not the file.

## Data (when published)

| path | shape |
| --- | --- |
| `ratings/<book-id>` | `{s: up\|side\|down\|forgot\|unread\|nope\|nobattle\|read, reasons: [], at}` |
| `extra/<book-id>` | a book added by Claude, a paste, or a photo, with `about` (description) and `why` |
| `about/<book-id>` | `{text, at}`: Claude's short description of a seed book, written on first view |
| `config/notes` | `{text, at}`: his taste in his own words |
| `config/summary` | `{text, at}`: a plain-English description of his taste |

His current to-hear list, in large print for a phone: https://erinfinnegan.github.io/order-of-battle/to-hear.html (source: `to-hear.html`; the same list as a table is in [TO-HEAR.md](TO-HEAR.md)).
