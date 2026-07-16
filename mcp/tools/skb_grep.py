import os
import re
import scriptling.mcp.tool as tool
import scriptling.grep as grep
import okf_lib as lib

path = lib.norm(tool.get_string("path", ""))
terms = [t for t in tool.get_list("terms", []) if t]

scope = lib.resolve(path)
if scope is None:
    tool.return_error("Invalid path: " + path)
elif not terms:
    tool.return_error("No search terms provided")

# single parallel OR scan (scriptling.grep uses a concurrent worker pool).
# glob="*.md" excludes generated sidecars like .vector.json.
pattern = "|".join(re.escape(t) for t in terms)
matches = grep.pattern(pattern, scope, recursive=True, ignore_case=True, glob="*.md")

root = lib.root_abs()
out = []
for m in matches:
    f = m["file"]
    if f.startswith(root + os.sep):
        f = f[len(root) + 1:]
    out.append({"path": f, "line": m["line"], "text": m["text"].strip()})
    if len(out) >= 200:
        break

tool.return_object({"matches": out, "count": len(out), "truncated": len(out) >= 200})
