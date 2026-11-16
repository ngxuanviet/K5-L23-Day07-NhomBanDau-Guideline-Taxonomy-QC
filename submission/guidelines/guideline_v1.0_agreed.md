# Guideline gán nhãn — v1.0 (bản thống nhất của nhóm)

- Phiên bản: v1.0, **khóa cho lượt gán độc lập Pha 3**
- Ngày: 2026-11-16
- Nguồn: hợp nhất `individual/guideline_113.md` (v0.2) và `individual/guideline_515.md` (v0.1)
- Người chốt: 113, 515 (họp Pha 2)
- Loại nhãn: bounding box trên ảnh 2D, CVAT, xuất COCO 1.0
- Taxonomy đi kèm: `submission/taxonomy.json` phiên bản `v1.0` (8 lớp, 4 thuộc tính, mục `rules` giữ nguyên)

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện vật 2D**: người và phương tiện cơ giới **thật, đang có mặt trong cảnh**, cho camera giao thông hoặc xe tự lái.

Hai kiểu sai nguy hiểm nhất:

- **Bỏ sót người thật** (người đi bộ, người ngồi trên xe máy, người bị che một phần): rủi ro an toàn.
- **Báo nhầm vật không thật** (tượng, ma-nơ-canh, hình in, phản chiếu, đồ chơi) thành người hoặc xe: phanh nhầm, đếm sai lưu lượng.

Nguyên tắc ưu tiên: *chỉ gán vật thật; đã gán thì ôm đúng phần nhìn thấy.*
Phép thử khi phân vân lớp hay thuộc tính: *"Mô hình có phải đoán ra điều này khi suy luận không?"* Có thì là lớp; chỉ dùng để lọc mẫu khó hoặc QC thì là thuộc tính.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô chở người thân liền, có mũi xe, tối đa 3 hàng ghế: sedan, hatchback, SUV, taxi. | Mazda bạc `img_012`; sedan đen `img_023`; taxi `img_040`; hai xe cắt mép `img_015` | Bán tải → `truck`; xe một khối → `van`; xe mô hình `img_038` → không gán |
| `truck` | Xe có **thùng hoặc sàn chở hàng tách khỏi cabin**: xe tải, bán tải (kể cả có nắp thùng hoặc mui bạt), đầu kéo kèm rơ-moóc. | `img_001`, `img_007` (2 xe), `img_002`, `img_012`, `img_028`, `img_036`, `img_037` | Tượng pickup đá `img_027` → không gán; thân kín liền cabin → `van` |
| `van` | Xe **một khối**, không có mũi xe rõ, khoang sau liền cabin, **tối đa 4 cửa sổ bên mỗi phía**. | Xe bạc `img_005`; van trắng `img_016` | Từ 5 cửa sổ bên trở lên → `bus` |
| `bus` | Xe chở khách có **từ 5 cửa sổ bên mỗi phía trở lên** hoặc cửa lên xuống kiểu xe khách; gồm cả xe buýt mini. | `img_009`, `img_031`, `img_037`, `img_040` | Van chở khách nhỏ → `van` |
| `tuk_tuk` | Xe **ba bánh có động cơ**, có mui hoặc khoang chở khách/hàng: tuk-tuk, xe lam. | `img_004` (2 xe), `img_016`, `img_035`, `img_040` | Xích lô (không động cơ) → không gán; mô tô có thùng bên → `motorcycle` |
| `motorcycle` | Xe hai bánh gắn máy hoặc chạy điện **không có bàn đạp**, **chỉ phần xe**; mô tô có thùng bên (sidecar) vẫn là một `motorcycle`. | `img_010`, `img_026`, `img_029` (xe điện), `img_022` (sidecar) | Xe đạp, xe đạp điện có bàn đạp → không gán |
| `person` | Người thật nhìn thấy trực tiếp: đi bộ, đứng, ngồi, ngồi trên xe hở. | `img_014`, `img_034`, `img_026` | Tượng `img_017`; ma-nơ-canh `img_033`; ảnh người trên biển `img_018`; người sau kính ô tô |
| `ignore_region` | Vùng không tách được từng vật; bỏ sót ở đây không tính lỗi. Không phải một loại vật. | Xe máy phía xa `img_021`; bãi xe `img_030`; đám đông `img_019`, `img_032` | Không dùng để né một vật tách được rõ ràng |

### Thuộc tính

**`occluded_level`** — phần diện tích bị **vật khác** che, ước theo hình dạng đầy đủ của vật. Bị cắt bởi mép ảnh không tính là che.

| Mức | Ngưỡng |
|---|---|
| `0` | che dưới 5% |
| `1` | che từ 5% đến dưới 30% |
| `2` | che từ 30% đến 70% |
| `3` | che trên 70% nhưng vẫn nhận ra lớp (xem R-12) |

Phân vân giữa hai mức: chọn mức **cao hơn** và tick `can_review`.

**`truncated`** — `yes` khi box chạm mép ảnh **và** vật rõ ràng còn tiếp tục ngoài khung; còn lại `no`.

**`can_review`** — tick khi không chắc lớp, không chắc vật có thật không, phân vân mức che, hoặc quy tắc chưa đủ. Vẫn phải vẽ box và chọn lớp theo phán đoán tốt nhất; tick không thay cho quyết định.

**`person_state`** — chỉ có nghĩa với lớp `person`: người đó đang ở trên phương tiện hay không.

| Giá trị | Khi nào | Ví dụ |
|---|---|---|
| `on_vehicle` | Người đang **ngồi hoặc đứng trên phương tiện**, cơ thể được xe đỡ: trên yên xe máy, xe đạp, xích lô; trong tuk-tuk, xe mui trần, thùng xe hở. Xe đang chạy, dừng đèn đỏ hay dựng tại chỗ đều tính, kể cả khi người đó chống chân xuống đất. | Hai người trên xe máy `img_026`; cô gái ngồi trên xe dựng `img_010`; người đạp xích lô `img_023`; tài xế tuk-tuk `img_004`; người lái xe diễu hành `img_019` |
| `off_vehicle` | Mọi người còn lại: đi bộ, đứng, ngồi ghế hoặc ngồi quán, **dắt xe**, đứng cạnh xe. | Người qua đường `img_014`, `img_034`; khách ngồi quán `img_001`; người dắt xe đạp và người bán rong `img_003`; người bán hàng `img_010` |
| `na` | Giá trị mặc định, dùng cho **mọi lớp không phải `person`**. | Mọi box `car`, `truck`, `van`, `bus`, `tuk_tuk`, `motorcycle` |

Mọi box `person` **bắt buộc** đổi sang `on_vehicle` hoặc `off_vehicle`; để `na` là lỗi. Tiêu chí phân định duy nhất: *cơ thể có đang được phương tiện đỡ không*. Không thấy phần dưới cơ thể nên không biết: chọn theo ngữ cảnh gần nhất (tư thế tay cầm lái, mũ bảo hiểm giữa dòng xe) và tick `can_review`.

Lý do là thuộc tính, không tách lớp: mô hình vẫn chỉ cần phát hiện `person`; thông tin này dùng để lọc mẫu, đo riêng độ đồng thuận trên người đi xe (nhóm bị che nhiều nhất) và soát R-02.

CVAT hiển thị cả bốn thuộc tính trên mọi lớp vật. `ignore_region` không có thuộc tính.

## 3. Quy tắc vẽ box

| Mã | Quy tắc |
|---|---|
| **R-01** | **Ôm sát phần nhìn thấy.** Cạnh box chạm điểm ngoài cùng của phần thấy được; lệch tối đa 2 px khi vật cao trên 50 px, 1 px khi nhỏ hơn. Không đoán phần bị che hay phần ngoài khung. |
| **R-02** | **Người đi xe máy: tách box.** Mỗi người một `person` (bao cả phần đang ngồi trên xe, `person_state=on_vehicle`); chiếc xe một `motorcycle` chỉ bao phần xe nhìn thấy. Hai box được chồng nhau. Xe dựng hay xe đang chạy gán cùng một cách. |
| **R-03** | **Người trên xe.** Gán `person` khi thấy trực tiếp: trên xe máy, tuk-tuk, xích lô, xe mui trần, thùng xe hở; các box này mang `person_state=on_vehicle`. Người trong cabin kín chỉ thấy **qua kính**: không gán. |
| **R-04** | **Vật nhỏ.** Box cao dưới **20 px** trên ảnh gốc thì không gán (`rules.min_box_height_px`). Đo bằng CVAT, không ước lượng bằng mắt. |
| **R-05** | **Đám đông, bãi xe.** Một vật được gán riêng khi cao từ 20 px **và** thấy được cả mép trái lẫn mép phải của nó. Phần còn lại, nơi các vật dính liền không tách được, gom vào **một** `ignore_region` ôm sát cụm đó. Không vẽ nửa vời vài vật trong cụm. |
| **R-06** | **Vật không thật: không gán**, cũng không vẽ `ignore_region`. Gồm tượng, ma-nơ-canh, hình in, biển quảng cáo, tranh tường, đồ chơi, mô hình, hình nộm, tác phẩm điêu khắc hình xe. Người thật mặc đồ hóa trang vẫn là `person`. |
| **R-07** | **Phản chiếu: không gán.** Hình trong gương, kính, vũng nước, mặt đường ướt. Box vật thật không nới theo bóng phản chiếu của nó. |
| **R-08** | **Xe chủ (ego): không gán.** Gương, nắp ca-pô, cửa, tay lái của chính xe đang chụp. |
| **R-09** | **Hàng hóa và đồ mang theo.** Box xe bao **thân xe**; hàng nằm gọn trong thùng thì nằm trong box, không có box riêng. Hàng nhô ra ngoài thân xe (ống dài, bao tải chất cao hơn nóc) **không làm nới box**. Box người bao cơ thể cùng thứ đội hoặc đeo sát người (mũ, ba lô); không bao đồ cầm tay, quang gánh. |
| **R-10** | **Xe chở xe.** Xe chở một box theo lớp của nó (đầu kéo: `truck` bao cả rơ-moóc). **Mỗi xe thật được chở một box riêng** theo lớp, kèm `occluded_level`, nếu đạt R-04 và R-12. Hai box chồng nhau là bình thường. |
| **R-11** | **Vật ngoài taxonomy.** Xe đạp, xe đạp điện có bàn đạp, xích lô, xe đẩy, quang gánh: **không gán**; người ngồi trên vẫn là `person` (R-03). Xe cơ giới khác chưa có lớp: không gán, ghi vào `image_issues.csv`. |
| **R-12** | **Vật bị che.** Vẽ khi **nhận ra được lớp**: người thấy đầu và vai; xe thấy ít nhất một bánh cùng một phần thân. Không nhận ra thì không vẽ. Ghi `occluded_level` theo bảng. |
| **R-13** | **Vật bị cắt mép ảnh.** Vẽ phần trong ảnh, `truncated=yes`. Phần trong ảnh không đạt tiêu chí nhận ra lớp ở R-12 hoặc cao dưới 20 px thì không vẽ. |
| **R-14** | **Vật nhòe do chuyển động.** Còn nhận ra lớp và đường bao: gán, box ôm vùng nhòe thấy được, tick `can_review`. Chỉ còn vệt mờ: vẽ `ignore_region` lên vệt đó. |
| **R-15** | **Ban đêm, thiếu sáng.** Chỉ gán vật nhận ra bằng mắt thường ở độ sáng gốc; không đoán vật chìm trong tối. |
| **R-16** | **Một vật một box.** Không gộp nhiều vật vào một box; không chia một vật thành hai box khi bị vật khác cắt ngang. Ngoại lệ duy nhất là `ignore_region` ở R-05 và R-14. |
| **R-17** | **Cạnh dưới box phương tiện** dừng ở điểm bánh xe chạm đất; không bao bóng đổ và chân chống. |
| **R-18** | **Phân `car` / `truck` / `van` / `bus`.** Thùng tách khỏi cabin → `truck`. Một khối, tối đa 4 cửa sổ bên → `van`. Từ 5 cửa sổ bên → `bus`. Có mũi xe, chở người → `car`. Chỉ thấy đầu xe: nóc liền khối kéo ra sau → `van`, ngược lại `truck`, và tick `can_review`. |
| **R-19** | **Mô tô có thùng bên:** một `motorcycle` bao cả xe và thùng bên; người gán `person` nếu đạt R-04. |
| **R-20** | **Xe tự chế, xe diễu hành** đang chạy thật trên đường và có người lái: gán theo lớp gần nhất, tick `can_review`. |
| **R-21** | **Soát nền trước khi export.** Vật cao từ 20 px và nhận ra lớp phải có box, kể cả nằm sau cột, kẹt giữa hai xe lớn. Ảnh không có vật nào vẫn phải có mặt trong COCO với 0 box. |

## 4. Ca khó

### Bất đồng giữa hai bản cá nhân và cách nhóm chốt

| # | Vấn đề | Bản 113 | Bản 515 | Nhóm chốt | Lý do |
|---|---|---|---|---|---|
| 1 | Xe buýt, tuk-tuk | Không vẽ box | `ignore_region` ôm xe | **Thêm lớp `bus` và `tuk_tuk`** | Cả hai bản đều đề nghị bàn việc thêm lớp. Mô hình phải phân biệt chúng với `truck`, `van`, `motorcycle`; chúng có ở khoảng 8 trong 40 ảnh. Bỏ làm nền thì dạy sai mô hình, còn `ignore_region` thì phí dữ liệu. |
| 2 | Ngưỡng tối thiểu để vẽ vật bị che | Thấy từ 30% trở lên hoặc nhận ra lớp | Nhận ra lớp | **Nhận ra lớp, có tiêu chí cụ thể (R-12)** | Ngưỡng "thấy từ 30%" mâu thuẫn với `occluded_level=3` (che trên 70%). |
| 3 | Hàng nhô ra khỏi xe | Box nới ra bao hàng gắn liền xe | Box không nới | **Không nới (R-09)** | Mép thân xe xác định được, mép đống hàng thì mỗi người vẽ một kiểu; IoU yêu cầu 0,85. |
| 4 | Vỏ xe vàng trên nóc xe đen `img_024` | `car` + `can_review` | Không gán | **`car` + `can_review`** | Nhất quán với R-10: vật có hình ô tô thật, cỡ thật. |
| 5 | Mô tô trang trí ở hội chợ `img_011` | Không gán (điêu khắc) | `motorcycle` + `can_review` | **Không gán (R-06)** | 113 đã xem ở độ phân giải cao: là tác phẩm điêu khắc kim loại. Ghi vào `image_issues.csv`. |
| 6 | Xe của người đội mũ đen `img_040`, chỉ lộ gương | `motorcycle`, `truncated=yes` | Không gán | **Không gán** | Không đạt R-12 (không thấy bánh hay thân xe). |
| 7 | Người sau kính ô tô | Không nói tới | Không gán | **Không gán (R-03)** | Nhìn qua kính, phản chiếu và độ tối làm hai người gán khó nhất quán. |
| 8 | Sai số mép box | 2 px khi cao trên 50 px, 1 px khi nhỏ hơn | Khoảng 2 px | **Theo 113 (R-01)** | Khớp ngưỡng `large_px = 50` của taxonomy. |
| 9 | Phân vân mức che | Chọn mức cao hơn + `can_review` | Không nói tới | **Theo 113** | Cho một cách xử lý duy nhất. |

### Bảng ca khó theo ảnh

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_026 | Hai người trên một xe máy, ban đêm, trước tranh tường | R-02, R-06, R-15 | 2 `person` (`on_vehicle`) + 1 `motorcycle` (mức che `2`); tranh tường không gán | Ảnh chuẩn để cả nhóm thử quy tắc người đi xe máy. |
| img_010 | Hai người trên xe ga; cô gái ngồi trên xe dựng; xe đạp bán hàng | R-02, R-11 | Mỗi người `person`, mỗi xe `motorcycle`; xe đạp không gán. Hai người trên xe ga và cô gái ngồi trên xe dựng: `on_vehicle`; người bán hàng: `off_vehicle` | Xe dựng gán như xe chạy; ngồi trên yên là `on_vehicle`. |
| img_005 | Cận cảnh nhiều người đội mũ bảo hiểm, xe gần như khuất | R-02, R-12, R-13 | Mỗi người một `person`; `motorcycle` chỉ khi thấy bánh và thân; xe phía sau `van` | Người là lớp không được bỏ sót. |
| img_002 | Xe đầu kéo chở ô tô hai tầng | R-10 | 1 `truck` + mỗi ô tô một `car` kèm mức che | Xe thật, đủ lớn. |
| img_024 | Vỏ xe vàng trên nóc xe đen, nhà trưng bày | R-10 | `car` cho xe đen; `car` + `can_review` cho xe vàng; xe cổ phía sau gán nếu đạt R-12 | Xem bất đồng số 4. |
| img_004, img_016, img_040 | Tuk-tuk có tài xế | Lớp `tuk_tuk`, R-03 | `tuk_tuk` cho xe; tài xế thấy trực tiếp gán `person` | Lớp mới ở v1.0. |
| img_035 | Xe lam chất bao tải cao gấp đôi thân xe | R-09 | `tuk_tuk` chỉ bao thân xe, không bao chồng hàng | Hàng không phải xe. |
| img_009, img_031, img_037 | Xe buýt, xe buýt mini | Lớp `bus`, R-18 | `bus` | Từ 5 cửa sổ bên. |
| img_037 | Bán tải có nắp thùng cao | R-18 | `truck` | Thùng vẫn tách khỏi cabin. |
| img_029 | Xe điện và xe đạp cùng vác một ống dài | R-09, R-11 | Xe điện: `motorcycle` + `person`; người đi xe đạp: `person`; ống không nằm trong box nào | Box không nới theo hàng. |
| img_023 | Xích lô nhìn từ sau | R-11, R-03 | Người đạp `person` (`on_vehicle`); xích lô không gán | Không có động cơ, nhưng người vẫn đang ở trên phương tiện. |
| img_021, img_030 | Biển xe máy chờ đèn đỏ; bãi xe dày đặc | R-05 | Vật thấy đủ hai mép gán riêng; còn lại một `ignore_region` | Tiêu chí tách vật đo được. |
| img_019 | Xe diễu hành vàng, người lái, hình nộm chuột, đám đông sau rào | R-20, R-03, R-06, R-05 | `car` + `can_review`; người lái `person`; hình nộm không gán; đám đông `ignore_region` | |
| img_032 | Hàng người chờ xe buýt | R-05, R-13 | Người đứng tách rời gán riêng; dải người dính liền `ignore_region`; ô tô xanh `car`, `truncated=yes` | |
| img_017, img_027, img_033, img_038 | Tượng cưỡi ngựa; bia mộ hình pickup; ma-nơ-canh; tủ xe đồ chơi | R-06, R-07 | 0 box | Vật không thật. Ảnh vẫn có trong COCO. |
| img_011 | Tượng nhân vật và mô tô điêu khắc | R-06, R-04 | Không gán tượng và mô tô điêu khắc; người thật cao từ 20 px gán `person` | Xem bất đồng số 5. |
| img_018 | Chân dung trên biển quảng cáo; ô tô sau hàng rào | R-06, R-12 | Người trên biển không gán; ô tô thật gán `car`, song rào mảnh tính mức che `0`–`1` | |
| img_020 | Gương chiếu hậu của xe đang chụp | R-07, R-08 | 0 box | Phản chiếu và xe chủ. |
| img_013, img_015, img_031 | Mặt đường ướt in bóng xe | R-07 | Chỉ gán vật thật; box không nới theo bóng | |
| img_015 | Hai ô tô cắt mép; một xe nhòe ở giữa | R-13, R-14 | Hai xe mép: `car`, `truncated=yes`; xe nhòe: `car` + `can_review` | |
| img_014 | Hai người qua đường rõ, xe máy xung quanh nhòe | R-14 | 2 `person` (`off_vehicle`); vệt nhòe không nhận ra lớp là `ignore_region` | |
| img_028 | Pickup cổ chở tượng ngựa | R-09, R-06 | `truck` bao thân xe; tượng ngựa không gán; xe đỏ phía sau `car` | |
| img_012 | Thùng pickup đầy hàng ở tiền cảnh | R-09, R-13 | `truck`, `truncated=yes`, hàng không có box riêng; xe bạc `car` | |
| img_040 | Người đội mũ đen ở tiền cảnh, xe chỉ lộ gương | R-12, R-13 | `person`, `truncated=yes`, `on_vehicle` + `can_review` (không thấy xe, suy từ mũ và gương); không gán `motorcycle`; taxi và SUV `car`; `tuk_tuk`; `bus` | Xem bất đồng số 6. |
| img_022 | Mô tô có thùng bên, ảnh đen trắng | R-19 | 1 `motorcycle` bao cả thùng bên | |
| img_025, img_039 | Phố rộng, nhiều vật ở xa | R-04, R-21 | Chỉ gán vật cao từ 20 px | Đo bằng CVAT. |

| img_003 | Người dắt xe đạp, người bán rong gánh hàng | `person_state`, R-09 | `person` (`off_vehicle`); xe đạp và quang gánh không gán | Dắt xe là đang đi bộ. |
| img_008 | Tài xế xe ôm áo cam giữa bãi xe đêm | `person_state`, R-02 | Ngồi trên yên: `on_vehicle`; đứng cạnh xe: `off_vehicle` | Tiêu chí "cơ thể được xe đỡ". |

### Ca chưa chốt (gán theo phương án ghi ở trên, tick `can_review`, đưa ra calibration nếu lệch)

- `img_024`: vỏ xe không hoàn chỉnh có là `car` không.
- `img_019`: xe tự chế có là `car` không.
- Xe hai bánh chạy điện không rõ có bàn đạp hay không: mặc định `motorcycle` + `can_review`.
- `img_003`: ước lượng phần trăm che khi người bán rong che người và xe phía sau.

## 5. QC và phiên bản

- Ngưỡng theo mục `rules` của `submission/taxonomy.json` (không đổi): box cao tối thiểu 20 px; ghép cặp box ở IoU 0,5; IAA yêu cầu IoU 0,85 và cùng lớp 0,95; tỉ lệ ảnh lỗi tối đa 2%.
- Trong Pha 3 mỗi người gán **độc lập**, không hỏi nhau. Ca lưỡng lự: tick `can_review`. Chưa vẽ được box: ghi ảnh, vùng, lý do, sau khi khóa nhãn nhóm thu vào `submission/qc/image_issues.csv` (cột `image,annotator,region,note`).
- Quyết định calibration ở Pha 5 dẫn mã `R-xx` của bản này. Quy tắc mới hoặc đổi nghĩa thì ghi vào `guideline_v1.1_calibrated.md`.
- Mọi thay đổi làm đổi nhãn đều tăng phiên bản guideline.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên: 6 lớp, 3 câu quy tắc, chưa có ca khó | |
| v1.0 | Thêm lớp `bus`, `tuk_tuk`; định nghĩa lớp kèm ví dụ và phản ví dụ; ngưỡng phần trăm cho `occluded_level` (mức 3 không còn nghĩa "không rõ"); điều kiện cho `truncated`, `can_review`; thêm thuộc tính `person_state` (`on_vehicle` / `off_vehicle` / `na`) để tách người trên xe với người đi bộ; quy tắc R-01 đến R-21; chốt 9 bất đồng giữa bản 113 và 515; bảng ca khó theo ảnh | Người đi xe máy `img_026`; xe chở xe `img_002`; tuk-tuk `img_004`, `img_016`, `img_035`; xe buýt `img_009`, `img_037`; vật không thật `img_017`, `img_027`, `img_033`, `img_038`; phản chiếu `img_020`; đám đông `img_021`, `img_030` |
