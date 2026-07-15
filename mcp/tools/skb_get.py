import os
import os.path
import scriptling.mcp.tool as tool
import okf_lib as lib

path = lib.norm(tool.get_string("path", ""))
# a request for a directory listing: empty, trailing slash, or "<dir>/index.md"
if path.endswith("/index.md"):
    path = path[: -len("/index.md")]
if path.endswith("/"):
    path = path[:-1]

full = lib.resolve(path)
if full is None:
    tool.return_error("Invalid path: " + path)
elif path == "":
    tool.return_string(lib.synthesize_index(""))  # root: the bundle list
elif os.path.isdir(full):
    tool.return_string(lib.synthesize_index(path))  # synthesize §6 listing
elif os.path.isfile(full):
    tool.return_string(os.read_file(full))  # raw concept markdown
else:
    tool.return_error("Not found: " + path)
