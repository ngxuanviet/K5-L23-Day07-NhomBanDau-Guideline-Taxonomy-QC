# Tóm tắt IAA (taxonomy v1.0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 4
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 270 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Cùng person_state | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 270 | 0.884 | 98.5% | 54.8% | 94.8% | 92.6% | 63/109 | 3 | ĐẠT |
| 102|107 | 6 | 26 | 0.860 | 100.0% | 42.3% | 100.0% | 96.2% | 7/2 | 0 | ĐẠT |
| 102|113 | 9 | 81 | 0.912 | 98.8% | 70.4% | 98.8% | 92.6% | 41/18 | 0 | ĐẠT |
| 102|515 | 5 | 60 | 0.896 | 100.0% | 41.7% | 95.0% | 83.3% | 6/17 | 0 | ĐẠT |
| 107|113 | 5 | 26 | 0.832 | 92.3% | 46.2% | 73.1% | 100.0% | 3/30 | 0 | CHƯA ĐẠT |
| 107|515 | 9 | 45 | 0.845 | 100.0% | 66.7% | 100.0% | 100.0% | 4/27 | 0 | CHƯA ĐẠT |
| 113|515 | 6 | 32 | 0.909 | 96.9% | 40.6% | 90.6% | 90.6% | 2/15 | 3 | ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 548 ({'bo_sot_thua': 75, 'co_can_review': 144, 'iou_thap': 64, 'sai_thuoc_tinh': 144, 'bat_dong_ignore': 117, 'sai_lop': 4}), trên 35 ảnh cần calibration.
