#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# ^\s*(?=\r?$)\n
with open("./SaveLoadManagerServer_JSON_RPC_HTTP.html", mode="r", encoding="utf-8", errors='ignore') as html_file:
    source_code = html_file.read()
with open("./SaveLoadManagerServer_JSON_RPC_HTTP_String.py", mode="w", encoding="utf-8", errors='ignore') as py_file:
    lines = ['#!/usr/bin/python3', '# -*- coding: UTF-8 -*-', '# ^\\s*(?=\\r?$)\\n', "html_string = ('''", source_code, "''')"]
    py_file.writelines('\n'.join(lines))
