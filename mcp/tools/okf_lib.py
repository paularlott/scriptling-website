# Shared helpers for the OKF MCP tools. Lives next to the tool scripts so each
# can `import okf_lib`. All paths are relative to OKF_ROOT (default mcp/okf).
import os
import os.path
import json
import re
import yaml

OKF_ROOT = os.getenv("OKF_ROOT", "mcp/okf")

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def norm(path):
    return (path or "").strip().strip("/")


def root_abs():
    return os.path.abspath(OKF_ROOT)


def resolve(rel):
    """Absolute path for a bundle-relative path, or None if it escapes root."""
    rel = norm(rel)
    root = root_abs()
    full = root if rel == "" else os.path.abspath(os.path.join(root, rel))
    if full != root and not full.startswith(root + os.sep):
        return None
    return full


def bundles():
    # manifest.json is tooling metadata, kept outside the OKF root.
    return json.loads(os.read_file(os.path.dirname(OKF_ROOT) + "/manifest.json"))


def bundle_entries():
    # Uniform bundle listing (with `path`) shared by skb_bundles and skb_list("").
    out = []
    for b in bundles():
        out.append({"name": b["name"], "type": "bundle", "path": b["name"] + "/",
                    "title": b["title"], "description": b.get("description", "")})
    return out


def frontmatter(path):
    raw = os.read_file(path)
    m = FM_RE.match(raw)
    if not m:
        return {}, raw
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def title_desc(path):
    fm, _ = frontmatter(path)
    title = fm.get("title") or os.path.splitext(os.path.basename(path))[0]
    return title, (fm.get("description") or "")


def overview_for(rel_dir):
    # Path to the overview concept for a folder. Bundle roots keep theirs
    # inside (<bundle>/<bundle>.md); subfolders sit beside theirs.
    name = os.path.basename(rel_dir)
    parent = os.path.dirname(rel_dir)
    if parent == "":
        return OKF_ROOT + "/" + name + "/" + name + ".md"
    return OKF_ROOT + "/" + parent + "/" + name + ".md"


def entries_for(rel_dir):
    """Concept files and subfolders in a folder, deduped: a subfolder that has
    an overview .md beside it is represented by that overview, not re-listed."""
    abs_dir = resolve(rel_dir)
    names = sorted(os.listdir(abs_dir))
    md_files = [e for e in names if e.endswith(".md")]
    dirs = [e for e in names if os.path.isdir(abs_dir + "/" + e)]
    md_stems = set(os.path.splitext(e)[0] for e in md_files)
    out = []
    for e in md_files:
        t, d = title_desc(abs_dir + "/" + e)
        rel = (rel_dir + "/" + e) if rel_dir else e
        out.append({"name": e, "type": "file", "path": rel, "title": t, "description": d})
    for e in dirs:
        if e in md_stems:
            continue  # the folder's overview concept already represents it
        ov = abs_dir + "/" + e + ".md"
        t, d = (title_desc(ov) if os.path.isfile(ov) else (e.replace("-", " ").title(), ""))
        rel = ((rel_dir + "/" + e) if rel_dir else e) + "/"
        out.append({"name": e, "type": "dir", "path": rel, "title": t, "description": d})
    return out


def synthesize_index(rel_dir):
    """OKF §6-style directory listing, generated on demand (no index.md files
    are committed)."""
    rel_dir = norm(rel_dir)
    if rel_dir == "":
        lines = ["# Scriptling OKF Bundles", ""]
        for b in bundles():
            desc = " - " + b["description"] if b.get("description") else ""
            lines.append("- [" + b["title"] + "](" + b["name"] + "/)" + desc)
        return "\n".join(lines) + "\n"
    title = os.path.basename(rel_dir).replace("-", " ").title()
    ov = overview_for(rel_dir)
    if os.path.isfile(ov):
        t, _ = title_desc(ov)
        title = t
    lines = ["# " + title, ""]
    for ent in entries_for(rel_dir):
        label = ent["title"] or ent["name"]
        desc = " - " + ent["description"] if ent["description"] else ""
        lines.append("- [" + label + "](" + ent["path"] + ")" + desc)
    return "\n".join(lines) + "\n"
