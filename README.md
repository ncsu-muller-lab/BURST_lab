# BURST Lab — Website & Research Automation

Official website repository for the **Biomedical Ultrasound Research for Structural Tissue Characterization (BURST) Laboratory** at North Carolina State University, directed by **Dr. Marie Muller** (Associate Professor & Interim Director of Graduate Programs, Department of Mechanical & Aerospace Engineering).

Hosted on GitHub Pages at:  
👉 **[https://ncsu-muller-lab.github.io/BURST_lab/](https://ncsu-muller-lab.github.io/BURST_lab/)**

---

## Architecture & Repository Structure

---

## Automated Publications & Grants Engine

`publications.html` is dynamically maintained by a Python automation pipeline coordinated by `scripts/build_research_outputs.py`.

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


---

### Step to Update:
1. Open **`README.md`** on GitHub.
2. Click the **pencil icon** to edit.
3. Replace the old text with the markdown above and click **Commit changes**.
