# How to update the lab website

Everything on this site is updated by editing small text files on GitHub, **directly in
your web browser** — no software to install, no coding. After you save ("commit") a
change, the site rebuilds itself automatically and goes live in about 1–2 minutes.

All of the steps below start at the repository page:
**https://github.com/mvpe-lab/mvpe-lab.github.io**

---

## Add a news item

1. Go to the folder `src/content/news/` in the repository.
2. Open `_TEMPLATE.md` to see the format (don't edit the template itself).
3. Click **Add file → Create new file** (top-right of the folder view).
4. Name the file with the date and a short slug, e.g. `2026-07-15-apec-paper.md`.
5. Paste this and fill it in:

   ```
   ---
   title: "Paper accepted at APEC 2027"
   date: 2026-07-15
   ---

   Our paper on single-stage MMCs was accepted at APEC 2027. Congratulations to the team!
   ```

6. Click **Commit changes...** → **Commit changes**. Done — the item appears at the top
   of the Home page news feed.

**To add a photo to a news item:** first upload the photo (see "Upload photos" below)
into `public/images/news/`, then add one line to the news file's top section:
`image: /images/news/your-photo.jpg`

**To embed a YouTube video:** paste the video's embed code (YouTube → Share → Embed)
into the body of the news file.

---

## Add a student / group member

1. Go to `src/content/people/`.
2. Open `_TEMPLATE-student.md` and copy its contents.
3. Click **Add file → Create new file**, name it like `jane-doe.md`.
4. Paste the template, fill in the fields (name, role, etc.), and delete the comment
   lines. Roles are grouped automatically on the Team page (PhD Students, MSc
   Students, etc.).
5. Commit. To add their photo, see below — photos go in `public/images/people/` and the
   file then needs the line `photo: /images/people/jane-doe.jpg`.

**When someone graduates:** edit their file, change `role:` to `"Alumni"` and add a
line like `note: "MSc 2028 — now at Tesla"`. They move to the Alumni list automatically.

---

## Upload photos

1. Go to the right folder: `public/images/people/` (portraits),
   `public/images/news/` (news photos), or `public/images/research/` (research figures).
2. Click **Add file → Upload files**, drag the photo in, and commit.
3. Reference it from a news/people/research file as `/images/people/filename.jpg`
   (the `public` part is dropped).

Tips: use lowercase filenames with hyphens (no spaces), and resize portraits to roughly
800×1000 pixels before uploading so pages load fast. Portraits display in a 4:5
(portrait) crop.

---

## Change the home-page banner photos

The photo strip in the red banner shows **every image in `public/images/home/`**, in
filename order (e.g. `prototype-1.jpg`, `prototype-2.jpg`). To change it:

- **Add a photo** — upload a landscape photo to `public/images/home/`. One to three
  photos look best; they share the row equally.
- **Remove a photo** — delete its file from that folder.
- **Reorder** — rename files so they sort in the order you want.

Landscape photos around 1400 px wide and under ~400 KB keep the page fast.

---

## Edit research areas

Each research theme is one file in `src/content/research/`. Click the file → click the
pencil icon → edit → commit. The `order:` number controls the order on the page. Add a
new area by copying `_TEMPLATE-research-area.md`.

---

## Publications (automatic)

The Publications page updates itself **every Monday** from your Google Scholar profile
(falling back to the OpenAlex database if Scholar blocks the request). You never need
to edit it.

To force an immediate update (e.g. a new paper just appeared on Scholar):

1. Go to the **Actions** tab of the repository.
2. Click **Refresh publications** in the left sidebar.
3. Click **Run workflow → Run workflow**. The site updates a couple of minutes later.

---

## Other common edits

| What | Where |
| --- | --- |
| Recruiting banner text on the Home page | `src/pages/index.astro` (the `callout` block) |
| Hero headline / tagline | `src/pages/index.astro` (the `hero` block) |
| Footer contact info | `src/layouts/Base.astro` |
| Research page intro paragraph | `src/pages/research.astro` |
| Colours / fonts / spacing | `src/styles/global.css` |

If a change ever breaks the build, the site simply keeps showing the previous version —
check the **Actions** tab for a red ✗, open the failed run to see what went wrong, or
revert your last commit (file → History → revert).
