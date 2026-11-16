"""Write models.json for the online model library (see app/models.js) from the .glb files in this folder.

Each model's matching words, pose and credit live in ENTRIES below; size and SHA-256 are measured here,
so the app can refuse a file that changed or broke on the way. Run after adding or replacing a model:
    python library/build_index.py
"""
import hashlib
import json
import pathlib

HERE = pathlib.Path(__file__).parent
CC_BY = ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/")

# id → names it stands for, pose [x, y, z] (radians), credit (Sketchfab page, author, profile).
# Names: a list of alternatives, each a list of words that must all appear in the headphones' name
# (case, spaces and dashes ignored). A model also stands in for lookalikes (FAMILY below).
# Only licences that allow selling the app.
ENTRIES = {
    "airpods-pro": ([["airpods", "pro"]], [0.35, -0.45, 0],
                    ("AirPods Pro", "https://sketchfab.com/3d-models/airpods-pro-2a97b522bd1e43ffa342e4a19ff21e35",
                     "eltayerkebulan", "https://sketchfab.com/eltayerkebulan")),
    "airpods-max": ([["airpods", "max"]], [0.1, 0.6, 0],
                    ("Airpods max", "https://sketchfab.com/3d-models/airpods-max-05181e126a6341668ca95f2d98324d30",
                     "Mr.Philin", "https://sketchfab.com/yarik.chilin")),
    # "wh1000…": the WF-1000XM4/XM5 earbuds share the number but look nothing alike
    "sony-xm4": ([["wh1000xm4"]], [0.1, 0.6, 0],
                 ("SONY headphone WH-1000XM4", "https://sketchfab.com/3d-models/sony-headphone-wh-1000xm4-f90f76c75d8143eb97eb49844050aa26",
                  "Chizuko V", "https://sketchfab.com/chizuk0")),
    "sony-xm5": ([["wh1000xm5"]], [0.1, 0.6, 0],  # the same file the app ships as its XM6 stand-in
                 ("Sony Wh-1000xm5", "https://sketchfab.com/3d-models/sony-wh-1000xm5-5d8aea0a780b49fa89c9c205912414e3",
                  "Zalanekee", "https://sketchfab.com/Zalanekee")),
    "galaxy-buds": ([["buds", "live"]], [0.35, -0.45, 0],
                    ("Samsung Galaxy Buds Live", "https://sketchfab.com/3d-models/samsung-galaxy-buds-live-7e4a0f2202144b91b4c47ffbfdf94584",
                     "DatSketch", "https://sketchfab.com/DatSketch")),
    "jbl-t450": ([["jbl", "t450"]], [0.1, 0.6, 0],
                 ("JBL T450", "https://sketchfab.com/3d-models/jbl-t450-6db4c5b60e124d40a8be06ec1fe22c67",
                  "Oleksii Rozumnyi", "https://sketchfab.com/Oleksii.Rozumnyi")),
}

# lookalikes: headphones with no model of their own that look close enough to borrow one
FAMILY = {
    # AirPods Pro 2 and 3 keep the Pro's shape (the name "AirPods Pro 2" already matches "airpods pro")
    "sony-xm4": [["wh1000xm3"], ["wh1000xm2"]],          # same fold-flat body as the XM4
    # Buds2, Buds2 Pro and Buds FE come in the same rounded-square case as the Buds Live
    "galaxy-buds": [["buds2"], ["buds", "fe"]],
    # JBL's on-ear foldables share the T450's flat band and round cups
    "jbl-t450": [["jbl", "t460"], ["jbl", "t500"], ["jbl", "tune", "500"], ["jbl", "tune", "510"], ["jbl", "tune", "520"]],
}

# shape stand-ins: any headphones whose name gives away their shape borrow the closest model. Used only
# when nothing matches by name above; the app then labels the 3D "similar look". Most words wins.
LOOKS = {
    # earbuds with a white stem-style case ("FreePods", "EarPods"…)
    "airpods-pro": [["pods"]],
    # other earbuds: a rounded case like the Buds Live's
    "galaxy-buds": [["buds"], ["earbuds"], ["tws"], ["liberty"], ["wf1000"], ["wfc"], ["earfun", "free"],
                    ["soundcore", "life", "p"], ["soundcore", "life", "a"], ["earbud"], ["inear"], ["space", "a4"], ["space", "a3"]],
    # on-ear foldables
    # words are about shape, never a look-alike name: "AirPods Max" is no earbud, "Tune Buds" no headphone.
    # Model names a brand uses for one shape only are fine ("Q30" is always Soundcore's over-ear line).
    "jbl-t450": [["onear"], ["jbl", "t4"], ["jbl", "t5"], ["jbl", "tune", "5"], ["whch5"], ["beats", "solo"]],
    # over-ear: the most common big headphones
    "sony-xm4": [["headphone"], ["overear"], ["wh1000"], ["whch7"], ["whxb"], ["ult", "wear"],
                 ["soundcore", "q2"], ["soundcore", "q3"], ["soundcore", "q4"], ["space", "one"],
                 ["bose", "quietcomfort"], ["bose", "qc"], ["bose", "700"], ["momentum"],
                 ["jbl", "tune", "7"], ["jbl", "live", "6"], ["jbl", "live", "7"], ["jbl", "760"], ["jbl", "770"],
                 ["beats", "studio"], ["sennheiser", "hd"]],
}

# size in the frame (1 = fill it like the XM6); compact shapes such as a closed case look too big at 1
SCALE = {"galaxy-buds": 0.62, "airpods-pro": 0.8}
# materials to leave out (the JBL's cable and plug) and the soft white finish for plain white models
HIDE = {"jbl-t450": ["Rubber_black", "Jack"]}
FINISH = {"sony-xm4": "soft-white", "airpods-pro": "soft-white", "airpods-max": "space-gray"}

models = []
for mid, (match, pose, (title, url, author, author_url)) in ENTRIES.items():
    f = HERE / f"{mid}.glb"
    if not f.exists():
        print("skipped (no file):", mid)
        continue
    data = f.read_bytes()
    models.append({"id": mid, "match": match + FAMILY.get(mid, []), **({"looks": LOOKS[mid]} if mid in LOOKS else {}), "file": f.name, "bytes": len(data),
                   "sha256": hashlib.sha256(data).hexdigest(), "pose": pose, "scale": SCALE.get(mid, 1),
                   **({"hide": HIDE[mid]} if mid in HIDE else {}), **({"finish": FINISH[mid]} if mid in FINISH else {}),
                   "credit": {"title": title, "url": url, "author": author, "authorUrl": author_url,
                              "license": CC_BY[0], "licenseUrl": CC_BY[1],
                              # CC BY asks that changes be indicated
                              "changes": ", ".join(x for x in ("recoloured" if mid in FINISH else "",
                                                               "cable hidden" if mid in HIDE else "") if x)}})
(HERE / "models.json").write_text(json.dumps({"version": 1, "models": models}, indent=2) + "\n", encoding="utf-8")
print("models.json:", ", ".join(m["id"] for m in models))
