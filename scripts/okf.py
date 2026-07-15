# OKF bundle generator — walks content/ and emits raw OKF markdown to static/okf/
# Run:  scriptling scripts/okf.py   (or:  make okf)
import os
import os.path
import shutil
import json
import yaml
import re

OUT = "mcp/okf"

# (name, source_dir, default_type, excluded_subdirs)
BUNDLES = [
    ("docs", "content/docs", "Guide", []),
    ("reference", "content/reference", "Reference", ["libraries"]),
    ("libraries", "content/reference/libraries", "API Reference", []),
]
BUNDLE_DESC = {
    "docs": "Guides, tutorials, and integration documentation.",
    "reference": "Language syntax, types, and built-in behaviour.",
    "libraries": "Standard and extended library API reference.",
}


# --- source -> bundle mapping ------------------------------------------------

def bundle_of(path):
    p = path.rstrip("/")
    if p == "content/reference/libraries" or p.startswith("content/reference/libraries/"):
        return "libraries"
    if p == "content/reference" or p.startswith("content/reference/"):
        return "reference"
    if p == "content/docs" or p.startswith("content/docs/"):
        return "docs"
    return None


def src_rel(path):
    b = bundle_of(path)
    if b is None:
        return None
    for name, src, _, _ in BUNDLES:
        if name != b:
            continue
        if path == src:
            return ""
        if path.startswith(src + "/"):
            return path[len(src) + 1:]
    return None


def out_rel_md(path):  # default mirrored output path for a source .md
    return OUT + "/" + bundle_of(path) + "/" + src_rel(path)


def out_base(path):  # output dir for a source file or directory
    return (OUT + "/" + bundle_of(path) + "/" + src_rel(path)).rstrip("/")


def out_dir_for(name, rel):  # output dir for a bundle + rel-from-source
    return OUT + "/" + name + ("/" + rel if rel else "")


def overview_out_path(cand):
    # Output path of the overview concept for a source directory. Bundle roots
    # keep theirs inside (<bundle>/<bundle>.md); subfolders sit beside theirs.
    b = bundle_of(cand)
    rel = src_rel(cand)
    if rel == "":
        return OUT + "/" + b + "/" + b + ".md"
    return out_dir_for(b, os.path.dirname(rel)) + "/" + os.path.basename(rel) + ".md"


# --- frontmatter -------------------------------------------------------------

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def parse(raw):
    m = FM_RE.match(raw)
    if not m:
        return {}, raw
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def build_frontmatter(fm, default_type, title):
    out = {"type": fm.get("type") or default_type, "title": title}
    for k in ["description", "tags", "timestamp", "resource"]:
        if k in fm and fm[k] not in ("", None):
            out[k] = fm[k]
    return "---\n" + yaml.safe_dump(out).rstrip() + "\n---\n"


def prepend_title(title, body):
    # Hugo renders the frontmatter title in its template, but raw OKF readers
    # only see frontmatter — surface it as an H1 (unless the body already opens
    # with one).
    if re.match(r"\s*# ", body):
        return body
    return "# " + title + "\n\n" + body.lstrip("\n")


def title_desc_of(file_path):
    fm, _ = parse(os.read_file(file_path))
    title = fm.get("title") or os.path.splitext(os.path.basename(file_path))[0]
    return title, (fm.get("description") or "")


# --- shortcode conversion ----------------------------------------------------

def convert_shortcodes(body):
    body = re.sub(r"\{\{<?\s*/?cards\s*>?\}\}\n?", "", body)

    def card_repl(m):
        attrs = m.group(1)
        link = re.search(r'link="([^"]*)"', attrs)
        title = re.search(r'title="([^"]*)"', attrs)
        desc = re.search(r'description="([^"]*)"', attrs)
        t = title.group(1) if title else ""
        d = " - " + desc.group(1) if desc else ""
        if link:
            return "- [" + t + "](" + link.group(1) + ")" + d + "\n"
        return "- **" + t + "**" + d + "\n"
    body = re.sub(r"\{\{<\s*card\b([^>]*)>\}\}", card_repl, body)

    def version_repl(m):
        return "### " + m.group(1) + "\n"
    body = re.sub(r'\{\{<\s*version\s+"?([^">]+?)"?\s*>\}\}', version_repl, body)

    def citem_repl(m):
        return "**" + m.group(1) + "**\n\n" + m.group(2).strip() + "\n"
    body = re.sub(r"\{\{<\s*changelog-item\s+\"?([a-zA-Z]+)\"?\s*>\}\}(.*?)\{\{<\s*/changelog-item\s*>\}\}",
                  citem_repl, body, flags=re.S)
    # strip any remaining shortcode tags
    body = re.sub(r"\{\{<\s*/[^>]*>\}\}", "", body)
    body = re.sub(r"\{\{<[^>]*>\}\}", "", body)
    return body


# --- link fixing -------------------------------------------------------------

LINK_PATTERN = r'(!?)\[([^\]]*)\]\(([^)]+)\)'


def resolve_target(src_file, out_file, url):
    """OKF link for an internal url, or None to leave unchanged.
    Target resolution uses the source location; relative links are computed
    from out_file (which may differ from the source mirror, e.g. a folder
    concept promoted to its parent level)."""
    anchor = ""
    if "#" in url:
        i = url.index("#")
        anchor = url[i:]
        url = url[:i]
    if url == "" or url.startswith("mailto:") or url.startswith("http://") or url.startswith("https://"):
        return None
    out_dir = os.path.dirname(out_file)
    if url.startswith("/"):
        cands = [os.path.normpath("content" + url.rstrip("/"))]
    else:
        d = os.path.dirname(src_file)
        if os.path.basename(src_file) == "_index.md":
            bases = [d]
        else:
            stem = os.path.splitext(os.path.basename(src_file))[0]
            bases = [d + "/" + stem, d]  # page-relative, then dir-relative fallback
        cands = [os.path.normpath(b + "/" + url).rstrip("/") for b in bases]
    for cand in cands:
        # OKF §5.2: relative links are portable and let consumers (e.g. an MCP
        # server) resolve a link from the file that contains it. Use relative
        # links for every internal target, cross- or same-bundle, so the bundle
        # never depends on a hosting path like /okf/.
        if os.path.isfile(cand + ".md"):
            tgt = cand + ".md"
            if bundle_of(tgt) is not None:
                return os.path.relpath(out_rel_md(tgt), out_dir) + anchor
        if os.path.isdir(cand):
            if bundle_of(cand) is None:
                continue
            # A directory link maps to its overview concept when it has one
            # (mirrors the website, where a dir URL serves the _index overview),
            # otherwise to the directory itself.
            if os.path.isfile(cand + "/_index.md"):
                return os.path.relpath(overview_out_path(cand), out_dir) + anchor
            return os.path.relpath(out_base(cand), out_dir) + "/" + anchor
    return None


def fix_links(body, src_file, out_file):
    def repl(m):
        r = resolve_target(src_file, out_file, m.group(3))
        if r is None:
            return m.group(0)
        return m.group(1) + "[" + m.group(2) + "](" + r + ")"
    return re.sub(LINK_PATTERN, repl, body)


# --- processing --------------------------------------------------------------

def process_file(src_file, default_type, out_file):
    raw = os.read_file(src_file)
    fm, body = parse(raw)
    body = convert_shortcodes(body)
    body = fix_links(body, src_file, out_file)
    title = fm.get("title") or os.path.splitext(os.path.basename(src_file))[0]
    body = prepend_title(title, body)
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    os.write_file(out_file, build_frontmatter(fm, default_type, title) + body.rstrip() + "\n")


def list_dir(src_dir, exclude):
    try:
        return sorted(os.listdir(src_dir))
    except Exception:
        return []


# PASS 1 — emit concept files ------------------------------------------------

def emit_bundle(name, src, default_type, exclude):
    def emit(rel):
        absd = src + ("/" + rel if rel else "")
        for entry in list_dir(absd, exclude):
            full = absd + "/" + entry
            if os.path.isdir(full):
                if entry in exclude:
                    continue
                emit(entry if rel == "" else rel + "/" + entry)
            elif entry.endswith(".md"):
                if entry == "_index.md":
                    if rel == "":
                        # bundle overview -> inside its bundle, named after it
                        out_file = OUT + "/" + name + "/" + name + ".md"
                    else:
                        # folder concept -> promoted beside its folder, named after it
                        parent_rel = os.path.dirname(rel)
                        out_file = out_dir_for(name, parent_rel) + "/" + os.path.basename(rel) + ".md"
                elif entry == "index.md":
                    out_file = out_dir_for(name, rel) + "/index.md"  # leaf concept
                else:
                    out_file = out_dir_for(name, rel) + "/" + entry  # mirrored concept
                process_file(full, default_type, out_file)
    emit("")


# PASS 2 — manifest ----------------------------------------------------------
# No index.md files are generated: directory listings are synthesized on the
# fly by the MCP server (OKF §6 permits this). A manifest lets list_bundles()
# return bundle metadata without touching source frontmatter.

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for name, src, default_type, exclude in BUNDLES:
        emit_bundle(name, src, default_type, exclude)
        idx = src + "/_index.md"
        if os.path.isfile(idx):
            t, d = title_desc_of(idx)
        else:
            t, d = name.title(), ""
        if not d:
            d = BUNDLE_DESC.get(name, "")
        if not t:
            t = name.title()
        manifest.append({"name": name, "title": t, "description": d})
    # manifest.json is tooling metadata (not OKF content) -> lives outside okf/
    os.write_file(os.path.dirname(OUT) + "/manifest.json", json.dumps(manifest, indent=2) + "\n")
    print("OKF bundles generated at " + OUT + "/")


main()
