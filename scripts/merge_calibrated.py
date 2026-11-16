"""Gộp COCO sau sửa: ảnh có trong phiếu sửa lấy từ đề xuất 113, ảnh còn lại giữ đồng thuận."""
import csv, json, sys
from pathlib import Path

Q = Path("submission/qc")
prop = json.loads((Q / "proposals/113_calibrated_proposal.json").read_text(encoding="utf8"))
cons = json.loads(Path("work/calib/consensus_flagged.json").read_text(encoding="utf8"))
fixed = {r["image"] for r in csv.DictReader(open(Q / "proposals/113_calibration_fixes.csv", encoding="utf-8-sig"))}
assert {c["id"]: c["name"] for c in prop["categories"]} == {c["id"]: c["name"] for c in cons["categories"]}
pid = {i["file_name"]: i["id"] for i in prop["images"]}
out = dict(cons, images=[], annotations=[])
for img in cons["images"]:
    name = img["file_name"]
    src, sid = (prop, pid[name]) if name in fixed and name in pid else (cons, img["id"])
    nid = len(out["images"]) + 1
    out["images"].append(dict(img, id=nid))
    for a in src["annotations"]:
        if a["image_id"] == sid:
            at = {k: v for k, v in a["attributes"].items() if k != "needs_calibration"}
            at["can_review"] = False  # ca đã có quyết định trong calibration_decisions.csv
            out["annotations"].append(dict(a, id=len(out["annotations"]) + 1, image_id=nid, attributes=at))
Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
print(len(out["images"]), "ảnh,", len(out["annotations"]), "box; lấy từ đề xuất 113:", len(fixed & set(pid)), "ảnh")
