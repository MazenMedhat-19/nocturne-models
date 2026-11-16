# Nocturne model library

3D models of headphones for the Nocturne app. The app reads `models.json`, matches the connected
headphones' name on the user's PC, and downloads only the matching `.glb`, once.

- `models.json`: the index (names each model stands for, pose, size, SHA-256). Written by `build_index.py`.
- `*.glb`: the models.

To add a model: put the `.glb` here, add it to `ENTRIES` in `build_index.py`, run
`python build_index.py`, commit both. The app picks it up within 12 hours, no app update needed.

## Credits

Every model is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) by its author.
The app recolours some of them or hides parts at display time; the files here are unchanged.

| File | Model | Author |
|---|---|---|
| `airpods-pro.glb` | [AirPods Pro](https://sketchfab.com/3d-models/airpods-pro-2a97b522bd1e43ffa342e4a19ff21e35) | [eltayerkebulan](https://sketchfab.com/eltayerkebulan) |
| `airpods-max.glb` | [Airpods max](https://sketchfab.com/3d-models/airpods-max-05181e126a6341668ca95f2d98324d30) | [Mr.Philin](https://sketchfab.com/yarik.chilin) |
| `sony-xm4.glb` | [SONY headphone WH-1000XM4](https://sketchfab.com/3d-models/sony-headphone-wh-1000xm4-f90f76c75d8143eb97eb49844050aa26) | [Chizuko V](https://sketchfab.com/chizuk0) |
| `sony-xm5.glb` | [Sony Wh-1000xm5](https://sketchfab.com/3d-models/sony-wh-1000xm5-5d8aea0a780b49fa89c9c205912414e3) | [Zalanekee](https://sketchfab.com/Zalanekee) |
| `galaxy-buds.glb` | [Samsung Galaxy Buds Live](https://sketchfab.com/3d-models/samsung-galaxy-buds-live-7e4a0f2202144b91b4c47ffbfdf94584) | [DatSketch](https://sketchfab.com/DatSketch) |
| `jbl-t450.glb` | [JBL T450](https://sketchfab.com/3d-models/jbl-t450-6db4c5b60e124d40a8be06ec1fe22c67) | [Oleksii Rozumnyi](https://sketchfab.com/Oleksii.Rozumnyi) |

## Trademarks

Product names belong to their owners (Apple, Sony, Samsung, Harman/JBL). Nocturne is not affiliated
with or endorsed by any of them; the names describe which headphones a model is for.
