# Guideline gán nhãn — v0.2 (cá nhân) — mã 105

- **Phiên bản:** v0.2 (bản cá nhân, viết từ `guideline_v0_starter.md`)
- **Mã thành viên:** 107
- **Người viết:** Trần Nguyễn Phi Long
- **Ngày:** 16/11/2026
- **Áp dụng cho:** Bounding Box 2D cho Biển báo và Đèn tín hiệu giao thông (CVAT → COCO 1.0)
- **Nền tảng kế thừa:** `guideline_v0_starter.md`

---

## 1. Mục tiêu

Nhãn dữ liệu phục vụ huấn luyện mô hình thị giác máy tính nhận diện **biển báo giao thông và đèn tín hiệu đường bộ** nhằm hỗ trợ hệ thống cảnh báo sớm và điều khiển xe tự hành (ADAS) tuân thủ luật giao thông.
- **Yêu cầu cốt lõi:** Nhận diện chính xác vị trí, chủng loại biển báo và trạng thái đèn tín hiệu để mô hình ra quyết định điều hướng đúng thời điểm.
- **Rủi ro sai sót:** 
  - *Bỏ sót (False Negative):* Bỏ sót biển cấm tốc độ, biển cấm ngược chiều hoặc đèn đỏ có thể dẫn đến vi phạm luật giao thông nghiêm trọng hoặc tai nạn.
  - *Nhận diện nhầm (False Positive):* Nhận diện nhầm biển hiệu quảng cáo thương mại, đèn trang trí đô thị thành đèn giao thông sẽ gây ra hiện tượng phanh gấp hoặc xử lý sai tình huống (phantom braking/steering).

---

## 2. Lớp và Thuộc tính

### 2.1. Định nghĩa Lớp (Classes)

| Lớp | Định nghĩa chuẩn | Ví dụ điển hình | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `traffic_sign_prohibitory` | Biển báo cấm hoặc hiệu lệnh (thường có hình tròn, viền đỏ nền trắng hoặc nền xanh dương đặc trưng). | Biển cấm đi ngược chiều, biển cấm rẽ trái, biển tốc độ tối đa. | **Không gán:** Biển quảng cáo tròn ngoài đường; Biển tên đường màu xanh chữ trắng. |
| `traffic_sign_warning` | Biển báo nguy hiểm/cảnh báo (hình tam giác đều, viền đỏ nền vàng có biểu tượng màu đen ở giữa). | Biển báo giao nhau với đường ưu tiên, đường trơn trượt, khu vực có trẻ em. | **Không gán:** Biển chỉ dẫn hình chữ nhật; Biển báo công trường tạm thời không rõ biểu tượng. |
| `traffic_sign_informative` | Biển chỉ dẫn, hướng dẫn thông tin giao thông (hình chữ nhật hoặc vuông, chủ yếu nền xanh dương hoặc nền trắng). | Biển chỉ dẫn lối đi bộ qua đường, biển báo đường cao tốc, biển chỉ dẫn làn đường. | **Không gán:** Biển hiệu quảng cáo cửa hàng, biển tên công ty bên đường. |
| `traffic_light` | Cụm đèn tín hiệu giao thông điều khiển phương tiện (đèn xanh, vàng, đỏ tại các nút giao hoặc làn đường riêng). | Đèn tín hiệu 3 màu giao lộ, đèn tín hiệu dành riêng cho rẽ trái/phải. | **Không gán:** Đèn trang trí cây xanh ven đường, đèn hiệu cửa hàng LED nhấp nháy. |
| `ignore_region` | Vùng gom nhóm các biển báo quá mờ nhòe trong đêm tối, bị biến dạng nặng hoặc các biển quảng cáo/biển hiệu không thuộc hệ thống quy chuẩn giao thông quốc gia. | Cụm biển hiệu quảng cáo dày đặc ở mặt tiền cửa hàng; Biển báo bị rách nát, phai màu hoàn toàn. | Không dùng để che lấp các biển báo chính thức, rõ nét có ý nghĩa điều tiết giao thông. |

---

### 2.2. Thuộc tính (Attributes) & Ngưỡng định lượng

Mọi bounding box (ngoại trừ vùng `ignore_region`) bắt buộc phải gán đủ các thuộc tính sau:

1. **`occluded_level` (Mức độ che khuất):**
   - **`0` (Thấy rõ):** Biển báo hoặc đèn nhìn thấy được $\ge 90\%$ diện tích bề mặt.
   - **`1` (Che ít):** Bị che từ $10\%$ đến dưới $35\%$ diện tích (ví dụ một góc biển bị cành cây che nhẹ).
   - **`2` (Che nhiều):** Bị che từ $35\%$ đến dưới $80\%$ diện tích bề mặt.
   - **`3` (Che rất nặng / không rõ):** Bị che $\ge 80\%$, chỉ còn lộ một phần nhỏ không chắc chắn nhận diện được loại biển.

2. **`truncated` (Cắt mép ảnh):**
   - **`no`:** Toàn bộ biển báo/đèn nằm trọn vẹn trong khung hình.
   - **`yes`:** Bị biên của ảnh cắt ngang làm mất một phần cấu trúc.

3. **`light_state` (Trạng thái đèn - *chỉ áp dụng riêng cho lớp `traffic_light`*):**
   - **`red`:** Đèn đang hiển thị tín hiệu đỏ.
   - **`yellow`:** Đèn đang hiển thị tín hiệu vàng.
   - **`green`:** Đèn đang hiển thị tín hiệu xanh.
   - **`off` / `unknown`:** Đèn tắt hoặc không phân biệt rõ màu do lóa sáng mạnh.

4. **`can_review` (Cờ cần kiểm tra lại):**
   - **`false` (mặc định):** Người gán tự tin với nhãn và box đã vẽ.
   - **`true`:** Trường hợp mơ hồ, biển báo lạ hoặc bị lóa sáng nặng cần đưa ra thảo luận trong buổi họp Calibration.

---

## 3. Quy tắc vẽ Bounding Box (Quy chuẩn thực hành)

- **`R-01` [Visible Box]:** Bounding box phải vẽ **ôm sát phần nhìn thấy thực tế (visible)** của mặt biển báo hoặc hộp đèn tín hiệu. Không bao gồm phần cột chống hay khung sắt giá đỡ phía sau/dưới (trừ khi không thể tách rời).
- **`R-02` [Biển báo kèm biển phụ]:** Trường hợp biển báo chính có gắn thêm biển phụ bên dưới (biển hình chữ nhật ghi chú thích khoảng cách hoặc thời gian), **bắt buộc vẽ chung 1 box lớn** bao trùm cả biển chính và biển phụ liền kề thành một khối thống nhất.
- **`R-03` [Cụm đèn tín hiệu]:** Đối với hộp đèn giao thông dọc/ngang nhiều bóng, vẽ ôm trọn **toàn bộ hộp đèn chứa các mắt đèn** (hoặc tách riêng từng mắt đèn nếu có yêu cầu dự án cụ thể; chuẩn chung mặc định là vẽ nguyên cụm hộp đèn).
- **`R-04` [Biển quảng cáo thương mại]:** Các biển hiệu quảng cáo sản phẩm, tên nhà hàng, banner dọc vỉa hè $\rightarrow$ **TUYỆT ĐỐI KHÔNG GÁN NHÃN**.
- **`R-05` [Ảnh phản chiếu / Màn hình]:** Biển báo hiển thị qua màn hình điện tử/tivi hoặc hình phản chiếu qua gương chiếu hậu/kính tòa nhà $\rightarrow$ **KHÔNG GÁN**.
- **`R-06` [Kích thước tối thiểu]:** Biển báo hoặc đèn có chiều rộng/cao dưới $15\text{ px}$ hoặc mờ nhòe ở cự ly quá xa không phân biệt được hình dáng/biểu tượng $\rightarrow$ **Bỏ qua** hoặc gom vào `ignore_region`.
- **`R-07` [Đèn trang trí đô thị]:** Các dải đèn LED quấn cây, đèn trang trí lễ hội dọc tuyến đường $\rightarrow$ **Không gán** vào lớp `traffic_light`.

---

## 4. Phân loại các Nhóm Ca Khó Điển hình

| Nhóm ca khó | Tình huống thực tế | Quy tắc áp dụng | Quyết định xử lý chuẩn |
|---|---|---|---|
| **Biển báo có biển phụ** | Biển cấm dừng đỗ kèm biển phụ hình chữ nhật phía dưới chỉ thời gian. | `R-02` | Vẽ một box duy nhất bao trọn cả biển chính và biển phụ. |
| **Biển báo bị nghiêng / xoay góc** | Biển báo gắn trên cột bị gió làm xoay lệch góc nhìn phối cảnh (perspective). | `R-01` | Vẽ box ôm sát diện tích mặt biển theo góc nhìn thực tế, đặt `occluded_level = 0` hoặc `1`. |
| **Đèn tín hiệu bị lóa nắng** | Ánh sáng mặt trời chiếu trực diện làm lóa màu đèn giao thông. | `R-03` | Vẫn vẽ box `traffic_light`, gán thuộc tính `light_state = unknown` và bật `can_review = true`. |
| **Biển hiệu quảng cáo giao thông giả** | Biển quảng cáo của cửa hàng có hình dáng giống biển báo giao thông. | `R-04` | Không gán (tránh gây nhầm lẫn cho mô hình). |
| **Biển báo bị che khuất một phần** | Cành cây hoặc tán lá che một phần mặt biển báo. | `R-01` | Vẽ ôm sát phần biển còn lộ diện, đánh giá đúng mức `occluded_level` (1 hoặc 2). |
| **Đèn trang trí đường phố** | Đèn nhấp nháy trang trí dọc thân cây hoặc vỉa hè. | `R-07` | Không gán vào bất kỳ lớp nào. |

---

## 5. Tiêu chuẩn QC và Lịch sử Phiên bản

### 5.1. Ngưỡng nghiệm thu chất lượng (QC Gates)
- **Độ đồng thuận IoU ($\text{IAA IoU}$):** $\ge 0.90$ (do kích thước biển báo thường nhỏ, đòi hỏi độ chính xác viền cao).
- **Độ đồng thuận phân lớp & thuộc tính ($\text{IAA Class & Attr}$):** $\ge 98\%$.
- **Tỷ lệ ảnh lỗi toàn lô:** $\le 1.5\%$ (trên 40 ảnh đã duyệt).

### 5.2. Lịch sử thay đổi

| Phiên bản | Thay đổi chính | Căn cứ phát sinh |
|---|---|---|
| `v0` | Bản khởi đầu chung của BTC cho đối tượng giao thông tĩnh. | Mẫu khởi tạo ban đầu. |
| `v1.0` | Chuẩn hóa 4 lớp biển/đèn, bổ sung thuộc tính `light_state`, quy tắc gom biển phụ (`R-02`) và loại trừ triệt để biển quảng cáo/đèn trang trí. | Đúc kết từ đợt kiểm thử nhãn trên 40 khung hình đô thị phức tạp. |