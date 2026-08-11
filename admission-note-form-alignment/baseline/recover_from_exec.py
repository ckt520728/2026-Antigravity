import io, json

base = r"C:/Users/YANGMI~1/AppData/Local/Temp/claude/C--Users-YangminRoom1/f0f62c61-6d6b-456f-807f-d79076dc94de/scratchpad"
s = io.open(base + "/proto_shell.html", encoding="utf-8").read()

BS = chr(92)
marker = BS + "x22userHtml" + BS + "x22:" + BS + "x22"
i = s.find(marker)
endpat = BS + "x22," + BS + "x22ncc"
j = s.find(endpat, i)
print("marker at", i, "end at", j)
seg = s[i + len(marker): j]
print("seg len", len(seg))


def js_unescape(t):
    """Undo one layer of JavaScript string-literal escaping."""
    out = []
    k = 0
    n = len(t)
    while k < n:
        c = t[k]
        if c == BS and k + 1 < n:
            nx = t[k + 1]
            if nx == "x":
                out.append(chr(int(t[k + 2:k + 4], 16)))
                k += 4
            elif nx == "u":
                out.append(chr(int(t[k + 2:k + 6], 16)))
                k += 6
            elif nx == BS:
                out.append(BS)   # keep single backslash so JSON layer still sees its escapes
                k += 2
            else:
                # JS drops the backslash for other escapes (notably \/ ),
                # leaving the JSON layer's own escapes intact.
                out.append(nx)
                k += 2
        else:
            out.append(c)
            k += 1
    return "".join(out)


json_body = js_unescape(seg)
print("after js_unescape len", len(json_body))

html = json.loads('"' + json_body + '"')
io.open(base + "/proto_app.html", "w", encoding="utf-8").write(html)
print("FINAL len", len(html))
print("lines", html.count("\n") + 1)
print("divs", html.count("<div"), "scripts", html.count("<script"))
print("head:", repr(html[:80]))
print("tail:", repr(html[-40:]))
