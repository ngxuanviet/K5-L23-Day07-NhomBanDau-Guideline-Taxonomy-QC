# Thông tin nhóm

- Tên nhóm: NhomBanDau
- Mã thành viên (ba chữ số): 515, 113, 107, 102 
- Người điều phối: 515
- Người review bản cuối: 107
- Commit chốt bài (điền ở kênh nộp sau khi commit): xem commit merge PR Pha 5-6 trên `main`

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: 80/80
- IAA trước calibration (kèm mẫu số): IoU TB 0.884, cùng lớp 98.5%, trên 270 cặp box ghép, 40 ảnh, 4 người gán (tổng ĐẠT; cặp 107|113 và 107|515 chưa đạt)
- Số ảnh phải calibration: 35 / 40
- Vòng QC và số ảnh đã duyệt / cả lô: vòng 3, 40/40 (vòng 1: 113 Release; vòng 2: 107 Rework 2/40; vòng 3: 107 Release)
- Tỉ lệ lỗi: 0.0 % theo ảnh (0/40), 0.0 % theo đối tượng (0/432)
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: Release ở vòng 3 — 107 duyệt độc lập phát hiện 2 ảnh bỏ sót cụm đông (R-05), đã sửa (Q01, Q02) và duyệt lại 0/40 lỗi
