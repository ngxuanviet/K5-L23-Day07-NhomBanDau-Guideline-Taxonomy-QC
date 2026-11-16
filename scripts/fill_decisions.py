"""Điền calibration_decisions.csv theo loại ca IAA, dẫn quy tắc có sẵn trong guideline v1.0 (không đổi nghĩa)."""
from __future__ import annotations

import csv

from common import QC_DIR, read_csv, write_csv
from calibration import DECISION_COLUMNS

RULES = {
    "sai_lop": ("R-18", "Chốt lớp theo R-18 (cửa sổ bên, thùng tách cabin); lớp của người gán đúng quy tắc được giữ."),
    "bo_sot_thua": ("R-12", "Giữ box khi nhận ra lớp theo R-12 (đầu+vai / bánh+thân), R-04 cao >=20 px; ngược lại bỏ."),
    "iou_thap": ("R-01", "Box ôm sát phần nhìn thấy theo R-01; R-16 một vật một box; R-09 không nới theo hàng."),
    "sai_thuoc_tinh": ("R-13", "Chốt truncated theo R-13 (chạm mép ảnh), occluded_level theo bảng mức che ở mục 2."),
    "bat_dong_ignore": ("R-05", "Vật tách riêng khi >=20 px và thấy đủ hai mép; phần dính liền gom 1 ignore_region (R-05/R-14)."),
    "co_can_review": ("R-20", "Ca mơ hồ gắn can_review: chốt theo quy tắc liên quan, giữ cờ can_review cho người review."),
}
PROPOSAL = "submission/qc/proposals/113_calibration_fixes.csv"


def main() -> None:
    proposed = {r["image"] for r in csv.DictReader(open(ROOT_PROPOSAL, encoding="utf-8-sig"))}
    rows = []
    for row in read_csv(QC_DIR / "calibration_candidates.csv"):
        rule, text = RULES[row["issue_type"]]
        fixed = row["image"] in proposed
        rows.append({
            "case_id": row["case_id"], "image": row["image"],
            "quyet_dinh": text,
            "quy_tac_ghi_vao_guideline": rule,
            "phien_ban_guideline": "v1.1",
            "nguoi_chot": "113",
            "phieu_sua": f"{PROPOSAL} (ảnh {row['image']})" if fixed else "giữ nhãn đồng thuận consensus_draft.json",
            "kiem_lai": "113 tự đối chiếu theo quy tắc; 107 (review bản cuối) xác nhận ở Pha 6",
            "pham_vi": "anh",
        })
    write_csv(QC_DIR / "calibration_decisions.csv", DECISION_COLUMNS, rows)
    print(f"Đã điền {len(rows)} ca.")


ROOT_PROPOSAL = QC_DIR / "proposals" / "113_calibration_fixes.csv"

if __name__ == "__main__":
    main()
