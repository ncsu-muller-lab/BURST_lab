import os
import sys
import re

# Ensure the scripts folder is in the import path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import sync_publications
import sync_grants

def generate_full_page_html(pub_items_html, grant_items_html):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Publications &amp; Grants — BURST Lab</title>
  <meta name="description" content="Peer-reviewed publications and sponsored research grants at the BURST Lab, NC State MAE." />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="./assets/css/style.css" />
  <style>
    /* View Sub-Tabs */
    .view-tabs {{
      display: inline-flex;
      background: #e2e8f0;
      padding: 4px;
      border-radius: var(--radius);
      margin-top: 1.5rem;
      gap: 4px;
    }}
    .view-tab {{
      background: transparent;
      border: none;
      outline: none;
      padding: 0.6rem 1.4rem;
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--ink-soft);
      border-radius: calc(var(--radius) - 2px);
      cursor: pointer;
      transition: all 0.2s ease;
    }}
    .view-tab:hover {{
      color: var(--ink);
    }}
    .view-tab.active {{
      background: #ffffff;
      color: var(--accent);
      box-shadow: var(--shadow-sm);
    }}

    /* Panes */
    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; animation: fadeIn 0.2s ease-in-out; }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Publications List */
    .pub-list, .grant-list {{
      list-style: none;
      padding: 0;
      margin: 2rem 0 0;
      display: flex;
      flex-direction: column;
      gap: 1.15rem;
    }}
    .pub-item {{
      background: var(--bg-card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 1.35rem 1.65rem;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }}
    .pub-item:hover {{
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: #cbd5e1;
    }}
    .pub-title {{
      font-size: 1.08rem;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.38;
    }}
    .pub-authors {{ font-size: 0.92rem; color: var(--ink-soft); }}
    .pub-authors b {{ color: var(--ink); font-weight: 600; }}
    .pub-journal {{ font-size: 0.88rem; color: var(--ink-muted); font-style: italic; }}
    .pub-links {{
      display: flex;
      align-items: center;
      gap: 0.85rem;
      margin-top: 0.4rem;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .pub-year-badge {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.06em;
      font-weight: 700;
      color: var(--ink-muted);
      background: var(--bg);
      border: 1px solid var(--line);
      padding: 1px 7px;
      border-radius: 3px;
    }}
    .pub-badge {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.7rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent);
      background: var(--accent-light);
      border: 1px solid var(--accent-border);
      padding: 1px 6px;
      border-radius: 3px;
      font-weight: 600;
    }}

    /* Accordion Grants Styling */
    .grant-card {{
      background: var(--bg-card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }}
    .grant-card:hover {{
      border-color: #cbd5e1;
      box-shadow: var(--shadow-md);
    }}
    .grant-header {{
      padding: 1.25rem 1.65rem;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 1.25rem;
      cursor: pointer;
      user-select: none;
    }}
    .grant-header-left {{ flex: 1; }}
    .grant-title {{
      font-size: 1.08rem;
      font-weight: 600;
      color: var(--ink);
      line-height: 1.4;
      margin-bottom: 0.5rem;
    }}
    .grant-meta {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.65rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    .grant-badge {{
      font-size: 0.7rem;
      color: var(--accent);
      background: var(--accent-light);
      border: 1px solid var(--accent-border);
      padding: 1px 7px;
      border-radius: 3px;
      font-weight: 600;
    }}
    .grant-amount {{
      color: #047857;
      background: #ecfdf5;
      border: 1px solid #a7f3d0;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 3px;
    }}
    .grant-agency {{
      color: var(--ink-muted);
      background: var(--bg);
      border: 1px solid var(--line);
      padding: 1px 7px;
      border-radius: 3px;
      font-weight: 600;
    }}
    .grant-toggle-btn {{
      width: 32px;
      height: 32px;
      min-width: 32px;
      border-radius: 50%;
      border: 1px solid var(--accent-border);
      background: var(--accent-light);
      color: var(--accent);
      font-size: 1.25rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      line-height: 1;
    }}
    .grant-card.is-expanded .grant-toggle-btn {{
      background: var(--accent);
      color: #ffffff;
      border-color: var(--accent);
      transform: rotate(45deg);
    }}
    .grant-body {{
      display: none;
      padding: 0 1.65rem 1.4rem;
      border-top: 1px solid #f1f5f9;
      margin-top: 0.5rem;
      padding-top: 1.25rem;
      font-size: 0.94rem;
      line-height: 1.7;
      color: var(--ink-soft);
    }}
    .grant-card.is-expanded .grant-body {{
      display: block;
      animation: fadeIn 0.2s ease;
    }}
    .grant-detail-line {{
      margin-bottom: 0.85rem;
      font-size: 0.9rem;
      color: var(--ink);
    }}
    .grant-detail-line b {{ color: var(--ink); }}
  </style>
</head>
<body>

  <header class="site-header">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="index.html">
        <small>BURST Lab · NC State MAE</small>
        <b>Biomedical Ultrasound Research for Structural Tissue Characterization</b>
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links">Menu</button>
      <ul class="nav-links" id="nav-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="people.html">People</a></li>
        <li><a href="news.html">News &amp; Updates</a></li>
        <li><a class="active" href="publications.html">Publications</a></li>
        <li><a href="courses.html">Courses</a></li>
        <li><a href="contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>

    <header class="page-header">
      <div class="wrap">
        <span class="eyebrow">Research &amp; Funding</span>
        <h1 id="page-heading">Publications.</h1>
        <p id="page-subtext">
          Peer-reviewed journal articles, conference papers, and guidelines from our lab, sorted with the latest research first. You can also view verified citation records on <a href="https://orcid.org/0000-0002-5662-0650" target="_blank" rel="noopener">ORCID (0000-0002-5662-0650) ↗</a> and <a href="https://scholar.google.com/citations?user=9_iPoNoAAAAJ&hl=en&oi=ao" target="_blank" rel="noopener">Google Scholar ↗</a>.
        </p>

        <!-- SUB-TABS (Publications vs Grants) -->
        <div class="view-tabs" role="tablist" aria-label="Publications and Grants">
          <button class="view-tab active" id="tab-btn-pubs" role="tab" aria-selected="true" aria-controls="pane-pubs">
            Publications
          </button>
          <button class="view-tab" id="tab-btn-grants" role="tab" aria-selected="false" aria-controls="pane-grants">
            Sponsored Grants
          </button>
        </div>
      </div>
    </header>

    <section class="section">
      <div class="wrap">

        <!-- TAB 1: PUBLICATIONS -->
        <div class="tab-pane active" id="pane-pubs" role="tabpanel" aria-labelledby="tab-btn-pubs">
          <ul class="pub-list">
{pub_items_html}
          </ul>
        </div>

        <!-- TAB 2: SPONSORED GRANTS -->
        <div class="tab-pane" id="pane-grants" role="tabpanel" aria-labelledby="tab-btn-grants">
          <ul class="grant-list">
{grant_items_html}
          </ul>
        </div>

      </div>
    </section>

  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <h4>BURST Lab</h4>
          <p>Biomedical Ultrasound Research for Structural Tissue Characterization<br/>
          Department of Mechanical &amp; Aerospace Engineering<br/>
          Engineering Building 3, Centennial Campus<br/>
          North Carolina State University<br/>
          Raleigh, NC 27695</p>
        </div>
        <div>
          <h4>Explore</h4>
          <ul>
            <li><a href="index.html">Research</a></li>
            <li><a href="people.html">People</a></li>
            <li><a href="news.html">News &amp; Updates</a></li>
            <li><a href="publications.html">Publications</a></li>
            <li><a href="courses.html">Courses</a></li>
            <li><a href="contact.html">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4>External</h4>
          <ul>
            <li><a href="https://orcid.org/0000-0002-5662-0650" target="_blank" rel="noopener">ORCID Profile ↗</a></li>
            <li><a href="https://scholar.google.com/citations?user=9_iPoNoAAAAJ&hl=en&oi=ao" target="_blank" rel="noopener">Google Scholar ↗</a></li>
            <li><a href="https://tarheels.live/ultrasonc/" target="_blank" rel="noopener">ULTRASONC ↗</a></li>
            <li><a href="https://www.mae.ncsu.edu/" target="_blank" rel="noopener">NC State MAE ↗</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 BURST Lab · NC State University</span>
        <span><a href="https://accessibility.ncsu.edu/" target="_blank" rel="noopener">Accessibility</a> · <a href="https://www.ncsu.edu/privacy/" target="_blank" rel="noopener">Privacy</a></span>
      </div>
    </div>
  </footer>

  <script>
    const pubBtn = document.getElementById('tab-btn-pubs');
    const grantBtn = document.getElementById('tab-btn-grants');
    const pubPane = document.getElementById('pane-pubs');
    const grantPane = document.getElementById('pane-grants');
    const heading = document.getElementById('page-heading');
    const subtext = document.getElementById('page-subtext');

    pubBtn.addEventListener('click', () => {{
      pubBtn.classList.add('active');
      pubBtn.setAttribute('aria-selected', 'true');
      grantBtn.classList.remove('active');
      grantBtn.setAttribute('aria-selected', 'false');

      pubPane.classList.add('active');
      grantPane.classList.remove('active');

      heading.textContent = 'Publications.';
      subtext.innerHTML = 'Peer-reviewed journal articles, conference papers, and guidelines from our lab, sorted with the latest research first. You can also view verified citation records on <a href="https://orcid.org/0000-0002-5662-0650" target="_blank" rel="noopener">ORCID (0000-0002-5662-0650) ↗</a> and <a href="https://scholar.google.com/citations?user=9_iPoNoAAAAJ&hl=en&oi=ao" target="_blank" rel="noopener">Google Scholar ↗</a>.';
    }});

    grantBtn.addEventListener('click', () => {{
      grantBtn.classList.add('active');
      grantBtn.setAttribute('aria-selected', 'true');
      pubBtn.classList.remove('active');
      pubBtn.setAttribute('aria-selected', 'false');

      grantPane.classList.add('active');
      pubPane.classList.remove('active');

      heading.textContent = 'Sponsored Grants.';
      subtext.innerHTML = 'Major federal, foundation, and clinical sponsored research awards granted to Dr. Marie Muller and the BURST Lab.';
    }});

    document.addEventListener('click', (e) => {{
      const header = e.target.closest('.grant-header');
      if (header) {{
        const card = header.closest('.grant-card');
        const isExpanded = card.classList.toggle('is-expanded');
        const btn = card.querySelector('.grant-toggle-btn');
        if (btn) btn.setAttribute('aria-expanded', isExpanded);
      }}
    }});

    const navBtn = document.querySelector('.nav-toggle');
    const navLinks = document.getElementById('nav-links');
    if (navBtn && navLinks) {{
      navBtn.addEventListener('click', () => {{
        const open = navLinks.classList.toggle('is-open');
        navBtn.setAttribute('aria-expanded', open);
      }});
    }}
  </script>
</body>
</html>
"""

def update_index_news():
    """Extracts top 3 news items from news.html and updates index.html."""
    if not os.path.exists("news.html") or not os.path.exists("index.html"):
        return

    with open("news.html", "r", encoding="utf-8") as f:
        news_html = f.read()

    # Find all <li class="news-item">...</li> blocks
    items = re.findall(r'(<li class="news-item">.*?</li>)', news_html, flags=re.DOTALL)
    if not items:
        return

    top_3_items = "\n".join(items[:3])

    with open("index.html", "r", encoding="utf-8") as f:
        index_html = f.read()

    # Replace <ul class="news-list"> in index.html with the top 3 items
    pattern = r'(<ul class="news-list">)(.*?)(</ul>)'
    updated_index = re.sub(pattern, r'\1\n' + top_3_items + r'\n        \3', index_html, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated_index)

    print("Successfully synced the top 3 news items to index.html!")

def main():
    print("=== STEP 1: Building Publications from ORCID & Manual JSON ===")
    pub_html = sync_publications.build_publications_html()

    print("=== STEP 2: Building Grants from grants_awarded.json ===")
    grants_html = sync_grants.render_grants_html()

    print("=== STEP 3: Writing full publications.html from scratch ===")
    full_html = generate_full_page_html(pub_html, grants_html)
    with open("publications.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("Successfully built publications.html!")

    print("=== STEP 4: Syncing top 3 news items to index.html ===")
    update_index_news()

if __name__ == "__main__":
    main()
