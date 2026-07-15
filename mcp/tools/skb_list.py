import os
import os.path
import scriptling.mcp.tool as tool
import okf_lib as lib

path = lib.norm(tool.get_string("path", ""))
if path == "":
    tool.return_object(lib.bundle_entries())
else:
    full = lib.resolve(path)
    if full is None:
        tool.return_error("Not found: " + path)
    elif os.path.isdir(full):
        tool.return_object(lib.entries_for(path))
    elif os.path.isfile(full):
        # Lenient: a file path yields its metadata as a single entry, signalling
        # "this is a file" so the caller can skb_get it rather than getting an error.
        t, d = lib.title_desc(full)
        tool.return_object([{"name": os.path.basename(full), "type": "file",
                             "path": path, "title": t, "description": d}])
    else:
        tool.return_error("Not found: " + path)
