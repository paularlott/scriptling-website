import os
import os.path
import json
import scriptling.mcp.tool as tool
import scriptling.similarity as sim
import okf_lib as lib

# Per-field cosine weights. td (title+description+path) is favoured because the
# short, curated field resists the hash collisions that long bodies suffer.
W_TD = 0.6
W_BODY = 0.4

query = tool.get_string("query", "")
path = lib.norm(tool.get_string("path", ""))
top_k = tool.get_int("top_k", 10)

if not query:
    tool.return_error("No query provided")

td_vecs = []
body_vecs = []
meta = []
dims = 512
for b in lib.bundles():
    bname = b["name"]
    vf = lib.OKF_ROOT + "/" + bname + "/.vector.json"
    if not os.path.isfile(vf):
        continue
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
    tool.return_error("No vectors found for scope (run 'make okf' to build them)")

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
