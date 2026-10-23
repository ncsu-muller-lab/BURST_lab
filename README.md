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
│   ├── build_research_outputs.py   # Master coordinator: Builds and generates publications.html
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


