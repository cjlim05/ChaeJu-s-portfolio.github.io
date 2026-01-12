import os
import re

css_files = [
    "src/experience/persol.css",
    "src/experience/hdmid.css",
    "src/experience/military.css",
    "src/experience/swacademy.css",
    "src/projects/chanjurun.css",
    "src/projects/newrodiversity.css",
    "src/projects/iyank.css",
    "src/projects/chungiham.css",
    "src/award/swarmy.css",
    "src/award/hecto.css"
]

base_path = "/Users/chaeju/Desktop/개인/취업/포트폴리오/portfolio"

def clean_css(file_path):
    full_path = os.path.join(base_path, file_path)
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        return

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove :root and body blocks
    content = re.sub(r":root\s*{[^}]*}", "", content, flags=re.DOTALL)
    content = re.sub(r"body\s*{[^}]*}", "", content, flags=re.DOTALL)
    
    # Remove the "GLOBAL VARIABLES" comment header if it's there
    content = re.sub(r"/\* =+.*?GLOBAL VARIABLES.*?=+\s*\*/", "", content, flags=re.DOTALL)
    content = re.sub(r"/\* =+.*?PAGE WRAPPER.*?=+\s*\*/", "", content, flags=re.DOTALL)

    # 2. Remove all box-shadow properties
    content = re.sub(r"\s*box-shadow:[^;]+;", "", content)

    # 3. Clean up hovers: Keep only color/border-color changes
    # This is trickier with regex. Let's focus on removing transform, scale, translate, and non-link background changes.
    
    # Remove transform and scale from hovers
    content = re.sub(r"(\.[\w\s.-]+:hover\s*{[^}]*?)\s*transform:[^;]+;", r"\1", content)
    content = re.sub(r"(\.[\w\s.-]+:hover\s*{[^}]*?)\s*scale\([^)]+\);", r"\1", content)
    
    # Remove background changes from hovers EXCEPT for links (we'll keep it simple: if it's not a known link class, remove it)
    # Actually, the user says "never use hover... except home". 
    # For these subpages, we can probably just remove most hovers or keep them extremely minimal.
    
    # Remove empty hover blocks that might be left over
    content = re.sub(r"\.[\w\s.-]+:hover\s*{\s*(/\*.*?\*/\s*)?}", "", content)
    
    # Final cleanup of excessive newlines
    content = re.sub(r"\n\s*\n\s*\n+", "\n\n", content)
    
    # Ensure "PAGE WRAPPER & SCOPED STYLES" header is at the top once
    if "PAGE WRAPPER & SCOPED STYLES" not in content:
        content = "/* ===============================\n   PAGE WRAPPER & SCOPED STYLES\n =============================== */\n" + content.strip()
    else:
        content = content.strip()

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content + "\n")
    print(f"Cleaned: {file_path}")

for css_file in css_files:
    clean_css(css_file)
