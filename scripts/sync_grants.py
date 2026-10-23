import json
import os

def render_grants_html():
    if not os.path.exists("grants_awarded.json"):
        return ""
        
    with open("grants_awarded.json", "r", encoding="utf-8") as f:
        grants = json.load(f)
        
    cards = []
    for g in grants:
        title = g.get("title", "")
        status = g.get("status", "Grant")
        agency = g.get("agency", "")
        amount = g.get("amount", "")
        period = g.get("period", "")
        pi = g.get("pi", "")
        desc = g.get("description", "")
        aims = g.get("aims", [])

        amount_html = f'<span class="grant-amount">{amount}</span>' if amount else ''
        period_html = f'<span>{period}</span>' if period else ''
        agency_html = f'<span class="grant-agency">{agency}</span>' if agency else ''
        
        aims_html = ""
        if aims:
            aims_items = "".join([f"<li>{a}</li>" for a in aims])
            aims_html = f"<ul>{aims_items}</ul>"

        card = f"""            <li class="grant-card">
              <div class="grant-header">
                <div class="grant-header-left">
                  <div class="grant-title">{title}</div>
                  <div class="grant-meta">
                    <span class="grant-badge">{status}</span>
                    {agency_html}
                    {amount_html}
                    {period_html}
                  </div>
                </div>
                <button class="grant-toggle-btn" aria-label="Expand grant details">+</button>
              </div>
              <div class="grant-body">
                <div class="grant-detail-line"><b>Investigators:</b> {pi}</div>
                <div class="grant-detail-line"><b>Funding Agency:</b> {agency}</div>
                <p>{desc}</p>
                {aims_html}
              </div>
            </li>"""
        cards.append(card)

    return "\n".join(cards)

if __name__ == "__main__":
    print(render_grants_html())
