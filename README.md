# Medium Voltage Power Electronics Laboratory — website

Website of the Medium Voltage Power Electronics Laboratory (Dr. Philippe Gray),
Schulich School of Engineering, University of Calgary.
Live at **https://mvpe-lab.github.io**.

**Updating content (news, people, photos)?** See [HOW-TO-UPDATE.md](HOW-TO-UPDATE.md) —
no coding required.

## Stack

- [Astro](https://astro.build) static site → pure HTML/CSS output, portable to any host
- Hosted on **GitHub Pages**, deployed by `.github/workflows/deploy.yml` on every push
- Publications auto-refresh weekly from **Google Scholar** (OpenAlex fallback) via
  `.github/workflows/refresh-publications.yml` → `scripts/fetch_publications.py` →
  `src/data/publications.json`
- Brand colours follow the
  [University of Calgary brand guidelines](https://www.ucalgary.ca/brand/standards-and-guidelines/colours):
  red `#d6001c`, gold `#ffcd00`

## Structure

```
src/
  content/
    news/        one .md file per news item (template: _TEMPLATE.md)
    people/      one .md file per member   (template: _TEMPLATE-student.md)
    research/    one .md file per research area
  data/
    publications.json   auto-generated — do not edit by hand
  layouts/Base.astro    header, nav, footer
  pages/                index (home + news), team, research, publications, news archive
  styles/global.css     theme
public/
  images/{people,news,research}/   uploaded photos
scripts/
  fetch_publications.py            publications fetcher (Scholar → OpenAlex)
```

## Local development

```sh
npm install
npm run dev        # dev server at http://localhost:4321
npm run build      # production build to dist/
```

Refresh publications locally:

```sh
pip install -r scripts/requirements.txt
python scripts/fetch_publications.py
```

## Moving to UCalgary hosting later

`npm run build` produces a self-contained static site in `dist/` — copy it to any web
server. Update `site` in `astro.config.mjs` to the new URL first so canonical URLs are
correct.
