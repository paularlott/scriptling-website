# OKF bundle generator — walks content/ and emits OKF 0.2 markdown to okf/.
# Run:  scriptling scripts/okf.py   (or:  make okf)
#
# Output is committed: the site is hosted on Cloudflare, which runs Hugo but
# not scripts, so okf/ is mounted into the site (see hugo.toml module.mounts)
# and published at /okf/. The zip for GitHub releases packs the three bundle
# directories only — okf/index.md is a site-only catalog outside the bundles.
import os
import os.path
import shutil
import yaml
import re

OUT = "okf"
OKF_VERSION = "0.2"
GENERATED_BY = "scriptling-website/okf.py"
BASE_URL = "https://scriptling.dev"

# (name, source_dir, default_type, excluded_subdirs)
BUNDLES = [
    ("scriptling-docs", "content/docs", "Guide", []),
    ("scriptling-reference", "content/reference", "Reference", ["libraries"]),
    ("scriptling-libraries", "content/reference/libraries", "API Reference", []),
]

BUNDLE_DESCRIPTIONS = {
    "scriptling-docs": "Guides: quick start, CLI usage, Go integration, plugins, security, and tutorials.",
    "scriptling-reference": "Language reference: syntax, types, operators, control flow, functions, classes, and error handling.",
    "scriptling-libraries": "API reference for every standard, Scriptling, and extended library.",
}


# --- source -> bundle mapping ------------------------------------------------

def bundle_of(path):
    p = path.rstrip("/")
    if p == "content/reference/libraries" or p.startswith("content/reference/libraries/"):
        return "scriptling-libraries"
    if p == "content/reference" or p.startswith("content/reference/"):
        return "scriptling-reference"
    if p == "content/docs" or p.startswith("content/docs/"):
        return "scriptling-docs"
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
    r = src_rel(path)
    if r.endswith("/index.md"):
        # leaf page bundle (a dir named after the page) emits its concept
        # beside the directory, so index.md never carries concept frontmatter
        d = os.path.dirname(r)
        return out_dir_for(bundle_of(path), os.path.dirname(d)) + "/" + os.path.basename(d) + ".md"
    return OUT + "/" + bundle_of(path) + "/" + r


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


def page_url(src_file):
    # Canonical hosted URL of the source page, used for provenance.
    rel = src_file[len("content/"):]
    if rel.endswith("/_index.md"):
        rel = rel[: -len("_index.md")]
    elif rel.endswith("/index.md"):
        rel = rel[: -len("index.md")]
    else:
        rel = rel[:-3] + "/"
    return BASE_URL + "/" + rel


# --- frontmatter -------------------------------------------------------------

FM_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def parse(raw):
    m = FM_RE.match(raw)
    if not m:
        return {}, raw
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def build_frontmatter(fm, default_type, title, url):
    out = {"type": fm.get("type") or default_type, "title": title}
    for k in ["description", "tags", "resource"]:
        if k in fm and fm[k] not in ("", None):
            out[k] = fm[k]
    # OKF 0.2 provenance and lifecycle fields. `generated.at` uses the page's
    # own lastmod/date when set so output stays deterministic across
    # regenerations; absent is conformant (only generated.by is required).
    generated = {"by": GENERATED_BY}
    for k in ["lastmod", "date"]:
        if fm.get(k):
            generated["at"] = fm[k]
            break
    out["generated"] = generated
    out["status"] = fm.get("okf_status") or "stable"
    out["sources"] = [{"resource": url}]
    if "resource" not in out:
        out["resource"] = url
    return "---\n" + yaml.safe_dump(out).rstrip() + "\n---\n"


def prepend_title(title, body):
    # Hugo renders the frontmatter title in its template, but raw OKF readers
    # only see frontmatter — surface it as an H1 (unless the body already opens
    # with one).
    if re.match(r"\s*# ", body):
        return body
    return "# " + title + "\n\n" + body.lstrip("\n")


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
            if os.path.isfile(cand + "/_index.md") or os.path.isfile(cand + "/index.md"):
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
    os.write_file(out_file, build_frontmatter(fm, default_type, title, page_url(src_file)) + body.rstrip() + "\n")


def list_dir(src_dir, exclude):
    try:
        return sorted(os.listdir(src_dir))
    except Exception:
        return []


def concept_title(out_file):
    # Title of an already-emitted concept, read back from its frontmatter.
    try:
        fm, _ = parse(os.read_file(out_file))
        return fm.get("title") or os.path.splitext(os.path.basename(out_file))[0]
    except Exception:
        return os.path.splitext(os.path.basename(out_file))[0]


def emit_bundle_index(name, src):
    # OKF 0.2 bundle-root index.md: the only index allowed frontmatter, and
    # only for the okf_version key. Body is level-by-level navigation.
    entries = []
    seen = set()  # concepts already listed via their directory
    overview = OUT + "/" + name + "/" + name + ".md"
    if os.path.isfile(overview):
        entries.append("- [" + concept_title(overview) + "](" + name + ".md)")
        seen.add(name + ".md")
    for entry in list_dir(OUT + "/" + name, []):
        if entry in (".", "..", "index.md"):
            continue
        full = OUT + "/" + name + "/" + entry
        if entry.endswith(".md"):
            if entry in seen:
                continue
            entries.append("- [" + concept_title(full) + "](" + entry + ")")
        elif os.path.isdir(full):
            concept = full + ".md"
            if os.path.isfile(concept):
                entries.append("- [" + concept_title(concept) + "](" + entry + ".md)")
                seen.add(entry + ".md")
            else:
                entries.append("- " + entry)
    body = "# " + name + "\n\n" + BUNDLE_DESCRIPTIONS[name] + "\n\n## Concepts\n\n" + "\n".join(entries) + "\n"
    os.write_file(OUT + "/" + name + "/index.md",
                  "---\nokf_version: \"" + OKF_VERSION + "\"\n---\n" + body)


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
                    # leaf page bundle -> concept beside its directory, named
                    # after it: OKF reserves index.md for navigation (no
                    # concept frontmatter outside a bundle root)
                    parent_rel = os.path.dirname(rel)
                    out_file = out_dir_for(name, parent_rel) + "/" + os.path.basename(rel) + ".md"
                else:
                    out_file = out_dir_for(name, rel) + "/" + entry  # mirrored concept
                process_file(full, default_type, out_file)
    emit("")
    emit_bundle_index(name, src)


def emit_site_catalog():
    # Site-only catalog at okf/index.md. It sits beside the bundles, not
    # inside any of them, so it is outside OKF's index rules entirely; it is
    # never packed into the release zip.
    entries = []
    for name, _, _, _ in BUNDLES:
        entries.append("- [" + name + "](" + name + "/index.md) — " + BUNDLE_DESCRIPTIONS[name])
    body = ("# Scriptling OKF Bundles\n\n"
            "OKF " + OKF_VERSION + " knowledge bundles generated from the [Scriptling documentation]("
            + BASE_URL + "/docs/). Fetch these URLs directly; every document is plain markdown with "
            "YAML frontmatter and relative links.\n\n## Bundles\n\n" + "\n".join(entries) + "\n")
    os.write_file(OUT + "/index.md", body)

    # HTML twin: static hosts serve /okf/ from index.html, not index.md
    rows = []
    for name, _, _, _ in BUNDLES:
        rows.append('<li><a href="' + name + '/index.md">' + name + "</a> — " + BUNDLE_DESCRIPTIONS[name] + "</li>")
    html = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Scriptling OKF Bundles</title>\n"
            "<style>body{font-family:system-ui,sans-serif;max-width:44rem;margin:3rem auto;padding:0 1rem;line-height:1.6}code{background:#f1f5f9;padding:.1rem .3rem;border-radius:.25rem}@media(prefers-color-scheme:dark){body{background:#0f172a;color:#e2e8f0}code{background:#1e293b}}</style>\n"
            "</head>\n<body>\n<h1>Scriptling OKF Bundles</h1>\n"
            "<p>OKF " + OKF_VERSION + " knowledge bundles generated from the <a href=\"" + BASE_URL + "/docs/\">Scriptling documentation</a>. "
            "Every document is plain markdown with YAML frontmatter and relative links — fetch these URLs directly, or start from <a href=\"index.md\">index.md</a>.</p>\n"
            "<ul>\n" + "\n".join(rows) + "\n</ul>\n</body>\n</html>\n")
    os.write_file(OUT + "/index.html", html)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)
    for name, src, default_type, exclude in BUNDLES:
        emit_bundle(name, src, default_type, exclude)
    emit_site_catalog()
    print("OKF " + OKF_VERSION + " bundles generated at " + OUT + "/")


main()
