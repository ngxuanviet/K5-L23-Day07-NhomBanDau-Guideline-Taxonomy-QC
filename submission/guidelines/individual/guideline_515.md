# Guideline gán nhãn — v0.1 (cá nhân) — 515

- Phiên bản: v0.1 (bản cá nhân Pha 1, sửa từ v0)
- Ngày: 2026-11-16
- Người viết: 515 · Người duyệt: chưa có (chờ họp nhóm Pha 2)
- Loại nhãn: bounding box trên ảnh 2D, CVAT, xuất COCO 1.0

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện cơ giới thật đang có mặt trên đường**, cho camera giao thông hoặc xe tự lái.

Hai loại sai nguy hiểm nhất:

- **Bỏ sót người thật** (người đi bộ, người ngồi trên xe máy): mô hình không thấy người thì hệ thống phía sau không phanh.
- **Gán vật giả là vật thật** (tượng, ma-nơ-canh, ảnh in, phản chiếu, đồ chơi): mô hình học báo động giả.

Phép thử dùng xuyên suốt: *"Mô hình có cần phát hiện vật này để ra quyết định trên đường không?"* Nếu không, đừng gán nó thành lớp vật.

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô chở người thân liền, có mũi xe, tối đa 3 hàng ghế: sedan, hatchback, SUV, taxi. | Mazda bạc `img_012`; Civic đen `img_023`; taxi xanh `img_040` | Pickup (→ `truck`); xe một khối cửa trượt (→ `van`); xe mô hình `img_038` (không gán) |
| `truck` | Xe có **thùng hoặc sàn chở hàng tách khỏi cabin**: xe tải, pickup, đầu kéo kèm rơ-moóc. | Pickup Suzuki `img_001`; xe tải Isuzu `img_007`; xe chở xe `img_002`; pickup có nắp thùng `img_037`; Veryca `img_036` | Tượng pickup bằng đá `img_027` (không gán); van thùng liền cabin |
| `van` | Xe **một khối**, không có mũi xe rõ, khoang sau liền cabin, **tối đa 4 cửa sổ bên mỗi phía**. | Xe bạc 51LD `img_005`; van trắng `img_016` | Từ 5 cửa sổ bên trở lên hoặc có cửa lên xuống kiểu xe khách là xe buýt (ngoài taxonomy), ví dụ `img_009` |
| `motorcycle` | Xe hai bánh gắn máy hoặc chạy điện **không có bàn đạp**: xe số, xe ga, mô tô, xe máy điện; xe có thùng bên (sidecar) vẫn là một `motorcycle`. | Xe ga `img_010`; xe điện `img_029`; mô tô có sidecar `img_022` | Xe đạp, xích lô, tuk-tuk ba bánh (ngoài taxonomy) |
| `person` | Người thật, nhìn thấy trực tiếp: đi bộ, đứng, ngồi, hoặc ngồi trên xe hở. | Hai người qua đường `img_014`; hai người trên xe máy `img_026` | Tượng `img_017`; ma-nơ-canh `img_033`; ảnh người trên biển quảng cáo `img_018`; người sau kính ô tô |
| `ignore_region` | Vùng không gán từng vật; bỏ sót trong vùng này không tính lỗi. Không phải một loại vật. | Đám xe máy phía xa `img_021`; bãi xe `img_030`; đám đông sau rào `img_019` | Không dùng để né một vật tách được rõ ràng |

### Vật không thuộc lớp nào (R-10)

- **Xe cơ giới ngoài taxonomy** (xe buýt, xe khách, tuk-tuk, xe lam ba bánh): vẽ **một `ignore_region` ôm sát xe**. Lý do: chúng rất giống `truck` / `van` / `motorcycle`; nếu để làm nền, mô hình bị dạy rằng "vật giống xe tải là nền".
- **Xe không động cơ** (xe đạp, xích lô, xe đẩy, quang gánh): **không gán**.
- **Người ngồi trên các xe đó** vẫn gán `person` theo R-03.
- Đề xuất nhóm bàn ở Pha 2: có thêm lớp `bus` và `three_wheeler` không. Tuk-tuk xuất hiện ở ít nhất 4 ảnh (`img_004`, `img_016`, `img_035`, `img_040`).

### Thuộc tính

**`occluded_level`** — phần của vật bị **vật khác** che, tính trên diện tích ước lượng của cả vật. Cắt bởi mép ảnh không tính là che (dùng `truncated`).

| Mức | Ngưỡng | Ví dụ |
|---|---|---|
| `0` | Không bị che (dưới 5%) | Người qua đường `img_034` |
| `1` | Che từ 5% đến dưới 30% | Xe máy bị chân người lái che một phần |
| `2` | Che từ 30% đến 70% | Xe máy chở hai người nhìn ngang `img_026` |
| `3` | Che trên 70% nhưng vẫn nhận ra lớp | Người chỉ lộ đầu và vai sau người khác `img_005` |

v0 ghi mức 3 là "không rõ". Tôi bỏ nghĩa đó: không chắc thì dùng `can_review`, còn `occluded_level` chỉ đo mức che.
Phần nhìn thấy không đủ để nhận ra lớp (ví dụ chỉ thấy gương chiếu hậu): **không gán**.

**`truncated`** — `yes` khi box chạm mép ảnh **và** vật rõ ràng còn tiếp tục ngoài khung; còn lại `no`.

**`can_review`** — tick khi bạn đã chọn một phương án nhưng không chắc về lớp hoặc về việc vật có thật không. Vẫn phải vẽ box và chọn lớp theo phán đoán tốt nhất; tick không thay cho quyết định.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| **R-01** | Box ôm sát **phần nhìn thấy** của vật, lệch mép tối đa khoảng 2 px. Không đoán phần bị che hay phần ngoài khung. Lý do: ngưỡng IoU của lô là 0,85; đoán phần khuất thì mỗi người đoán một kiểu. |
| **R-02** | **Người đi xe máy: tách box.** Mỗi người một box `person`; chiếc xe một box `motorcycle` **chỉ bao phần xe nhìn thấy**, không nới ra để bao người. Xe bị người che thì ghi `occluded_level` theo ngưỡng. Lý do: xe đỗ không người vẫn là `motorcycle`, nên box xe phải có cùng nghĩa dù có người hay không. |
| **R-03** | **Người trên xe:** gán `person` khi nhìn thấy trực tiếp (xe máy, tuk-tuk, xích lô, xe mui trần, thùng xe hở). Người trong cabin kín chỉ thấy qua kính: **không gán**, coi là một phần của xe. |
| **R-04** | **Vật nhỏ:** box cao dưới **20 px** (đo trên ảnh gốc) thì không gán. Ngưỡng lấy từ `rules.min_box_height_px`. |
| **R-05** | **Đám đông, bãi xe:** một vật được gán riêng khi cao từ 20 px **và** thấy được cả mép trái lẫn mép phải của nó. Phần còn lại, nơi các vật chồng nhau liên tục không tách được ranh, gom vào **một `ignore_region`** ôm sát vùng đó. |
| **R-06** | **Vật không thật** (tượng, ma-nơ-canh, ảnh in, biển quảng cáo, đồ chơi, mô hình, hình nộm): **không gán**, kể cả `ignore_region`. Lý do: mô hình cần học đây là nền. Người thật mặc đồ hóa trang vẫn là `person`. |
| **R-07** | **Phản chiếu** (gương, kính, vũng nước): không gán. |
| **R-08** | **Xe chủ (ego):** phần xe của chính người chụp lọt vào khung thì không gán. |
| **R-09** | **Hàng hóa và đồ mang theo:** box xe bao thân xe; hàng nhô ra ngoài thân (ống dài, bao tải chất cao) **không làm nới box**. Box người bao cơ thể cùng thứ đội hoặc đeo sát người (mũ, ba lô); không bao đồ cầm tay, quang gánh. |
| **R-11** | **Xe chở xe:** xe kéo gán một box `truck` bao đầu kéo và rơ-moóc; **mỗi ô tô thật trên giàn gán một box `car`** kèm `occluded_level`. Lý do: đó là ô tô thật, mô hình nhìn thấy hình ô tô thì phải báo. |
| **R-12** | **Vật nhòe do chuyển động:** còn nhận ra lớp và đường bao thì gán và tick `can_review`; chỉ còn vệt mờ thì vẽ `ignore_region` lên vệt đó. |
| **R-13** | Một vật một box. Không gộp hai vật cùng lớp vào một box, không chia một vật thành hai box khi bị vật khác cắt ngang. |

(R-10 nằm ở mục "Vật không thuộc lớp nào".)

## 4. Ca khó

### Loại theo quy tắc

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_026 | Hai người trên một xe máy, nhìn ngang | R-02 | 2 box `person` + 1 box `motorcycle` (mức che `2`) | Thử lại trên `img_010` (hai người trên xe ga nhìn từ sau) và `img_006`: quy tắc vẫn cho đúng 3 box mỗi xe. |
| img_010 | Cô gái ngồi trên xe đang dựng; xe đạp bán hàng | R-02, R-10 | `person` + `motorcycle` riêng; xe đạp không gán; người bán gán `person` | Xe dựng hay xe chạy đều cùng một cách gán. |
| img_005 | Cận cảnh bốn, năm người đội mũ bảo hiểm, xe gần như khuất | R-02, R-05 | Mỗi người một `person` (nhiều box `truncated=yes`, mức che `2`–`3`); xe chỉ gán khi đủ nhận ra; xe bạc phía sau là `van` | Người là lớp không được bỏ sót. |
| img_002 | Xe chở xe | R-11 | 1 `truck` + mỗi ô tô trên giàn 1 `car` | Ô tô thật, kích thước đủ lớn. |
| img_004, img_016, img_035 | Tuk-tuk, xe lam | R-10, R-03 | `ignore_region` ôm xe; tài xế thấy trực tiếp gán `person` | Ngoài taxonomy nhưng dễ nhầm với `motorcycle` / `van`. |
| img_035 | Xe lam chất bao tải cao gấp đôi thân xe | R-09, R-10 | `ignore_region` chỉ bao thân xe, không bao chồng hàng | Hàng không phải xe. |
| img_029 | Hai người vác ống dài trên xe điện và xe đạp | R-09, R-10 | Xe điện: `motorcycle` + `person`; người đi xe đạp: `person`, xe đạp không gán; ống không nằm trong box nào | Box không nới theo hàng. |
| img_009, img_031, img_037, img_040 | Xe buýt, xe khách | R-10 | `ignore_region` | Từ 5 cửa sổ bên trở lên, ngoài taxonomy. |
| img_023 | Xích lô nhìn từ sau, có người đạp | R-10, R-03 | Người đạp gán `person`; xích lô không gán | Xe không động cơ. |
| img_021 | Hàng trăm xe máy chờ đèn đỏ | R-05, R-02 | Hàng đầu tách được gán riêng từng `person` và `motorcycle`; phía sau một `ignore_region` | Phía xa không tách được ranh từng vật. |
| img_030 | Bãi xe máy dày đặc | R-05 | Vài xe tiền cảnh thấy đủ hai mép gán riêng; còn lại `ignore_region`; người mặc áo xanh gán `person` | Như trên. |
| img_019, img_032 | Đám đông sau rào chắn; hàng người chờ xe buýt | R-05 | Người đứng tách rời gán riêng; dải người chồng nhau là một `ignore_region` | Tiêu chí "thấy cả hai mép thân". |
| img_017 | Tượng người cưỡi ngựa | R-06 | Không gán gì | Vật không thật. Ảnh vẫn phải có mặt trong COCO với 0 box. |
| img_027 | Bia mộ hình pickup bằng đá | R-06 | Không gán | Kích thước gần như xe thật, đây là ca dễ gán nhầm nhất. |
| img_033 | Ma-nơ-canh trong tủ kính, kính phản chiếu xe | R-06, R-07 | Không gán | Vừa vật giả vừa phản chiếu. |
| img_038 | Tủ kính bày xe mô hình | R-06 | Không gán (0 box) | Đồ chơi. |
| img_018 | Ảnh chân dung trên biển quảng cáo; ô tô sau hàng rào | R-06, R-01 | Người trên biển không gán; ô tô thật sau rào gán `car`, song sắt mảnh không tính là che | Song sắt che dưới 5%. |
| img_020 | Gương chiếu hậu: thấy thân xe mình và một xe phía sau | R-07, R-08 | Không gán (0 box) | Phản chiếu và xe chủ. |
| img_013, img_031 | Đường ướt ban đêm, bóng xe in dưới mặt đường | R-07 | Chỉ gán vật thật; bóng phản chiếu không nằm trong box | Box nới theo bóng sẽ hỏng IoU. |
| img_028 | Pickup cổ chở tượng ngựa | R-09, R-06 | `truck` bao thân xe; tượng ngựa không gán, không nới box; xe đỏ phía sau gán `car` | Hàng hóa và vật giả. |
| img_001, img_012, img_037 | Pickup các kiểu (thùng trần, thùng chở hàng, có nắp) | Định nghĩa lớp | `truck` | Thùng tách khỏi cabin. `img_012`: pickup tiền cảnh `truncated=yes`. |
| img_015 | Hai ô tô bị cắt mép ảnh; xe giữa ảnh nhòe do chạy | R-01, R-12 | Hai xe cắt mép: `car`, `truncated=yes`; xe nhòe: `car` + `can_review` nếu còn thấy đường bao | |
| img_014 | Hai người qua đường rõ nét, xe máy xung quanh nhòe thành vệt | R-12 | 2 `person`; các vệt xe máy là `ignore_region` | Không xác định được ranh từng xe. |
| img_025 | Người trên vỉa hè biển, càng xa càng nhỏ | R-04 | Chỉ gán người cao từ 20 px | Dùng thước đo của CVAT, không ước lượng bằng mắt. |
| img_040 | Người đội mũ bảo hiểm ở tiền cảnh, xe của họ chỉ lộ hai gương | R-02 | `person` (`truncated=yes`); không gán `motorcycle` | Phần thấy không đủ để nhận ra lớp. |
| img_022 | Mô tô có thùng bên, ảnh đen trắng | Định nghĩa lớp | 1 `motorcycle` bao cả thùng bên; người thấy trực tiếp gán `person` | Sidecar là một phần của xe. |

### Cần hỏi reviewer (chưa đủ căn cứ, gán theo phương án ghi dưới và tick `can_review`)

| Ảnh | Tình huống | Phương án tạm | Điều cần chốt |
|---|---|---|---|
| img_019 | Xe diễu hành hình xe hoạt hình màu vàng, có người lái thật và một hình nộm chuột | Xe: `car`; người lái: `person` (xe mui trần, R-03); hình nộm: không gán (R-06) | Xe tự chế chạy được có tính là `car` không? |
| img_024 | Nửa vỏ ô tô màu vàng đặt trên nóc ô tô đen trong nhà trưng bày | Xe đen: `car`; vỏ xe vàng: không gán (coi là hàng hóa, R-09) | Vỏ xe thật nhưng không hoàn chỉnh là xe hay là hàng? Xe trưng bày trong nhà có thuộc phạm vi "đường phố" không? |
| img_011 | Tượng nhân vật hóa trang và dãy mô tô trang trí ở hội chợ | Tượng: không gán (R-06); mô tô trang trí: `motorcycle` + `can_review` | Mô tô độ làm tác phẩm trưng bày là xe thật hay vật không thật? |
| img_010, img_029 | Xe điện hai bánh | `motorcycle` nếu không thấy bàn đạp | Xe đạp điện có bàn đạp xếp vào đâu? |
| img_003 | Người bán rong che gần hết người và xe phía sau | Gán từng `person` theo phần thấy, mức che theo ngưỡng | Ước lượng phần trăm che có đủ ổn định giữa hai người gán không? |

## 5. QC và phiên bản

- Ngưỡng áp dụng (theo `rules` trong `taxonomy.json`, không đổi): box cao tối thiểu 20 px; IoU đồng thuận 0,85; đồng thuận lớp 0,95; tỉ lệ ảnh lỗi tối đa 2%.
- Ca mơ hồ: người gán chọn phương án tốt nhất và tick `can_review`; người review bản cuối của nhóm quyết định, quyết định được ghi thành quy tắc có mã.
- Chưa vẽ được box (không biết có vật hay không): ghi ảnh, vùng, lý do để nhóm đưa vào `image_issues.csv`.
- Mọi thay đổi làm đổi nhãn đều tăng phiên bản guideline.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | |
| v0.1 (515) | Thêm ví dụ và phản ví dụ cho từng lớp; ngưỡng phần trăm cho `occluded_level`, bỏ nghĩa "không rõ" của mức 3; điều kiện cho `truncated` và `can_review`; quy tắc R-01 đến R-13; bảng ca khó | Người đi xe máy (`img_026`), xe chở xe (`img_002`), tuk-tuk (`img_004`), vật không thật (`img_017`, `img_027`, `img_033`, `img_038`), phản chiếu (`img_020`), đám đông (`img_021`, `img_030`) |
