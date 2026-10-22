import json
import re
import urllib.request
import os

ORCID_ID = "0000-0002-5662-0650"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "NCState-BURST-Lab-Website/1.0"
}

def clean_doi(doi_str):
    if not doi_str:
        return ""
    doi_str = str(doi_str).strip()
    doi_str = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi_str, flags=re.I)
    return doi_str.lower().strip()

def fetch_orcid_works():
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching ORCID works: {e}")
        return []

    pubs = []
    group = data.get("group", [])
    for g in group:
        summaries = g.get("work-summary", [])
        if not summaries:
            continue
        item = summaries[0]
        
        # Title
        title = item.get("title", {}).get("title", {}).get("value", "").strip()
        if not title:
            continue
            
        # Year
        pub_date = item.get("publication-date") or {}
        year = pub_date.get("year", {}).get("value")
        try:
            year = int(year) if year else 0
        except ValueError:
            year = 0
            
        # Journal
        journal = item.get("journal-title", {}).get("value", "") if item.get("journal-title") else ""
        
        # Type
        work_type = item.get("type", "").replace("_", " ").title()
        
        # DOI
        doi = ""
        ext_ids = item.get("external-ids", {}).get("external-id", [])
        for eid in ext_ids:
            if eid.get("external-id-type", "").lower() == "doi":
                doi = clean_doi(eid.get("external-id-value", ""))
                break
                
        pubs.append({
            "title": title,
            "authors": "Marie Muller et al.", # Summary level authors
            "journal": journal,
            "year": year,
            "doi": doi,
            "type": work_type or "Publication"
        })
    return pubs

def load_manual_pubs():
    if not os.path.exists("manual_publications.json"):
        return []
    try:
        with open("manual_publications.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                d["doi"] = clean_doi(d.get("doi", ""))
            return data
    except Exception as e:
        print(f"Error loading manual_publications.json: {e}")
        return []

def main():
    orcid_pubs = fetch_orcid_works()
    manual_pubs = load_manual_pubs()
    
    # Merge and deduplicate by DOI, then title
    seen_dois = set()
    seen_titles = set()
    merged = []
    
    # Priority to manual_pubs for rich author info & custom in-press titles
    for p in manual_pubs:
        doi = p.get("doi")
        title_key = re.sub(r"\W+", "", p.get("title", "").lower())
        if doi:
            seen_dois.add(doi)
        if title_key:
            seen_titles.add(title_key)
        merged.append(p)
        
    for p in orcid_pubs:
        doi = p.get("doi")
        title_key = re.sub(r"\W+", "", p.get("title", "").lower())
        if doi and doi in seen_dois:
            continue
        if title_key and title_key in seen_titles:
            continue
            
        if doi:
            seen_dois.add(doi)
        if title_key:
            seen_titles.add(title_key)
        merged.append(p)
        
    # Sort newest first
    merged.sort(key=lambda x: x.get("year", 0), reverse=True)
    
    # Render items HTML
    pub_items_html = []
    for p in merged:
        authors_html = p.get("authors", "").replace("Marie Muller", "<b>Marie Muller</b>")
        doi_val = p.get("doi")
        doi_link = f'<a href="https://doi.org/{doi_val}" target="_blank" rel="noopener">DOI ↗</a>' if doi_val else ""
        year_str = str(p.get("year")) if p.get("year") else "Recent"
        
        item_html = f"""          <li class="pub-item">
            <div class="pub-title">{p.get("title")}</div>
            <div class="pub-authors">{authors_html}</div>
            <div class="pub-journal">{p.get("journal", "")}</div>
            <div class="pub-links">
              <span class="pub-year-badge">{year_str}</span>
              <span class="pub-badge">{p.get("type", "Journal")}</span>
              {doi_link}
            </div>
          </li>"""
        pub_items_html.append(item_html)
        
    full_list_html = "\n".join(pub_items_html)
    
    # Replace the list in publications.html
    if os.path.exists("publications.html"):
        with open("publications.html", "r", encoding="utf-8") as f:
            content = f.read()
            
        pattern = r'(<ul class="pub-list">)(.*?)(</ul>)'
        replacement = r'\1\n' + full_list_html + r'\n        \3'
        updated = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open("publications.html", "w", encoding="utf-8") as f:
            f.write(updated)
        print("Successfully updated publications.html with merged publications!")

if __name__ == "__main__":
    main()
