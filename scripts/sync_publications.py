import json
import re
import urllib.request
import os

ORCID_ID = "0000-0002-5662-0650"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "NCState-BURST-Lab-Website/1.0 (mailto:mmuller2@ncsu.edu)"
}

def clean_doi(doi_str):
    if not doi_str:
        return ""
    doi_str = str(doi_str).strip()
    doi_str = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi_str, flags=re.I)
    return doi_str.lower().strip()

def normalize_title(title_str):
    if not title_str:
        return ""
    return re.sub(r"\W+", "", title_str.lower()).strip()

def is_meeting_abstract(work_type_raw, title, journal, doi):
    """Identifies conference abstracts, presentation summaries, and proceedings."""
    blocked_types = [
        "conference_abstract", 
        "conference_poster", 
        "conference_paper", 
        "lecture_speech", 
        "other"
    ]
    if any(bt in work_type_raw.lower() for bt in blocked_types):
        return True

    combined_text = f"{title} {journal}".lower()
    abstract_signals = [
        "supplement",
        "suppl",
        "_supplement",
        "abstracts of",
        "conference abstract",
        "annual meeting abstract",
        "meeting abstract"
    ]
    if any(sig in combined_text for sig in abstract_signals):
        return True

    if doi:
        url = f"https://api.crossref.org/works/{doi}"
        req = urllib.request.Request(url, headers={"User-Agent": "NCState-BURST-Lab/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8")).get("message", {})
                cr_type = data.get("type", "").lower()
                if cr_type in ["proceedings-article", "component", "dataset"]:
                    return True
                page = data.get("page", "")
                if re.match(r"^A\d+", page, flags=re.I):
                    return True
        except Exception:
            pass

    return False

def fetch_work_contributors(put_code):
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/work/{put_code}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            contributors = data.get("contributors", {}).get("contributor", [])
            names = []
            for c in contributors:
                credit_name = c.get("credit-name", {})
                if credit_name and credit_name.get("value"):
                    names.append(credit_name.get("value").strip())
            if names:
                if len(names) == 1:
                    return names[0]
                elif len(names) == 2:
                    return f"{names[0]} and {names[1]}"
                else:
                    return f"{', '.join(names[:-1])}, and {names[-1]}"
    except Exception:
        pass
    return ""

def fetch_doi_authors(doi):
    if not doi:
        return ""
    url = f"https://api.crossref.org/works/{doi}"
    req = urllib.request.Request(url, headers={"User-Agent": "NCState-BURST-Lab/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            authors = data.get("message", {}).get("author", [])
            names = []
            for a in authors:
                given = a.get("given", "").strip()
                family = a.get("family", "").strip()
                if given and family:
                    names.append(f"{given} {family}")
                elif family:
                    names.append(family)
            if names:
                if len(names) == 1:
                    return names[0]
                elif len(names) == 2:
                    return f"{names[0]} and {names[1]}"
                else:
                    return f"{', '.join(names[:-1])}, and {names[-1]}"
    except Exception:
        pass
    return ""

def fetch_orcid_works():
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching ORCID works: {e}")
        return [], []

    journal_pubs = []
    abstracts_only = []

    group = data.get("group", [])
    for g in group:
        summaries = g.get("work-summary", [])
        if not summaries:
            continue
        item = summaries[0]
        put_code = item.get("put-code")
        
        title = item.get("title", {}).get("title", {}).get("value", "").strip()
        if not title:
            continue
            
        pub_date = item.get("publication-date") or {}
        year = pub_date.get("year", {}).get("value")
        try:
            year = int(year) if year else 0
        except ValueError:
            year = 0
            
        journal = item.get("journal-title", {}).get("value", "") if item.get("journal-title") else ""
        raw_type = item.get("type", "")
        work_type = raw_type.replace("_", " ").title()
        
        doi = ""
        ext_ids = item.get("external-ids", {}).get("external-id", [])
        for eid in ext_ids:
            if eid.get("external-id-type", "").lower() == "doi":
                doi = clean_doi(eid.get("external-id-value", ""))
                break

        if is_meeting_abstract(raw_type, title, journal, doi):
            abstracts_only.append({
                "title": title,
                "journal": journal,
                "year": year,
                "doi": doi,
                "type": "Conference Abstract"
            })
            continue
        
        authors = ""
        if put_code:
            authors = fetch_work_contributors(put_code)
        if not authors and doi:
            authors = fetch_doi_authors(doi)
        if not authors:
            authors = "Marie Muller"

        journal_pubs.append({
            "title": title,
            "authors": authors,
            "journal": journal,
            "year": year,
            "doi": doi,
            "type": work_type or "Journal"
        })
        
    return journal_pubs, abstracts_only

def load_manual_pubs():
    if not os.path.exists("manual_publications.json"):
        return [], []
    try:
        with open("manual_publications.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            journal_list = []
            abstract_list = []
            for d in data:
                d["doi"] = clean_doi(d.get("doi", ""))
                t_lower = d.get("type", "").lower()
                if "abstract" in t_lower:
                    abstract_list.append(d)
                else:
                    journal_list.append(d)
            return journal_list, abstract_list
    except Exception as e:
        print(f"Error loading manual_publications.json: {e}")
        return [], []

def build_publications_html():
    """Main function called by build_research_outputs.py to build the list."""
    orcid_pubs, orcid_abstracts = fetch_orcid_works()
    manual_pubs, manual_abstracts = load_manual_pubs()

    # 1. Save conference abstracts
    all_abstracts = manual_abstracts + orcid_abstracts
    abstract_seen = set()
    deduped_abstracts = []
    for a in all_abstracts:
        t_key = normalize_title(a.get("title", ""))
        doi_key = a.get("doi", "")
        key = doi_key if doi_key else t_key
        if key and key not in abstract_seen:
            abstract_seen.add(key)
            deduped_abstracts.append(a)
    deduped_abstracts.sort(key=lambda x: x.get("year", 0), reverse=True)
    with open("conference_abstracts_only.json", "w", encoding="utf-8") as f:
        json.dump(deduped_abstracts, f, indent=2)

    # 2. Update in_ORCID_now.json
    orcid_dois = {p["doi"] for p in orcid_pubs if p.get("doi")}
    orcid_titles = {normalize_title(p["title"]) for p in orcid_pubs if p.get("title")}
    in_orcid_now = []
    for p in manual_pubs:
        doi = p.get("doi")
        title_key = normalize_title(p.get("title", ""))
        if (doi and doi in orcid_dois) or (title_key and title_key in orcid_titles):
            in_orcid_now.append({
                "title": p.get("title"),
                "year": p.get("year"),
                "doi": p.get("doi"),
                "journal": p.get("journal")
            })
    with open("in_ORCID_now.json", "w", encoding="utf-8") as f:
        json.dump(in_orcid_now, f, indent=2)

    # 3. Merge publications
    seen_dois = set()
    seen_titles = set()
    merged = []
    for p in manual_pubs:
        doi = p.get("doi")
        title_key = normalize_title(p.get("title", ""))
        if doi: seen_dois.add(doi)
        if title_key: seen_titles.add(title_key)
        merged.append(p)

    for p in orcid_pubs:
        doi = p.get("doi")
        title_key = normalize_title(p.get("title", ""))
        if (doi and doi in seen_dois) or (title_key and title_key in seen_titles):
            continue
        if doi: seen_dois.add(doi)
        if title_key: seen_titles.add(title_key)
        merged.append(p)

merged.sort(key=lambda x: x.get("year", 0), reverse=True)

    pub_items_html = []
    divider_inserted = False

    for p in merged:
        year_val = p.get("year", 0)
        try:
            year_int = int(year_val)
        except (ValueError, TypeError):
            year_int = 0

        # Insert a visual divider right below the last 2017 paper
        if year_int < 2017 and not divider_inserted:
            divider_html = """          <li class="pub-divider">
            <span class="pub-divider-line"></span>
            <span class="pub-divider-text">Prior to BURST Lab (Foundational &amp; Postdoctoral Works, 2003 – 2016)</span>
            <span class="pub-divider-line"></span>
          </li>"""
            pub_items_html.append(divider_html)
            divider_inserted = True

        authors_raw = p.get("authors", "")
        authors_html = re.sub(r"\b(Marie Muller|M\. Muller|Muller, M\.)\b", r"<b>\1</b>", authors_raw)
        doi_val = p.get("doi")
        doi_link = f'<a href="https://doi.org/{doi_val}" target="_blank" rel="noopener">DOI ↗</a>' if doi_val else ""
        year_str = str(year_val) if year_val else "Recent"
        badge_type = p.get("type", "Journal")

        item_html = f"""          <li class="pub-item">
            <div class="pub-title">{p.get("title")}</div>
            <div class="pub-authors">{authors_html}</div>
            <div class="pub-journal">{p.get("journal", "")}</div>
            <div class="pub-links">
              <span class="pub-year-badge">{year_str}</span>
              <span class="pub-badge">{badge_type}</span>
              {doi_link}
            </div>
          </li>"""
        pub_items_html.append(item_html)

    return "\n".join(pub_items_html)

if __name__ == "__main__":
    print(build_publications_html())
