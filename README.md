# Muller Lab — Website

A static, multi-page website for the Ultrasonic Material Characterization Lab, designed to be hosted on GitHub Pages.

## What's here

```
muller-lab/
├── index.html         # Home: hero, research areas, news preview, ULTRASONC callout
├── people.html        # PI, postdocs, grad students, alumni
├── news.html          # Full news feed
├── courses.html       # Courses taught
├── contact.html       # Contact details
├── assets/
│   ├── css/style.css  # All styling lives here — one file
│   └── img/
│       └── marie-muller.jpg
└── README.md
```

There is **no build step**. No npm, no compiler, no framework. You can edit any HTML file in a text editor (or directly on github.com) and the change is live as soon as you commit it.

---

## Deploying to GitHub Pages

### One-time setup (about 10 minutes)

1. Create a free GitHub account at github.com if you don't have one.
2. On github.com, click **New repository** in the top right.
   - Repository name: `muller-lab` (or whatever you like)
   - Visibility: **Public**
   - Do **not** initialize it with a README (you already have one).
3. On your repo page, click **uploading an existing file** and drag in everything from this folder (the four `.html` files, this `README.md`, and the `assets/` folder).
4. Commit the upload.
5. In your repo, go to **Settings → Pages** (left sidebar).
6. Under **Source**, choose **Deploy from a branch**, and set the branch to `main` and folder to `/ (root)`. Save.
7. Wait ~1 minute. GitHub will give you a URL like `https://<your-username>.github.io/muller-lab/`. That's the live site.

### Pointing your real domain at it (optional, later)

NC State IT typically owns `*.ncsu.edu` subdomains. If you want to keep `muller.wordpress.ncsu.edu` or get something like `muller.mae.ncsu.edu`, you'll need to ask the MAE web admin or NC State IT to set up a CNAME pointing at your `github.io` URL. Until then, the `github.io` URL works perfectly.

---

## Editing the site

The whole site is plain HTML and CSS. There is no database. To change something:

### To edit text (e.g., a student bio, a news item)

1. Go to your repo on github.com.
2. Click the file you want to edit (e.g., `people.html`).
3. Click the pencil icon in the top right.
4. Edit the text directly in the browser. The structure looks like this:
   ```html
   <div class="person">
     <div class="person-photo">...</div>
     <h4>Student Name</h4>
     <p>Bio paragraph goes here.</p>
     <span class="person-email">email@ncsu.edu</span>
   </div>
   ```
5. Scroll down, write a short commit message like "Update Caleb's bio", and click **Commit changes**.
6. The live site updates in ~30 seconds.

### To add a new news item

Open `news.html` and find the `<ul class="news-list">` block. Copy any existing `<li class="news-item">...</li>` and paste it as the **first** item in the list (newest at top). Edit the date, tag, headline, and body.

Then do the same on `index.html` if you want it to appear in the home-page preview.

### To add a new lab member

Open `people.html` and find the section you need (Postdocs, Grad Students, Undergrads). Copy an existing `<div class="person">...</div>` block, paste it inside the same `<div class="people-grid">`, and edit the photo URL, name, bio, and email.

For the photo: upload it to `assets/img/` in your repo, then point at it like `assets/img/firstname-lastname.jpg`.

### To move someone to alumni

Cut their `<div class="person">` block out and add their name to the alumni list at the bottom of `people.html`. (Already done for Austin McCandless and Ben Nguyen.)

---

## Notes

- **Photos.** The lab member photos and research figures currently load from the existing WordPress site. They will keep working as long as that site stays up — but for permanence, you should download each one, place it in `assets/img/`, and update the `src=` attributes in the HTML to point at your local copy. Higher-priority for student photos than research figures.
- **Publications.** The Publications nav link goes straight to your Google Scholar profile. If you'd rather have a curated list page, that's an easy addition later.
- **Fonts.** The site uses Fraunces (display serif) and IBM Plex Sans (body), loaded from Google Fonts. They're free and have stable CDN URLs.
- **NC State branding.** The accent color is NC State red, used sparingly for emphasis, links, and a single border line. It's intentionally restrained so the site feels like a research lab rather than a marketing brochure.
- **Accessibility.** Color contrast is WCAG AA, the navigation works without JavaScript (the JS is only for the mobile menu toggle), and `prefers-reduced-motion` is respected.

---

## Things I didn't fill in (gaps you can plug)

- Office room number in Engineering Building 3 (only the building was given).
- A phone number, if you want one published.
- Lab room number, if you want to list it separately from your office.
- A few research figures could use higher-resolution replacements.
