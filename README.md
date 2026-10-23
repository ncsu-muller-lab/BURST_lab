# BURST Lab — Website & Research Automation

Official website repository for the **Biomedical Ultrasound Research for Structural Tissue Characterization (BURST) Laboratory** at North Carolina State University, directed by **Dr. Marie Muller** (Associate Professor & Interim Director of Graduate Programs, Department of Mechanical & Aerospace Engineering).

Hosted on GitHub Pages at:  
👉 **[https://ncsu-muller-lab.github.io/BURST_lab/](https://ncsu-muller-lab.github.io/BURST_lab/)**

---

## Architecture & Repository Structure

```text
BURST_lab/
├── index.html                      # Home: research thrusts, interactive modal figures, news preview
├── people.html                     # Lab roster: PI profile, postdocs, graduate students, alumni
├── news.html                       # News feed, major awards, and research milestones
├── publications.html               # Generated page: Sub-tabs for Publications vs. Sponsored Grants
├── courses.html                    # Undergraduate & graduate courses taught
├── contact.html                    # Campus location (EB3 Centennial Campus), office, lab rooms
│
├── grants_awarded.json             # Source of truth: Curated federal & foundation grant awards
├── manual_publications.json        # Source of truth: In-press & manually indexed papers
├── in_ORCID_now.json               # Auto-generated: Tracks manual entries verified live on ORCID
├── conference_abstracts_only.json  # Auto-generated: Archived conference presentation abstracts
│
├── scripts/
│   ├── build_research_outputs.py   # Master coordinator: Builds publications.html & syncs top news to index.html
│   ├── sync_publications.py        # ORCID v3 API + Crossref fetcher, deduplication & abstract filter
│   └── sync_grants.py              # Transforms grants_awarded.json into expandable (+) accordions
│
├── .github/workflows/
│   └── sync_publications.yml       # Scheduled GitHub Action (weekly auto-sync + manual trigger)
│
├── assets/
│   ├── css/
│   │   └── style.css               # Central stylesheet (clean typography, mobile nav, modals)
│   └── img/                        # Member headshots (.webp / .jpg), lab figures, branding
└── README.md
```

---

## Automated Publications & Grants Engine

`publications.html` is dynamically generated and maintained by a Python automation pipeline coordinated by `scripts/build_research_outputs.py`.

### How It Works:
1. **ORCID Live Sync:** Queries Dr. Marie Muller's public ORCID record (`0000-0002-5662-0650`) and queries the Crossref API to retrieve full author lists (eliminating generic summary text) and highlight **Marie Muller** in bold.
2. **Abstract Separation:** Automatically detects conference presentation abstracts and separates them into `conference_abstracts_only.json`, ensuring the main publication tab displays only full peer-reviewed journal articles, reviews, and clinical guidelines.
3. **Smart In-Press Merging:** Merges works from `manual_publications.json` (such as upcoming accepted manuscripts) with ORCID records, deduplicating entries by normalized DOI and title. When an entry is confirmed live on ORCID, it is archived to `in_ORCID_now.json`.
4. **Sponsored Grants Integration:** Reads `grants_awarded.json` and renders an interactive, expandable accordion (`+`) view with green funding pills, sponsor agency badges, project dates, and specific aims.
5. **Interactive Sub-Tabs:** Visitors can seamlessly switch between **Publications** (default) and **Sponsored Grants** without page reloads.

---

## Maintenance & Common Workflows

### 1. Adding a New Paper Before It Appears on ORCID
Open `manual_publications.json` and append the new paper to the JSON array:
```json
{
  "title": "Example Paper Title",
  "authors": "Student Name, Collaborator Name, and Marie Muller",
  "journal": "The Journal of the Acoustical Society of America (JASA), In Press",
  "year": 2026,
  "doi": "10.1121/...",
  "type": "Journal"
}
```
*Run the GitHub Action (or wait for the weekly Monday run), and the paper will be formatted and injected into `publications.html` automatically.*

### 2. Adding or Updating Sponsored Grants
Open `grants_awarded.json` and add or edit the grant entry:
```json
{
  "title": "Project Title",
  "status": "Active Grant",
  "agency": "National Institutes of Health (NIH)",
  "amount": "$2,650,000.00",
  "period": "2024 – 2029",
  "pi": "Dr. Marie Muller (NC State MAE) & Co-PI",
  "description": "Project narrative describing clinical or physical motivation.",
  "aims": [
    "Specific Aim 1...",
    "Specific Aim 2..."
  ]
}
```

### 3. Triggering the Sync Manually
1. In your GitHub repository, navigate to the **Actions** tab.
2. Select **Sync Publications and Grants** from the left sidebar.
3. Click **Run workflow** → **Run workflow**. The pipeline completes in ~15–20 seconds and commits the updated `publications.html`.

### 4. Adding or Updating Lab Members (`people.html`)
Member cards follow a standardized visual hierarchy. Add new members inside the appropriate `<div class="people-grid">`:

```html
<div class="person">
  <div class="person-photo">
    <img src="assets/img/firstname-lastname.webp" alt="Full Name" loading="lazy" />
  </div>
  <h4>Full Name</h4>
  <p class="person-role">Ph.D. Student, MAE</p>

  <p class="person-degrees">
    M.S. - Degree Program, University Name<br />
    B.S. - Degree Program, University Name
  </p>

  <p class="person-bio">
    One to two sentences summarizing current thesis focus or experimental technique.<br />
    <span class="person-offhours">Off-hours: hobby1, hobby2, hobby3.</span>
  </p>

  <a class="person-email" href="mailto:unityid@ncsu.edu">unityid@ncsu.edu</a>
</div>
```
*Tip: Place headshot images in `assets/img/` using `.webp` or `.jpg` formatted to a 1:1 square aspect ratio.*

### 5. Moving a Member to Alumni
1. Cut their `<div class="person">` block from the active roster in `people.html`.
2. Add their name and new role to the corresponding list in the `<section class="section">` Alumni block at the bottom of `people.html` (Postdoc Alumni, Ph.D. Alumni, Graduate Alumni, or Undergraduate Alumni).

### 6. Adding or Updating Lab News (`news.html` & Automated `index.html` Preview)
You only need to update **`news.html`**. When the build script runs, it automatically extracts the top 3 newest items and updates the homepage preview on `index.html`.

1. Open `news.html` in GitHub and find `<ul class="news-list">`.
2. Paste the new entry right at the top of the list (so the latest news appears first):

```html
<li class="news-item">
  <div class="news-date">Month Year</div>
  <div class="news-body">
    <span class="news-tag">Publication</span> <!-- e.g., Publication, Grant, Award, Defense, Conference -->
    <h3>Headline of the News Item.</h3>
    <p>Detailed summary description or paper citation details go here.</p>
    <p><a href="[https://doi.org/](https://doi.org/)..." target="_blank" rel="noopener">Read the announcement / paper →</a></p>
  </div>
</li>
```
3. Commit the changes to `news.html`.
4. Trigger the workflow in the **Actions** tab (or wait for the weekly scheduled run) so `build_research_outputs.py` syncs the top 3 items to `index.html`.

---

## Design System & Styling Guidelines

- **Typography:** Uses Google Fonts `IBM Plex Sans` for clear headings and body text, with `IBM Plex Mono` for academic metadata badges, tags, and email labels.
- **Color Palette:** 
  - Primary Background: `#f8fafc` (neutral off-white canvas)
  - Cards & Modals: `#ffffff` with subtle borders (`#e2e8f0`) and elevation shadows
  - University Accent: NC State Red (`#cc0000`) for badges, links, active states, and accents
  - Funding Badges: Emerald Green (`#047857` on `#ecfdf5`) for grant awards
- **Accessibility:** Fully responsive across mobile, tablet, and desktop viewports, with WCAG AA compliant contrast ratios and keyboard-accessible navigation menus and accordions.

---

## Deployment Details

- **Host:** GitHub Pages
- **Branch:** `main` (served from root `/`)
- **DNS / Custom Domain:** Standard GitHub Pages URL. Can be routed to an institutional `*.ncsu.edu` subdomain by configuring a `CNAME` record through NC State MAE Web Administration / OIT.
