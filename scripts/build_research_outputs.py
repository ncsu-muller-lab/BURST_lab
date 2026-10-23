import os
import sys
import re

# Add the 'scripts' folder to Python path so it can import sibling modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import sync_publications
import sync_grants

def main():
    print("=== STEP 1: Building Publications from ORCID & Manual JSON ===")
    pub_html = sync_publications.build_publications_html()

    print("=== STEP 2: Building Grants from grants_awarded.json ===")
    grants_html = sync_grants.render_grants_html()

    print("=== STEP 3: Updating publications.html ===")
    if not os.path.exists("publications.html"):
        print("Error: publications.html not found.")
        sys.exit(1)

    with open("publications.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace publications list
    if pub_html:
        pub_pattern = r'(<ul class="pub-list">)(.*?)(</ul>)'
        content = re.sub(pub_pattern, r'\1\n' + pub_html + r'\n          \3', content, flags=re.DOTALL)

    # Replace grants list
    if grants_html:
        grant_pattern = r'(<ul class="grant-list">)(.*?)(</ul>)'
        content = re.sub(grant_pattern, r'\1\n' + grants_html + r'\n          \3', content, flags=re.DOTALL)

    with open("publications.html", "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully built and synchronized publications and grants!")

if __name__ == "__main__":
    main()
