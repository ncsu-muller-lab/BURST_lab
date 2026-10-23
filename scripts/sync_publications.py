def build_publications_html():
    orcid_pubs, orcid_abstracts = fetch_orcid_works()
    manual_pubs, manual_abstracts = load_manual_pubs()

    # Save conference abstracts
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

    # Update in_ORCID_now.json
    orcid_dois = {p["doi"] for p in orcid_pubs if p.get("doi")}
    orcid_titles = {normalize_title(p["title"]) for p in orcid_pubs if p.get("title")}
    in_orcid_now = [
        {"title": p.get("title"), "year": p.get("year"), "doi": p.get("doi"), "journal": p.get("journal")}
        for p in manual_pubs
        if (p.get("doi") and p.get("doi") in orcid_dois) or (normalize_title(p.get("title", "")) in orcid_titles)
    ]
    with open("in_ORCID_now.json", "w", encoding="utf-8") as f:
        json.dump(in_orcid_now, f, indent=2)

    # Merge publications
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
    for p in merged:
        authors_raw = p.get("authors", "")
        authors_html = re.sub(r"\b(Marie Muller|M\. Muller|Muller, M\.)\b", r"<b>\1</b>", authors_raw)
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

    return "\n".join(pub_items_html)
