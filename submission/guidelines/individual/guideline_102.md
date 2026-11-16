# Guideline gán nhãn — v0.2 (cá nhân) — mã 102

- **Phiên bản:** v0.2 (bản cá nhân, viết từ `guideline_v0_starter.md`)
- **Mã thành viên:** 102
- **Người viết:** Bùi Văn Thịnh (MSSV 2A202604040)
- **Ngày:** 16/11/2026
- **Áp dụng cho:** Bounding Box 2D trên ảnh đường phố (CVAT → COCO 1.0)
- **Nền tảng kế thừa:** `guideline_v0_starter.md`

---

## 1. Mục tiêu

Nhãn dữ liệu phục vụ huấn luyện mô hình thị giác máy tính nhận diện **người và phương tiện tham gia giao thông thực tế** trên đường phố cho hệ thống camera giám sát và xe tự hành (ADAS).
- **Yêu cầu cốt lõi:** Nhận diện đúng các thực thể vật lý có khả năng di chuyển hoặc đang tương tác trực tiếp với luồng giao thông.
- **Rủi ro sai sót:** 
  - *Bỏ sót (False Negative):* Bỏ sót người đi bộ, người lái xe máy hoặc xe tải lớn có thể gây tai nạn nghiêm trọng.
  - *Nhận diện nhầm (False Positive):* Nhận diện nhầm ma-nơ-canh, tượng nghệ thuật, ảnh in quảng cáo hoặc hình phản chiếu qua gương sẽ gây ra hiện tượng phanh gấp (phantom braking).

---

## 2. Lớp và Thuộc tính

### 2.1. Định nghĩa Lớp (Classes)

| Lớp | Định nghĩa chuẩn | Ví dụ điển hình | Phản ví dụ / Dễ nhầm lẫn |
|---|---|---|---|
| `car` | Ô tô con từ 4–7 chỗ (sedan, hatchback, coupe), xe SUV, CUV, xe bán tải (pickup) gia đình. | Xe taxi, xe sedan 4 chỗ, xe SUV cá nhân. | **Không gán:** Xe tải thùng hàng riêng → `truck`; Xe van thùng kín chở hàng → `van`; Ô tô đồ chơi mô hình. |
| `truck` | Xe tải chở hàng, xe chuyên dụng có kết cấu ca-bin và thùng hàng tách rời, xe ben, xe đầu kéo container, xe tải chở ô tô. | Xe tải thùng mui bạt, xe ben chở đất, xe chuyên chở ô tô con. | **Không gán:** Xe bán tải nhỏ không cải tạo → `car`; Xe van chở hàng thân liền → `van`. |
| `van` | Xe thân liền, thùng kín cỡ nhỏ đến trung bình, trần phẳng (thường dùng chở bưu kiện hoặc chở khách 9–16 chỗ). | Xe giao hàng bưu phẩm, Ford Transit, Toyota Hiace. | **Không gán:** Xe SUV → `car`; Xe tải thùng rời → `truck`. |
| `motorcycle` | Phương tiện 2 bánh có động cơ (xe máy số, xe tay ga, mô tô phân khối lớn, xe gắn máy). | Xe số, xe ga, xe côn tay, xe cào cào. | **Không gán:** Xe đạp, xe xích lô đạp chân; Xe 3 bánh (tuk-tuk). |
| `person` | **Người thật** (đang đi bộ, đứng, ngồi vỉa hè hoặc đang điều khiển / ngồi trên phương tiện hở). | Người đi bộ qua đường, người điều khiển xe máy, hành khách ngồi trên xe máy/xe xích lô. | **Không gán:** Tượng đài điêu khắc, ma-nơ-canh shop, hình in người trên biển quảng cáo/poster. |
| `ignore_region` | Vùng gom nhóm các vật thể quá đông đúc ở xa, mờ nhòe trong đêm tối hoặc các phương tiện giao thông ngoài taxonomy. | Cụm người/xe quá đông ở hậu cảnh xa xôi; Cụm xe đỗ dày đặc mờ tối ở góc khuất; Xe tuk-tuk. | Không dùng để che lấp các vật thể đứng riêng lẻ, rõ nét ở cự ly gần. |

---

### 2.2. Thuộc tính (Attributes) & Ngưỡng định lượng

Mọi bounding box (ngoại trừ vùng `ignore_region`) bắt buộc phải gán đủ 3 thuộc tính sau:

1. **`occluded_level` (Mức độ che khuất):**
   - **`0` (Thấy rõ):** Vật thể nhìn thấy được $\ge 90\%$ toàn bộ cơ thể/phương tiện.
   - **`1` (Che ít):** Bị che từ $10\%$ đến dưới $35\%$ diện tích bề mặt (ví dụ xe bị cột biển báo che một góc nhỏ).
   - **`2` (Che nhiều):** Bị che từ $35\%$ đến dưới $80\%$ diện tích bề mặt (ví dụ ô tô chỉ lộ đầu hoặc đuôi xe ra khỏi tường).
   - **`3` (Che rất nặng / không rõ):** Bị che $\ge 80\%$, chỉ còn thấy một phần rất nhỏ không chắc chắn.

2. **`truncated` (Cắt mép ảnh):**
   - **`no`:** Toàn bộ vật thể nằm trọn vẹn bên trong khung hình.
   - **`yes`:** Vật thể bị biên của ảnh cắt ngang làm mất một phần thân.

3. **`can_review` (Cờ cần kiểm tra lại):**
   - **`false` (mặc định):** Người gán tự tin với nhãn và box đã vẽ.
   - **`true`:** Trường hợp mơ hồ, ca biên đặc biệt cần đưa ra thảo luận trong buổi họp Calibration.

---

## 3. Quy tắc vẽ Bounding Box (Quy chuẩn thực hành)

- **`R-01` [Visible Box]:** Bounding box phải vẽ **ôm sát phần nhìn thấy thực tế (visible)** của vật thể. Không tưởng tượng vẽ xuyên qua chướng ngại vật và không vẽ tràn ra ngoài mép ảnh.
- **`R-02` [Tách người và xe máy]:** Đối với người ngồi trên xe máy (`motorcycle`), bắt buộc vẽ **2 box độc lập**:
  - 1 box `person` (ôm từ đỉnh đầu/mũ bảo hiểm đến phần cơ thể nhìn thấy).
  - 1 box `motorcycle` (ôm toàn bộ khung xe nhìn thấy từ bánh trước đến bánh sau). Box người và box xe được phép chồng đè lên nhau.
- **`R-03` [Người trong phương tiện kín]:** Người ngồi bên trong ô tô con (`car`), xe tải (`truck`), xe van (`van`) có cửa và kính che kín thì **KHÔNG gán nhãn `person`**.
- **`R-04` [Hàng hóa trên phương tiện]:**
  - Hàng hóa thông thường trên thùng xe bán tải hoặc sau yên xe máy: Box xe ôm trọn cả hàng hóa nếu hàng gắn liền với phương tiện.
  - Trường hợp đặc biệt xe tải chở ô tô con: Xe tải vẽ 1 box lớn `truck`; các ô tô con nằm trên giá đỡ sàn xe **vẫn vẽ từng box riêng biệt là `car`** (kèm mức `occluded_level` tương ứng).
- **`R-05` [Vật thể phi thực / Giả lập]:** Tượng điêu khắc, ma-nơ-canh cửa hàng, hình người/xe in trên poster biển quảng cáo, tranh vẽ tường, xe đồ chơi/mô hình nhỏ trưng bày trong tủ kính $\rightarrow$ **TUYỆT ĐỐI KHÔNG GÁN NHÃN**.
- **`R-06` [Ảnh phản chiếu]:** Hình ảnh phản chiếu người hoặc xe trong gương chiếu hậu, mặt kính tòa nhà hay vũng nước $\rightarrow$ **KHÔNG GÁN**.
- **`R-07` [Kích thước tối thiểu]:** Vật thể có chiều cao dưới $20\text{ px}$ hoặc mờ nhòe, quá tối ở xa không thể xác định lớp bằng mắt thường $\rightarrow$ **Bỏ qua** hoặc gom vào `ignore_region` nếu là cụm đông.
- **`R-08` [Phương tiện phi chuẩn]:** Xe xích lô đạp chân, xe kéo, xe tuk-tuk 3 bánh $\rightarrow$ người điều khiển/hành khách gán `person`, phần thân xe nếu không thuộc 4 lớp phương tiện thì khoanh vào `ignore_region` (hoặc không gán).

---

## 4. Phân loại các Nhóm Ca Khó Điển hình

| Nhóm ca khó | Tình huống thực tế | Quy tắc áp dụng | Quyết định xử lý chuẩn |
|---|---|---|---|
| **Người trên xe 2 bánh** | Người điều khiển / người ngồi sau xe máy. | `R-02` | Tách 2 box: 1 box `person` + 1 box `motorcycle`. |
| **Vật thể chở trên xe tải** | Xe chuyên dụng chở ô tô con trên sàn xe. | `R-04` | Vẽ 1 box `truck` cho xe tải, vẽ từng box `car` cho ô tô trên sàn. |
| **Vật thể trưng bày / Tượng** | Tượng nghệ thuật, tượng đài công viên, ma-nơ-canh shop. | `R-05` | Không gán (tránh phantom braking). |
| **Hình in 2D / Quảng cáo** | Biển quảng cáo in hình người hoặc xe. | `R-05` | Không gán. |
| **Gương phản chiếu** | Người/xe phản chiếu trong gương chiếu hậu. | `R-06` | Không gán (chỉ gán thực thể vật lý trực tiếp). |
| **Phương tiện ngoài phân loại** | Xe tuk-tuk 3 bánh, xích lô du lịch. | `R-08` | Người gán `person`; xe đưa vào `ignore_region` hoặc bỏ qua. |
| **Vật thể bị che khuất nặng** | Chỉ thấy 1 phần nhỏ qua khe hở tường/cột. | `R-01` | Vẽ ôm sát phần thấy, đặt `occluded_level = 2` hoặc `3`. |

---

## 5. Tiêu chuẩn QC và Lịch sử Phiên bản

### 5.1. Ngưỡng nghiệm thu chất lượng (QC Gates)
- **Độ đồng thuận IoU ($\text{IAA IoU}$):** $\ge 0.85$ (trung bình trên các cặp box khớp nhau).
- **Độ đồng thuận phân lớp ($\text{IAA Class}$):** $\ge 95\%$.
- **Tỷ lệ ảnh lỗi toàn lô:** $\le 2.0\%$ (trên 40 ảnh đã duyệt).

### 5.2. Lịch sử thay đổi

| Phiên bản | Thay đổi chính | Căn cứ phát sinh |
|---|---|---|
| `v0` | Bản khởi đầu của BTC (sơ sài, chưa có quy tắc tách box và xử lý ca biên). | Mẫu khởi tạo ban đầu. |
| `v1.0` | Chuẩn hóa 6 lớp, định lượng rõ ràng 4 mức `occluded_level`, bổ sung quy tắc `R-01` đến `R-08` (tách box người/xe máy, loại bỏ tượng, ma-nơ-canh, hình in, gương phản chiếu). | Đúc kết từ khảo sát thực tế 40 ảnh đường phố. |

