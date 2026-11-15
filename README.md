# mahean-site

Personal site of Mahean Magamemnon. One self-contained HTML file: open `index.html` in a browser, or host it anywhere (GitHub Pages, Netlify, Vercel).

## Layout

```
index.html                  the built site (everything embedded, no dependencies)
src/
  content.py                all the writing: bio, interests, notes
  build.py                  builds index.html from the pieces below
  base.html                 page shell: folders sidebar, bookshelf, notes
  orig_refine.css           styles layered on the original design
  app.js                    hash navigation + the two interactive figures
  assets/photos/            Wikimedia Commons photos (credits in meta.json and on the page)
  art/                      background artwork and the scripts that made it
```

## Edit and rebuild

Edit `src/content.py` (or the CSS/JS), then:

```bash
pip install pillow
python3 src/build.py index.html
```

## Credits

Photos are from Wikimedia Commons under their stated licences (CC BY, CC BY-SA, public domain). Each one is credited under the image on the page, with a link to its source.
