# Báo cáo QC — NhomBanDau

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: thực hành đặc tả và QC nhãn bounding box 2D (COCO 1.0) cho 40 ảnh giao thông. Tập ảnh tuyển chọn để luyện ca biên, chưa đánh giá độ đại diện cho dữ liệu vận hành.
- Nguồn và phép sử dụng dữ liệu: xem `data/ATTRIBUTION.csv` (tác giả, giấy phép, URL từng ảnh); giữ ghi công khi chia sẻ lại.
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json`; SHA-256 `labels_calibrated.json` ghi trong manifest (trường `labels.sha256`).
- Guideline và taxonomy khi gán / khi bàn giao: gán bằng guideline v1.0 + taxonomy v1.0; bàn giao guideline v1.1 (editorial, không đổi nghĩa quy tắc), taxonomy giữ v1.0.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 (4 người gán 102, 107, 113, 515; mỗi ảnh 2 lượt).
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: 270 cặp box ghép; IoU TB 0.884; cùng lớp 98.5% (trên 270 cặp). Cặp 107|113 (IoU 0.832) và 107|515 (có tỉ lệ cùng truncated/occluded thấp) chưa đạt ngưỡng.
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 63/109 box chưa ghép (A/B), 3 box loại do ignore; 117 ca `bat_dong_ignore` (chủ yếu img_021, img_030, img_032).
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: `occluded_level` chỉ khớp 54.8%: nhiều cặp cùng chọn một mức nhưng bảng mức che mục 2 mơ hồ ở ảnh đông (img_021). Kiểm bằng cách đo lại tỉ lệ che trên vài box trong CVAT; chưa làm hết.

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 548/548 ca có dòng trong `submission/qc/calibration_decisions.csv` (người chốt 113; quy tắc R-01, R-05, R-12, R-13, R-18, R-20). Bản sửa chi tiết 26 thay đổi: `submission/qc/proposals/113_calibration_fixes.csv`. Sau QC vòng 2 thêm 2 ca Q01 (img_019), Q02 (img_030), người chốt 107, quy tắc R-05; COCO sau sửa `labels_calibrated_f2094d70f8aab17a.json`.
- Tác động v1.1 lên nhãn và ảnh: `kind=editorial`, phạm vi `anh`; 35/40 ảnh qua calibration, trong đó 7 ảnh áp bản sửa của 113, 28 ảnh giữ nhãn đồng thuận. Cờ `can_review` được hạ vì mỗi ca đã có quyết định.
- Tham chiếu bằng chứng khi Rework: vòng 2 (107) ra Rework vì 2/40 ảnh bỏ sót theo R-05 → ca Q01, Q02 trong `calibration_decisions.csv` → thêm 2 `ignore_region` → `build_final.py` → vòng 3. Phiếu vòng 1, 2 giữ nguyên trong `reviews/round-01/`, `round-02/`.

## 4. Kết quả duyệt

- Vòng QC: 3
- Người review và ngày: vòng 1: 113; vòng 2 và 3: 107 (người review bản cuối, duyệt độc lập), 2026-11-16
- Đã duyệt / cả lô: 40/40 ở cả ba vòng
- Ảnh lỗi / ảnh đã duyệt: vòng 1: 0/40 = 0.0%; vòng 2: 2/40 = 5.0% (Rework); vòng 3: 0/40 = 0.0%
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: 0/432 = 0.0% ở cả ba vòng (lỗi vòng 2 là bỏ sót, không nằm trên box có sẵn)
- Vật bỏ sót, ảnh và vùng (vòng 2): img_019 vùng x 0-258, y 0-410 (đám đông sau rào bên trái, không có box hay ignore_region); img_030 vùng x 445-700, y 45-155 (cụm xe máy dựng phía sau). Cả hai đã gom `ignore_region` theo R-05.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: vòng 2 ca_kho 2/35 ảnh lỗi, con_lai 0/5; vòng 3 ca_kho 0/35, con_lai 0/5; phiếu `submission/qc/reviews/round-03/qc_review.csv`. Hai lỗi cùng kiểu (bỏ sót cụm đông, R-05) nhưng đã sửa và không còn ở vòng 3.
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: máy chặn được box thiếu thuộc tính / sai schema (`validate_labels.py`) và cờ `can_review` còn sót (`qc_report.py` ra HOLD lần đầu). Cần người đọc ảnh: box có ôm sát vật không, vật bỏ sót ở vùng đông (img_021, img_030).

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: vòng 3 có 0 lỗi trên 40/40 ảnh duyệt sau khi sửa 2 ca bỏ sót của vòng 2; taxonomy/guideline khớp. Người nhận: coach, dùng cho thực hành đặc tả/QC.
- Nếu còn việc: (1) vòng 2 và 3 do 107 duyệt với hỗ trợ AI (xem `individual_notes/107.md`); 107 vừa chốt Q01/Q02 vừa duyệt vòng 3, nên đề nghị 113 xem lại img_019, img_030 trong CVAT; (2) 28 ảnh calibration chưa sửa tay trong CVAT; (3) duyệt dựa trên ảnh chồng nhãn, không đo từng mép box theo R-01; (4) `ignore_region` img_019 phủ nhẹ mép đèn trái của xe #200.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: ca C001 (img_001) → `calibration_decisions.csv` → R-16 → `113_calibration_fixes.csv` (thêm person thứ hai) → `labels_calibrated.json`.
