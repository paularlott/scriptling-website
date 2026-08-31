# OKF bundle generator — walks content/ and emits OKF 0.2 markdown in two trees.
# Run:  scriptling scripts/okf.py   (or:  make okf)
#
#   okf/       hosted copy, mounted into the site at /okf/ (hugo.toml
#              module.mounts) and committed — Cloudflare runs Hugo but not
#              scripts. Every internal link is an absolute
#              https://scriptling.dev/okf/ URL: agents fetch these files over
#              HTTP and their fetch guards track absolute URLs from earlier
#              fetches, not relative ones.
#   dist/okf/  release-zip copy, packed by `make bundle-pack` and uploaded to
#              GitHub releases. Not committed (dist/ is gitignored). Links
#              stay relative per OKF §5.2, so the bundle never depends on a
#              hosting path.
#
# okf/index.md, okf/index.html and okf/llms.txt are site-only catalogs outside
# the bundles; the zip packs the three bundle directories only.
import os
import os.path
import shutil
import yaml
import re

OUT = "okf"            # hosted tree: absolute links, committed, served at /okf/
ZIP_OUT = "dist/okf"   # zip tree: relative links, packed into the release bundle
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
    if rel == ".":
        rel = ""
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


# --- presentation and shortcode conversion ----------------------------------

def clean_presentation_text(value):
    # Presentation cards may contain icons and styled wrapper elements. Keep
    # their readable text without teaching OKF consumers about the site layout.
    value = re.sub(r"(?si)<svg\b.*?</svg>", "", value)
    value = re.sub(r"<[^>]+>", "", value)
    for old, new in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#39;", "'"), ("&rarr;", "→")]:
        value = value.replace(old, new)
    return re.sub(r"\s+", " ", value).strip()


def convert_presentation_html(body):
    # Convert visual card grids marked `not-prose` into semantic Markdown.
    # Scriptling's RE2 wrapper uses inline flags for multiline matching.
    pattern = r'(?si)<div[^>]*class="[^"]*not-prose[^"]*"[^>]*>\s*(.*)\n</div>'

    def grid_repl(m):
        cards = re.findall(r'(?si)<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>', m.group(1))
        if not cards:
            return m.group(0)
        lines = []
        for href, card in cards:
            title_match = re.search(r"(?si)<h[1-6]\b[^>]*>(.*?)</h[1-6]>", card)
            if title_match is None:
                return m.group(0)
            title = clean_presentation_text(title_match.group(1))
            description_match = re.search(r"(?si)<p\b[^>]*>(.*?)</p>", card)
            description = clean_presentation_text(description_match.group(1)) if description_match else ""
            lines.append("- [" + title + "](" + href + ")" + (" — " + description if description else ""))
            for item in re.findall(r"(?si)<li\b[^>]*>(.*?)</li>", card):
                text = clean_presentation_text(item)
                if text:
                    lines.append("  - " + text)
        return "\n".join(lines)

    return re.sub(pattern, grid_repl, body)


def convert_shortcodes(body):
    body = convert_presentation_html(body)
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


def link_target(out_path, out_dir, anchor, absolute, dir_link):
    # OKF §5.2: the zip copy links relatively so a consumer resolves every
    # link from the file that contains it and the bundle never depends on a
    # hosting path. The hosted copy links absolutely (see header) so HTTP
    # fetchers never need relative-path resolution.
    if absolute:
        if dir_link:
            return BASE_URL + "/" + out_path + "/" + anchor
        return BASE_URL + "/" + out_path + anchor
    if dir_link:
        return os.path.relpath(out_path, out_dir) + "/" + anchor
    return os.path.relpath(out_path, out_dir) + anchor


def resolve_target(src_file, out_file, url, absolute):
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
        if os.path.isfile(cand + ".md"):
            tgt = cand + ".md"
            if bundle_of(tgt) is not None:
                return link_target(out_rel_md(tgt), out_dir, anchor, absolute, False)
        if os.path.isdir(cand):
            if bundle_of(cand) is None:
                continue
            # A directory link maps to its overview concept when it has one
            # (mirrors the website, where a dir URL serves the _index overview),
            # otherwise to the directory itself.
            if os.path.isfile(cand + "/_index.md") or os.path.isfile(cand + "/index.md"):
                return link_target(overview_out_path(cand), out_dir, anchor, absolute, False)
            return link_target(out_base(cand), out_dir, anchor, absolute, True)
    return None


def fix_links(body, src_file, out_file, absolute):
    def repl(m):
        r = resolve_target(src_file, out_file, m.group(3), absolute)
        if r is None:
            return m.group(0)
        return m.group(1) + "[" + m.group(2) + "](" + r + ")"
    return re.sub(LINK_PATTERN, repl, body)


# --- processing --------------------------------------------------------------

def process_file(src_file, default_type, out_file, out_root, absolute):
    raw = os.read_file(src_file)
    fm, body = parse(raw)
    body = convert_shortcodes(body)
    body = fix_links(body, src_file, out_file, absolute)
    title = fm.get("title") or os.path.splitext(os.path.basename(src_file))[0]
    body = prepend_title(title, body)
    dest = out_root + out_file[len(OUT):]
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    os.write_file(dest, build_frontmatter(fm, default_type, title, page_url(src_file)) + body.rstrip() + "\n")


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
    # only for the okf_version key. Body is level-by-level navigation. The
    # zip copy keeps relative targets (OKF §5.2); the hosted copy uses
    # absolute URLs so agents can follow the nav with plain fetches.
    pairs = []
    seen = set()  # concepts already listed via their directory
    overview = OUT + "/" + name + "/" + name + ".md"
    if os.path.isfile(overview):
        pairs.append([concept_title(overview), name + ".md"])
        seen.add(name + ".md")
    for entry in list_dir(OUT + "/" + name, []):
        if entry in (".", "..", "index.md"):
            continue
        full = OUT + "/" + name + "/" + entry
        if entry.endswith(".md"):
            if entry in seen:
                continue
            pairs.append([concept_title(full), entry])
        elif os.path.isdir(full):
            concept = full + ".md"
            if os.path.isfile(concept):
                pairs.append([concept_title(concept), entry + ".md"])
                seen.add(entry + ".md")
            else:
                pairs.append([entry, ""])
    zip_entries = []
    site_entries = []
    for p in pairs:
        title = p[0]
        target = p[1]
        if target == "":
            zip_entries.append("- " + title)
            site_entries.append("- " + title)
        else:
            zip_entries.append("- [" + title + "](" + target + ")")
            site_entries.append("- [" + title + "](" + BASE_URL + "/" + OUT + "/" + name + "/" + target + ")")
    body = "# " + name + "\n\n" + BUNDLE_DESCRIPTIONS[name] + "\n\n## Concepts\n\n"
    os.makedirs(ZIP_OUT + "/" + name, exist_ok=True)
    os.write_file(ZIP_OUT + "/" + name + "/index.md",
                  "---\nokf_version: \"" + OKF_VERSION + "\"\n---\n" + body + "\n".join(zip_entries) + "\n")
    os.write_file(OUT + "/" + name + "/index.md",
                  "---\nokf_version: \"" + OKF_VERSION + "\"\n---\n" + body + "\n".join(site_entries) + "\n")


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
                process_file(full, default_type, out_file, OUT, True)
                process_file(full, default_type, out_file, ZIP_OUT, False)
    emit("")
    emit_bundle_index(name, src)


def walk_concepts(root, out):
    # Depth-first, alphabetical: every concept beside the tree it documents.
    for entry in list_dir(root, []):
        if entry in (".", "..", "index.md"):
            continue
        full = root + "/" + entry
        if entry.endswith(".md"):
            out.append(full)
        elif os.path.isdir(full):
            walk_concepts(full, out)


def concept_description(out_file):
    # Description of an already-emitted concept, read back from its frontmatter.
    try:
        fm, _ = parse(os.read_file(out_file))
        d = fm.get("description")
        if d not in ("", None):
            return d
    except Exception:
        pass
    return ""


def emit_llms_txt():
    # Site-only llms.txt at /okf/llms.txt: every concept in every bundle as an
    # absolute link, so an agent lists the whole corpus in one fetch. Never
    # packed into the release zip.
    sections = []
    total = 0
    for name, _, _, _ in BUNDLES:
        files = []
        walk_concepts(OUT + "/" + name, files)
        lines = ["## " + name, "", "> " + BUNDLE_DESCRIPTIONS[name], ""]
        for f in files:
            total = total + 1
            url = BASE_URL + "/" + f
            d = concept_description(f)
            if d == "":
                lines.append("- [" + concept_title(f) + "](" + url + ")")
            else:
                lines.append("- [" + concept_title(f) + "](" + url + "): " + d)
        sections.append("\n".join(lines))
    header = ["# Scriptling OKF bundles", "",
              "> All " + str(total) + " OKF " + OKF_VERSION + " concepts, plain markdown served from "
              + BASE_URL + "/okf/. Links here and inside every document are absolute URLs: fetch any of them directly.", ""]
    os.write_file(OUT + "/llms.txt", "\n".join(header + sections) + "\n")


def emit_site_catalog():
    # Site-only catalog at okf/index.md. It sits beside the bundles, not
    # inside any of them, so it is outside OKF's index rules entirely; it is
    # never packed into the release zip.
    entries = []
    for name, _, _, _ in BUNDLES:
        entries.append("- [" + name + "](" + BASE_URL + "/" + OUT + "/" + name + "/index.md) — " + BUNDLE_DESCRIPTIONS[name])
    body = ("# Scriptling OKF Bundles\n\n"
            "OKF " + OKF_VERSION + " knowledge bundles generated from the [Scriptling documentation](" + BASE_URL + "/docs/). "
            "Fetch these URLs directly: every document is plain markdown with YAML frontmatter, and every link is an absolute "
            + BASE_URL + "/okf/ URL, so no relative-path resolution is ever needed. "
            "[llms.txt](" + BASE_URL + "/" + OUT + "/llms.txt) lists every page in one fetch. "
            "The release zip keeps portable relative links per OKF §5.2.\n\n## Bundles\n\n" + "\n".join(entries) + "\n")
    os.write_file(OUT + "/index.md", body)

    # HTML twin: static hosts serve /okf/ from index.html, not index.md
    rows = []
    for name, _, _, _ in BUNDLES:
        rows.append('<li><a href="' + BASE_URL + "/" + OUT + "/" + name + '/index.md">' + name + "</a> — " + BUNDLE_DESCRIPTIONS[name] + "</li>")
    html = ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>Scriptling OKF Bundles</title>\n"
            "<style>body{font-family:system-ui,sans-serif;max-width:44rem;margin:3rem auto;padding:0 1rem;line-height:1.6}code{background:#f1f5f9;padding:.1rem .3rem;border-radius:.25rem}@media(prefers-color-scheme:dark){body{background:#0f172a;color:#e2e8f0}code{background:#1e293b}}</style>\n"
            "</head>\n<body>\n<h1>Scriptling OKF Bundles</h1>\n"
            "<p>OKF " + OKF_VERSION + " knowledge bundles generated from the <a href=\"" + BASE_URL + "/docs/\">Scriptling documentation</a>. "
            "Every document is plain markdown with YAML frontmatter and absolute links — fetch these URLs directly, "
            "start from <a href=\"" + BASE_URL + "/" + OUT + "/index.md\">index.md</a>, or fetch "
            "<a href=\"" + BASE_URL + "/" + OUT + "/llms.txt\">llms.txt</a> for every page in one list.</p>\n"
            "<ul>\n" + "\n".join(rows) + "\n</ul>\n</body>\n</html>\n")
    os.write_file(OUT + "/index.html", html)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    if os.path.isdir(ZIP_OUT):
        shutil.rmtree(ZIP_OUT)
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(ZIP_OUT, exist_ok=True)
    for name, src, default_type, exclude in BUNDLES:
        emit_bundle(name, src, default_type, exclude)
    emit_site_catalog()
    emit_llms_txt()
    print("OKF " + OKF_VERSION + " bundles generated at " + OUT + "/ (hosted, absolute links) and " + ZIP_OUT + "/ (zip, relative links)")


main()
