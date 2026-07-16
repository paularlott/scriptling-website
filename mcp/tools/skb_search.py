import os
import os.path
import json
import scriptling.mcp.tool as tool
import scriptling.similarity as sim
import logging as log
import okf_lib as lib

# Per-field cosine weights. td (title+description+path) is favoured because the
# short, curated field resists the hash collisions that long bodies suffer.
W_TD = 0.6
W_BODY = 0.4


def _walk_md(d):
    out = []
    for e in sorted(os.listdir(d)):
        full = d + "/" + e
        if os.path.isdir(full):
            out.extend(_walk_md(full))
        elif e.endswith(".md"):
            out.append(full)
    return out


def ensure_vectors(bname):
    """Build a bundle's .vector.json sidecar on first use if missing. Mirrors
    the offline OKF generator: per-concept td (title+description+path) and body
    vectors at lib.VECTORS_DIMS, powering semantic ranking."""
    bdir = lib.OKF_ROOT + "/" + bname
    vf = bdir + "/" + lib.VECTOR_FILE
    if os.path.isfile(vf):
        return vf
    log.info("Building vector index for " + bname)
    entries = []
    for f in _walk_md(bdir):
        fm, body = lib.frontmatter(f)
        title = fm.get("title") or os.path.splitext(os.path.basename(f))[0]
        desc = fm.get("description") or ""
        rel = f[len(bdir) + 1:]
        td_text = title + " " + desc + " " + rel.replace("/", " ")
        entries.append({"path": rel, "title": title,
                        "td": sim.vectorize(td_text, dims=lib.VECTORS_DIMS),
                        "body": sim.vectorize(body, dims=lib.VECTORS_DIMS)})
    os.write_file(vf, json.dumps({"dims": lib.VECTORS_DIMS, "entries": entries}))
    log.info("Indexed " + str(len(entries)) + " concepts for " + bname)
    return vf


query = tool.get_string("query", "")
path = lib.norm(tool.get_string("path", ""))
top_k = tool.get_int("top_k", 10)

if not query:
    tool.return_error("No query provided")

td_vecs = []
body_vecs = []
meta = []
dims = lib.VECTORS_DIMS
for b in lib.bundles():
    bname = b["name"]
    vf = ensure_vectors(bname)  # build on first use if missing
    data = json.loads(os.read_file(vf))
    dims = data.get("dims", dims)
    for e in data["entries"]:
        full = bname + "/" + e["path"]
        if path and not (full == path or full.startswith(path + "/")):
            continue
        td_vecs.append(e["td"])
        body_vecs.append(e["body"])
        meta.append({"path": full, "title": e["title"]})

if not td_vecs:
    tool.return_error("No concepts found for scope")

q = sim.vectorize(query, dims=dims)
scored = []
for i in range(len(td_vecs)):
    combined = W_TD * sim.cosine_similarity(q, td_vecs[i]) + W_BODY * sim.cosine_similarity(q, body_vecs[i])
    if combined > 0:
        scored.append((combined, i))
scored.sort(reverse=True)

out = []
for combined, i in scored[:top_k]:
    out.append({"path": meta[i]["path"], "title": meta[i]["title"], "score": round(combined, 4)})
tool.return_object({"query": query, "scope": path or "(all bundles)", "results": out})
