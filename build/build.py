#!/usr/bin/env python3
"""Ensambla Codigo/web/index.html a partir de site_template.html + assets."""
import json, base64, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = pathlib.Path("/Users/stce/Proyectos/Le-RING/Codigo/web/index.html")

tpl = (ROOT / "site_template.html").read_text()
tpl = tpl.replace("{{FONTS_CSS}}", (ROOT / "fonts/embedded.css").read_text())

for ph, path in [("IMG_LOGO", "assets/f_logo.jpg"), ("IMG_TUYAUX", "assets/f_tuyaux.jpg"),
                 ("IMG_POSE", "assets/f_pose.jpg"), ("IMG_EQ", "assets/f_equilibrium.jpg"),
                 ("IMG_DISSO", "assets/f_dissolvium.jpg"), ("IMG_DN150", "assets/f_dn150.jpg")]:
    b64 = base64.b64encode((ROOT / path).read_bytes()).decode()
    tpl = tpl.replace("{{" + ph + "}}", "data:image/jpeg;base64," + b64)

m = json.load(open(ROOT / "map/svgmap.json"))
main, inset, pts = m["main"], m["inset"], m["points"]
repl = {
    "MAP_W": str(main["w"]), "MAP_H": str(main["h"]),
    "MAP_FRANCE": main["france"], "MAP_SPAIN": main["spain"], "MAP_PORTUGAL": main["portugal"],
    "MAP_CANARIAS": inset["canarias"],
    "INSET_TX": "12", "INSET_TY": "150",
    "INSET_BOX_W": str(round(inset["w"] + 16, 1)), "INSET_BOX_H": str(round(inset["h"] + 34, 1)),
    "INSET_LABEL_Y": str(round(inset["h"] + 17, 1)),
}
for name, (x, y) in pts.items():
    repl["PT_" + name.upper()] = f"[{x},{y}]"
for k, v in repl.items():
    tpl = tpl.replace("{{" + k + "}}", v)

leftover = tpl.split("{{")[1:]
assert not leftover, "placeholders sin sustituir: " + str([l[:30] for l in leftover])

OUT.write_text(tpl)
print("OK →", OUT, OUT.stat().st_size // 1024, "KB")
