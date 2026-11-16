# Guideline gán nhãn — v0.6 (cá nhân) — mã 113

- Phiên bản: v0.5 (bản cá nhân, v0.5 = rà lại từng ảnh trong 20 ảnh được giao cho 113; thêm lớp `tuktuk` và `rider`; viết từ `guideline_v0_starter.md`, chưa phải bản nhóm). v0.3 = gom quy tắc theo nhóm, thêm sơ đồ quyết định, sửa 3 chỗ mâu thuẫn, thêm ca khó phát hiện khi gán tay. **Mã R-xx giữ nguyên** để các ghi chú cũ vẫn tra được.
- Ngày: 2026-11-16
- Người viết: mã thành viên **113** (nhóm NhomBanDau). Chưa ai duyệt.
- Phạm vi khảo sát: cả 40 ảnh `data/images/`; ví dụ dẫn bằng mã ảnh `img_0xx`. Dấu (P) = ảnh thuộc lô pilot 12 ảnh cũ; upstream đã bỏ pilot, nay gán cả 40 ảnh nên dấu này chỉ còn là ghi chú.
- Phần gán của 113: 20 ảnh theo `submission/qc/assignments/113.txt` (xem `assignment.csv` của nhóm).
- Kế thừa cách viết của guideline BT2 v1.1 (`bt2_submit/guideline_v1.1.md`: ngưỡng số, thuộc tính đo được, quyết định từng ca). Khác BT2 ở chỗ lab này có lớp `person` và `ignore_region`, nên **người và xe máy tách box** (R-02), không gộp như BT2 C9.

## 1. Mục tiêu

Nhãn dùng huấn luyện mô hình **phát hiện vật 2D** (người và phương tiện) cho camera giao thông / xe tự lái. Hai kiểu sai nguy hiểm nhất:

- **Báo nhầm** vật không thật (tượng, đồ chơi, hình in, phản chiếu) thành người/xe → phanh nhầm, đếm sai lưu lượng.
- **Bỏ sót** người đi xe máy, người bị che một phần → rủi ro an toàn.

Quy tắc ưu tiên: *chỉ gán vật thật đang có mặt trong cảnh; đã gán thì ôm đúng phần nhìn thấy.*

## Tóm tắt một trang (đọc phần này trước)

**Thứ tự hỏi khi gặp một vật** — dừng ở câu đầu tiên có đáp án:

1. **Thật không?** Tượng, mô hình, đồ chơi, hình in, tranh tường, phản chiếu, bộ phận xe người chụp → **không gán** (R-04, R-10, R-17).
2. **Thấy đủ nhận ra lớp không?** Người: thấy đầu hoặc thân. Xe: thấy bánh + một phần thân/đèn. Không → **không gán** (R-03).
3. **Tách được và cao ≥ 20 px không?** Có → **vẽ box riêng**, kể cả vật nhỏ nằm trong đám đông (R-22). Không tách được → **một `ignore_region`** ôm phần còn lại (R-05).
4. **Thuộc lớp nào?** `car` / `truck` / `van` / `motorcycle` / `tuktuk` (xe 3 bánh có động cơ) / `person` / `rider` (mục 2). Xe ngoài taxonomy (xe đạp, xích lô, xe buýt) → **không box xe** (R-07).
5. **Người là `rider` hay `person`, có gán không?** Người **ngồi trên** xe máy, xe đạp, xích lô, sidecar hoặc chỗ hở của tuk-tuk → `rider`. Người còn lại (đi bộ, đứng, ngồi ghế, dắt xe, ngồi trên ô tô mui trần) → `person`. Người trong khoang **kín** (ô tô, van, buýt, cabin tải, nhìn qua kính) → **không gán** (R-23, R-25).
6. **Vẽ box:** ôm phần nhìn thấy (R-01), người và xe là hai box (R-02), người ôm tới bàn chân (R-21), hàng chất vượt thân xe không vào box (R-18).
7. **Thuộc tính:** `occluded_level` theo bảng %, `truncated=yes` khi box chạm mép (≤ 2 px), `can_review` khi phải đoán.

**Sáu luật vàng khi đang gán:** (1) vật thật mới gán; (2) vật ≥ 20 px nhận ra được thì phải có box; (3) một vật một box; (4) người và xe máy tách box; (5) ignore chỉ cho phần không tách được; (6) chưa chắc thì tick `can_review`, không tự bịa.

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con 4 bánh chở người (sedan, hatchback, SUV, taxi). | img_015 (hai xe ở mép ảnh), img_025 (sedan đen), img_040 (P, taxi) | img_012 (P) bán tải → `truck`; img_009 xe buýt mini → ngoài lớp (R-07) |
| `truck` | Xe có **thùng hàng riêng** phía sau cabin: xe tải, bán tải, xe tải nhỏ thùng hở/bạt. | img_002 (P, đầu kéo chở xe), img_012 (P, bán tải chở hàng, chụp từ phía sau), img_036 (xe tải nhỏ xanh mui bạt), img_037 (bán tải trắng có mui che), img_007 (bán tải Hilux và xe tải Isuzu), img_001 (bán tải thùng hở) | Xe thùng kín cỡ nhỏ → có thể là `van` (R-06) |
| `van` | Xe **thùng kín liền khối** cỡ nhỏ, không có thùng hàng tách khỏi cabin. | img_016 (van trắng giữa ảnh), img_005 (P, van trắng phía sau) | Xe có thùng hàng hở → `truck` |
| `motorcycle` | Xe hai bánh có động cơ (xe máy, xe ga, mô tô, kể cả thùng bên/thùng kéo gắn liền), **chỉ phần xe**, không gồm người ngồi. | img_005, img_006, img_008, img_026, img_030, img_022 (sidecar) | Xe ba bánh có động cơ → `tuktuk`; xe đạp, xích lô → ngoài lớp (R-07) |
| `tuktuk` | Xe **ba bánh có động cơ** chở khách hoặc hàng, thường có mái, thân hở hông: tuk-tuk Thái, auto-rickshaw Ấn, xe lam. Box ôm thân xe (mái, 3 bánh, cản), không gồm hàng vượt thân (R-18). | img_004 (2 xe xanh), img_016 (2 xe), img_035 (2 xe vàng), img_040 (xe vàng phía sau) | Xe máy có thùng bên → `motorcycle`; xích lô đạp chân → ngoài lớp; ô tô nhỏ thân kín → `car` |
| `person` | Người thật **không ngồi trên** xe 2/3 bánh: đi bộ, đứng, ngồi ghế/đất, bán hàng cạnh xe, dắt/đẩy xe, ngồi trên ô tô mui trần. | img_014, img_034, img_010 (người bán chuối), img_019 (tài xế xe mui trần) | Người ngồi trên xe máy/xe đạp/tuk-tuk → `rider`; tượng, ma-nơ-canh, hình in (R-04) |
| `rider` | Người **ngồi trên** phương tiện hở hai/ba bánh: người lái và người ngồi sau xe máy, người đạp xe đạp/xích lô, người ngồi sidecar, tài xế và khách ngồi chỗ hở của tuk-tuk; kể cả khi xe đang đỗ mà người còn ngồi trên yên. Box ôm phần người nhìn thấy, từ mũ tới bàn chân (R-21). | img_005 (3 người trên xe máy), img_026 (2 người 1 xe), img_006, img_029, img_023 (người đạp xích lô), img_004 (tài xế tuk-tuk) | Người dắt xe, đứng cạnh xe, vừa xuống xe → `person`; người trong ô tô/van/buýt → không gán (R-23) |
| `ignore_region` | Vùng không tách được từng vật hoặc ngoài phạm vi gán; bỏ sót ở đây không tính lỗi. | img_021 (rừng xe máy phía sau), img_030 (bãi xe), img_032 (đám đông xa) | Không dùng để "né" vật rõ ràng gán được |

**Vật không thuộc lớp nào** (xe đạp, xích lô, xe buýt, buýt mini…): **không vẽ box cho vật đó** (R-07). Người ngồi trên xe đạp/xích lô vẫn gán `rider`; người trong khoang kín thì không gán (R-23). Ghi vào `image_issues.csv` để nhóm quyết có thêm lớp không.

### Thuộc tính

**`occluded_level`** — tỉ lệ diện tích vật bị che, ước theo hình dạng đầy đủ của vật:

| Mức | Nghĩa | Ngưỡng |
|---|---|---|
| `0` | Thấy rõ | che < 5% |
| `1` | Che ít | 5% – 30% |
| `2` | Che nhiều | 30% – 70% |
| `3` | Gần như không thấy | > 70%, chỉ đoán được từ vài phần |

Phần bị cắt **mép ảnh** không tính là "che" (đã có `truncated`). Phân vân giữa hai mức thì chọn mức **cao hơn** và tick `can_review`.

**`truncated`** — `yes` khi vật bị cắt bởi mép ảnh (box chạm mép, thân thật còn kéo ra ngoài); `no` còn lại. Ví dụ `yes`: img_015 (hai xe ở hai mép), img_040 (P, người/taxi bị cắt mép).

**`can_review`** — tick khi: (a) không chắc lớp, (b) không chắc có nên gán không, (c) phân vân mức che, (d) quy tắc dưới đây chưa đủ.

## 3. Quy tắc vẽ box (gom theo nhóm, mã R-xx giữ nguyên)

### A. Gán hay không gán

| ID | Quy tắc |
|---|---|
| R-04 | **Không gán vật giả:** tượng, mô hình, đồ chơi, ma-nơ-canh, hình in/áp phích/tranh tường/biển quảng cáo, mascot, **phản chiếu** trong gương/kính/nước. Ví dụ: img_017 (tượng người cưỡi ngựa), img_027 (bia mộ hình xe tải), img_033 (ma-nơ-canh), img_038 (tủ xe đồ chơi), img_018 (người trên biển quảng cáo), img_020 (xe trong gương), img_026 (tàu trên tranh tường), img_019 (chuột bông), img_028 (tượng ngựa: không gán ngựa, xe tải cổ thật vẫn gán `truck`). |
| R-10 | **Xe chủ (ego):** gương chiếu hậu, nắp ca-pô, tay lái của xe người chụp không gán (img_020, mép dưới img_040). |
| R-17 | **Bóng phản chiếu / vật ngập nước** (img_015, img_031): chỉ vẽ phần nổi, không vẽ bóng (tính là R-04). |
| R-03 | **Vật bị che:** chỉ vẽ nếu còn thấy ≥ 30% **hoặc** nhận ra rõ lớp (xe thấy bánh + đầu xe; người thấy đầu + vai). Che nặng hơn, không nhận ra → không vẽ. |
| R-12 | **Chuyển động nhòe** (img_014): nhận ra hình dạng → vẫn gán, box ôm vùng nhòe thấy được; không đoán nổi lớp → `ignore_region` + `can_review`. |
| R-13 | **Thiếu sáng** (img_008, img_026, img_031): chỉ gán vật nhận ra bằng mắt thường, không đoán vật chìm trong tối. |
| R-20 | **Xe lễ hội / chế tạo riêng** cỡ thật, chạy được (img_019): gán `car` + `can_review`; nhân vật bông trên xe không gán; người lái gán `person`. |
| R-23 | **Người trong phương tiện:** khoang **hở** (xe máy, xe đạp, xích lô, tuk-tuk hở hông) → `rider` nếu thấy ≥ 30%; xe mui trần → `person`. Khoang **kín** (ô tô, van, buýt, cabin tải, nhìn qua kính) → **không gán**. Ví dụ không gán: khách trong xe buýt mini img_009; ví dụ gán: tài xế tuk-tuk img_004 (`rider`), người lái xe diễu hành img_019 (`person`). |
| R-25 | **`rider` hay `person`:** hỏi một câu — *người này đang ngồi trên xe 2 hoặc 3 bánh không?* Có → `rider`; không → `person`. Bảng ca biên bên dưới. **Phép thử đo được (v0.5):** nếu box người chồng lên box xe ≥ 35% diện tích người, tâm ngang nằm trong xe và chân/đáy người nằm trong khoảng dọc của xe → `rider`. Người cao, chỉ chạm xe một phần (đứng cạnh, dắt xe, bán hàng) → `person` (img_003). Khi xe bị che nên không có box xe (img_005, hành khách ngồi sau) thì nhìn tư thế: ngồi trên yên/đệm = `rider`. |

### B. Lớp nào

| ID | Quy tắc |
|---|---|
| R-06 | **`truck` / `van`:** thấy thùng hàng hở, thùng bạt, mui che/canopy hoặc thùng tách khỏi cabin → `truck` (img_036, img_037, img_012). Thân kín liền cabin → `van` (img_005, img_016). Chỉ thấy đầu xe, không phân được → chọn theo nóc (liền khối → `van`, ngược lại `truck`) + `can_review`. |
| R-07 | **Phương tiện ngoài taxonomy** (xe đạp, xích lô, xe buýt, buýt mini): **không vẽ box xe**; người ngồi trên xe đạp/xích lô gán `rider` (R-25). Ví dụ: img_023, 025, 029 (xe đạp, xích lô), img_009, 031, 037 (xe buýt). Tuk-tuk **không** nằm ở đây, đã có lớp `tuktuk` (R-24). |
| R-19 | **Xe máy có thùng bên / thùng kéo** (img_022, img_025): một `motorcycle` ôm cả xe + thùng gắn liền. |
| R-24 | **`tuktuk`:** một box ôm thân xe 3 bánh gồm mái, bánh, cản; không gồm hàng chất vượt thân (R-18, img_035) và không gồm người đứng ngoài xe. Tuk-tuk bị che nhiều vẫn vẽ nếu thấy ≥ 30% hoặc nhận ra mái + bánh (img_016, 040). Tài xế/khách ngồi chỗ hở là `rider` (box riêng, chồng lên box xe), khách trong khoang che kín không gán (R-23). |

### C. Vẽ box thế nào

| ID | Quy tắc |
|---|---|
| R-01 | **Ôm sát phần nhìn thấy:** cạnh box chạm điểm ngoài cùng của vật, sai số ≤ 2 px (vật cao > 50 px) hoặc ≤ 1 px (nhỏ hơn). Không bù phần khuất ở **rìa**; nhưng đoạn bị che nằm **giữa** hai phần thấy được vẫn nằm trong box (img_001: xe tải bị người đứng trước che một đoạn). **Cạnh dưới xe dừng ở điểm tiếp đất của bánh** (không tính chân chống, bóng đổ) (gộp R-14). |
| R-02 | **Người + xe máy = box riêng.** `motorcycle` ôm xe, `rider` ôm phần người nhìn thấy; hai box được chồng nhau; mỗi người ngồi trên xe một `rider`. Hai người một xe → 2 `rider` + 1 `motorcycle` (img_026, img_005). |
| R-21 | **Box người ôm tới bàn chân / đế giày** nếu thấy; không cắt ở thắt lưng hay đầu gối (img_006, img_014). Chân bị che hẳn thì dừng ở chỗ nhìn thấy. |
| R-15 | **Một vật một box:** không hai box đè lên cùng một vật; không gộp nhiều xe thành một box. Một xe bị YOLO chia thành 2 box → giữ **một** (img_012, img_026). |
| R-08 | **Xe chở xe / xe chở vật:** đầu kéo + khung chở = 1 `truck`; mỗi xe con thật trên khung gán riêng theo lớp của nó (img_002; img_024: xe vàng nhỏ trên mui `car` + `can_review`). Hàng, rau, tượng **không phải xe** thì không box riêng (img_012). |
| R-18 | **Hàng chất vượt ra ngoài thân xe không vào box** (bao tải img_035, tượng ngựa img_028, xe mô hình trên nóc); hàng nằm trong thùng thì nằm trong box thùng (R-08). *(Bản v0.2 ghi ngược lại; đổi để khớp quy ước chung, vì biên thân xe rõ nên hai người vẽ trùng nhau.)* |
| R-09 | **Vật dài nhô ra** (ống, thanh dài, quang gánh, img_029, img_003): box người/xe không kéo theo vật đó. |

### D. Vật nhỏ, đám đông, cắt mép

| ID | Quy tắc |
|---|---|
| R-22 | **Vẽ riêng trước, ignore sau:** vật cao ≥ 20 px và nhận ra lớp thì phải có box riêng, kể cả đứng trong cụm xa (img_013: 1 ô tô và 1 xe máy nhỏ được vẽ riêng thay vì cả vùng `ignore_region`). |
| R-05 | **`ignore_region`** chỉ cho phần **không tách được** (đám đông chồng nhau che > 40%, vật < 20 px, nhòe mạnh): khoanh **một** vùng ôm cả cụm (img_021, 030, 032, 019). Không dùng ignore thay cho vật rõ. Ignore không được phủ lên vật đã có box riêng, trừ khi vật đó nằm lọt trong cụm. |
| R-16 | **Soát nền sau/xa trước khi nộp:** vật ≥ 20 px, nhận ra lớp → có box, kể cả sau cột, sau người, kẹt giữa hai xe lớn (nguồn bất đồng lớn nhất ở BT2 C6). |
| R-11 | **Bị cắt mép ảnh:** vẽ phần trong ảnh, `truncated=yes`; phần còn lại < 20% vật hoặc < 20 px thì không vẽ. |

*Đã gộp:* R-14 → R-01 (cạnh dưới xe). R-17 giữ lại như một ví dụ riêng của R-04. ID mới của v0.3: R-21, R-22, R-23.

## 4. Ca khó

> Từ v0.4: mọi `person` **ngồi trên xe 2/3 bánh** trong các bảng dưới đọc là `rider`; tuk-tuk là lớp `tuktuk`, không còn là "ngoài lớp".

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_005 (P) | 3 người đội mũ bảo hiểm ngồi sát trên xe máy, xe van phía sau | R-02, R-03 | 3 `person`; `motorcycle` chỉ cho xe thấy ≥ 30%; xe phía sau `van` | Mỗi người một box, không gộp người + xe |
| img_002 (P) | Đầu kéo chở nhiều ô tô nhiều tầng | R-08 | 1 `truck` + mỗi `car` thấy ≥ 30% | Mô hình cần học cả xe chở lẫn xe được chở |
| img_004 (P) | Hai tuk-tuk ba bánh có tài xế | R-07 | Không box tuk-tuk; `person` tài xế nếu thấy ≥ 30% | Không có lớp tương ứng; tick `can_review` |
| img_006 (P) | Nhiều xe máy nhìn từ phía sau, người che xe | R-02, R-05 | Gán từng xe/người rõ; cụm xa thành `ignore_region` | Vật gần tách được, vật xa dính liền |
| img_008 (P) | Đêm, bãi xe máy dày + 2 tài xế áo cam | R-05, R-13 | Vật rõ vẽ box; hàng xe đậu sát phía sau thành `ignore_region` | Tránh vẽ dày đặc thiếu chính xác |
| img_012 (P) | Bán tải chở rau/thùng hàng, ô tô phía sau | R-06, R-08 | `truck` cho bán tải (không vẽ hàng); `car` cho xe sau | Có thùng hàng riêng → truck |
| img_017 (P) | Tượng người cưỡi ngựa, nón cone trên đầu | R-04 | Không box | Vật giả |
| img_020 (P) | Gương chiếu hậu có phản chiếu xe và đường | R-04, R-10 | Không box | Phản chiếu + bộ phận xe chủ |
| img_026 (P) | Đêm, 2 người trên xe máy trước tranh tường có tàu | R-02, R-04, R-13 | 2 `person` + 1 `motorcycle`; tranh tường không gán | Hình in không phải vật thật |
| img_027 (P) | Tượng xe tải đen trên bệ ở bãi cỏ | R-04 | Không box | Điêu khắc, không phải xe thật |
| img_033 (P) | Ma-nơ-canh, gương, ảnh | R-04 | Không box | Không phải người thật |
| img_040 (P) | Taxi, người đội mũ bảo hiểm lớn ở tiền cảnh, tuk-tuk phía sau | R-07, R-10, R-11 | `person` tiền cảnh `truncated=yes`; `car` taxi; bỏ tuk-tuk | Người bị cắt mép; tuk-tuk ngoài lớp |
| img_028 | Xe tải cổ thật chở tượng ngựa | R-04, R-08 | Gán `truck`; ngựa không gán | Tượng là vật giả |
| img_029 | Người chở thanh dài nhô ra | R-09 | Box không kéo theo vật dài | Tránh box phình, IoU thấp giữa hai người gán |
| img_024 | Xe nhỏ vàng trên mui xe đen trong bảo tàng | R-08 | `car` cho cả hai; xe vàng thêm `can_review` | Chưa rõ xe thật hay mô hình trưng bày |

### Phân biệt `rider` và `person` — ca biên (v0.4)

| Tình huống | Nhãn | Lý do / ví dụ |
|---|---|---|
| Người lái xe máy đang chạy | `rider` | img_006, 034 |
| Người ngồi sau, trẻ ngồi trước/giữa xe máy | `rider` | img_005, 026 |
| Người ngồi trên xe máy **đỗ** (tay còn trên tay lái, chân chạm đất) | `rider` | img_010, cô gái ngồi xe 29-C1 |
| Người đạp xe đạp / xích lô | `rider` | img_023, 029, 006 |
| Người ngồi trong sidecar | `rider` | img_022 |
| Tài xế tuk-tuk; khách ngồi chỗ hở, thấy ≥ 30% | `rider` | img_004, 016, 035 |
| Một chân đã trên yên, đang lên/xuống xe | `rider` | còn đang ngồi lên |
| Người **dắt/đẩy** xe, đứng cạnh xe, vừa xuống xe | `person` | img_003 (người dắt xe đạp) |
| Người bán hàng rong đứng cạnh xe đạp/xe máy | `person` | img_010 người bán chuối |
| Người ngồi trên ô tô mui trần | `person` | img_019 (xe 4 bánh, không phải xe 2/3 bánh) |
| Người ngồi trên thùng bán tải | `person` | không ngồi trên xe 2/3 bánh |
| Người trong ô tô, van, buýt, cabin tải | không gán | R-23 |
| Chỉ thấy người trên xe ở xa, vẫn ≥ 20 px | `rider` nếu nhận ra đang ngồi trên xe, ngược lại `person` + `can_review` | R-16 |

### Ca khó phát hiện thêm khi gán tay (v0.3)

| Ảnh | Tình huống | Rule | Quyết định | Lý do |
|---|---|---|---|---|
| img_019 | Xe diễu hành, tài xế khuất sau kính, đám đông dày sau rào, người cắt mép phải và góc dưới phải | R-20, R-23, R-05, R-11 | 1 `car` + `can_review`; tài xế `person` `occluded_level=2`; 2 người cắt mép `truncated=yes`; 4 người hàng đầu thấy rõ gán riêng; 2 `ignore_region` cho đám đông; chuột bông không gán | Đã gán tay từng box, lý do ghi ở `hand.json` |
| img_001 | Bán tải bị người đứng chắn giữa thân xe | R-01 | 1 box `truck` kéo từ mép trái thấy được tới mép phải | YOLO tách thành nhiều box; đoạn khuất nằm giữa hai phần thấy |
| img_006, img_014 | Box người YOLO dừng ở đầu gối/đùi | R-21 | Kéo box xuống tới bàn chân | Hai người cùng gán sẽ khớp IoU hơn |
| img_013 | Đêm, xe và xe máy nhỏ ở xa (cao ≥ 20 px) | R-22 | Vẽ riêng `car` và `motorcycle`, không phủ ignore | Vật rõ thì có box |
| img_011 | Xe trắng phía sau tượng, YOLO gọi `car` | R-06 | Đổi thành `truck` khi thấy thùng/dáng xe tải | Phân lớp theo thùng, không theo nhãn YOLO |
| img_035 | Xe ba bánh chở bao tải chất cao | R-07, R-18 | Bỏ xe ba bánh; hàng không vào box nào | Ngoài taxonomy; hàng vượt thân xe |
| img_009 | Khách trong xe buýt mini | R-23 | Không gán `person` | Khoang kín |
| img_012, img_026 | YOLO chia 1 xe thành 2–3 box | R-15 | Gộp thành 1 box | Một vật một box |
| img_003 | Người bán hàng rong và người dắt xe đứng giữa dãy xe máy đỗ | R-25 | `person` (không phải `rider`); xe đạp dắt không có lớp | Đứng cạnh xe, box người chỉ chạm xe < 35% |
| img_003 | Hai box cho một người (bản cũ ngắn + bản đã kéo tới chân) | R-15, R-21 | Giữ box dài tới bàn chân, xóa box ngắn | Một vật một box |
| img_005 | 4 người ngồi sát nhau, xe máy bị che gần hết | R-25, R-02 | Tất cả người ngồi trên yên là `rider`; xe máy chỉ vẽ khi thấy bánh/thân | Tư thế ngồi, không dựa box xe |
| img_028 | Xe tải cổ chở tượng ngựa | R-18, R-01 | Box ôm cả xe từ đuôi thùng tới cản trước, bỏ phần ngựa phía trên mui | YOLO cắt mất đầu xe |
| img_035 | Tài xế ngồi chỗ hở của tuk-tuk chất hàng | R-23, R-24 | `rider` riêng, chồng lên box `tuktuk` | Khoang hở |

### Bảng đọc từng ảnh (đã xem lại ở độ phân giải cao)

| Ảnh | Có gì | Gán | Không gán / lưu ý |
|---|---|---|---|
| 001 | Bán tải trắng thùng hở, người ngồi quán bia phía sau | `truck`; `person` thấy ≥ 30% (che, `occluded_level` 1–2) | Bàn ghế, hình trên bảng hiệu |
| 002 | Đầu kéo chở 8 ô tô, 2 tầng | 1 `truck`; từng `car` thấy ≥ 30% (tầng dưới che nhiều) | Người xa mép phải nếu < 20 px |
| 003 | Người bán rong gánh trái cây, người dắt xe đạp, xe máy phía sau | `person` (3–4 người rõ), `motorcycle` thấy ≥ 30% | Xe đạp (ngoài lớp); nền xe máy xa dính liền → `ignore_region` |
| 004 | Hai tuk-tuk xanh, tài xế ngồi trong | 2 `tuktuk`; `rider` tài xế nếu thấy ≥ 30% | Nón cone |
| 005 | 4 người đội mũ bảo hiểm ngồi sát trên xe máy, van trắng sau | `rider` từng người; `motorcycle` thấy ≥ 30%; `van` | Che nhiều giữa người với nhau → `occluded_level` 2 |
| 006 | Nhiều xe máy nhìn từ phía sau, 1 taxi trắng, xe đạp | Từng `motorcycle` + `person` rõ; `car` taxi (cắt mép trái, `truncated=yes`) | Xe đạp; hàng xa dính liền → `ignore_region` |
| 007 | Bán tải Hilux trắng + xe tải Isuzu trong gara tối | 2 `truck` | Rào chắn cam |
| 008 | Đêm, xe máy đỗ dày, 2 tài xế áo cam | Xe/người rõ phía trước | Dãy xe sau → `ignore_region` (R-05, R-13) |
| 009 | Xe buýt mini đang chạy, nhà dân | Không có vật thuộc lớp rõ | Xe buýt mini bỏ (R-07); xe máy xa dưới 20 px bỏ |
| 010 | Chợ: xe máy 2 người, người bán rau, 2 xe máy đỗ | `motorcycle` (3), `rider` (người ngồi trên xe, kể cả cô gái ngồi xe đỗ), `person` (người bán, người đứng) | Xe đẩy rau (ngoài lớp); hàng hóa |
| 011 | Tượng Predator + xe máy điêu khắc kim loại, hội chợ | Không gán tượng / xe điêu khắc (R-04) | Người xa dưới 20 px bỏ |
| 012 | Thùng bán tải đầy hàng (cắt mép), Mazda xám phía sau | `truck` (`truncated=yes`); `car` | Hàng trong thùng không box riêng (R-08) |
| 013 | Đêm, quán nhỏ, 2–3 người và xe rất xa | Chỉ vật ≥ 20 px, nhận ra được | Ảnh gần rỗng (R-13, R-16) |
| 014 | 2 người đi bộ rõ giữa xe máy nhòe | 2 `person` rõ | Nền nhòe: nhận ra thì gán, không thì `ignore_region` (R-12) |
| 015 | Xe đỏ (trái) và SUV bạc (phải) cắt mép, xe nền, mặt đường phản chiếu | 2 `car` `truncated=yes`; xe nền nếu nhận ra | Bóng phản chiếu trên mặt đường (R-17) |
| 016 | 2 tuk-tuk, Vespa xanh có tài xế, van trắng, người góc dưới phải cắt mép | 2 `tuktuk`; `motorcycle` + `rider` (Vespa); `van`; `person` góc phải `truncated=yes`; `rider` trong tuk-tuk nếu thấy ≥ 30% | |
| 017 | Tượng người cưỡi ngựa, nón cone trên đầu | Không gán | R-04 |
| 018 | Biển quảng cáo có chân dung, bãi xe sau hàng rào | `car` thấy ≥ 30% sau hàng rào (`occluded_level` 1–2) | Chân dung trên biển (R-04) |
| 019 | Xe vàng hình xe đua, người lái, chuột bông, đám đông sau rào | `car` + `can_review` (R-20); `person` lái | Chuột bông; đám đông → `ignore_region` |
| 020 | Gương chiếu hậu có phản chiếu | Không gán | R-04, R-10 |
| 021 | Rừng xe máy đông, hàng đầu rõ | `motorcycle` + `person` hàng 1–2 | Phía sau `ignore_region` (R-05) |
| 022 | Ảnh đen trắng, xe máy sidecar xa trên đường rừng | `motorcycle` (R-19) nếu ≥ 20 px | Người nhỏ có thể bỏ |
| 023 | Honda sedan đen, xích lô, xe máy xa | `car`; `rider` đạp xích lô; `rider` + `motorcycle` xa nếu ≥ 20 px | Xích lô (R-07) |
| 024 | Xe wagon đen, xe vàng nhỏ trên mui, nhiều xe cổ bảo tàng | `car` đen; `car` vàng + `can_review`; xe cổ phía sau nếu rõ | Biển Texaco |
| 025 | Đại lộ ven biển, người đi bộ xa, taxi/xe máy xa | Chỉ vật ≥ 20 px | Nhiều vật dưới ngưỡng, ảnh gần rỗng |
| 026 | Đêm, 2 người trên xe máy đỏ, tranh tường cảng | 2 `rider` + `motorcycle` | Tranh tường (R-04) |
| 027 | Bia mộ hình xe tải đá đen trên cỏ | Không gán | R-04 |
| 028 | Xe tải cổ thật chở ngựa tượng, xe đỏ phía sau | `truck`; `car` đỏ | Ngựa tượng (R-04) |
| 029 | Xe máy chở ống dài, người đạp xe đạp | 2 `rider` + `motorcycle` | Xe đạp (R-07); ống dài (R-09); người nhỏ xa bỏ |
| 030 | Bãi xe máy dày, người áo xanh | Vài `motorcycle` hàng trước; `person` áo xanh | Phần còn lại `ignore_region` (R-05) |
| 031 | Đêm mưa, SUV trắng, xe khác, xe buýt xa | `car` rõ | Xe buýt (R-07), phản chiếu mặt đường (R-17) |
| 032 | Đám đông xếp hàng chờ xe, sedan xanh cắt mép trái | `car` `truncated=yes` | Đám đông xa → `ignore_region`; nón cone không gán |
| 033 | Ma-nơ-canh, quần áo, gương xe tải | Không gán | R-04 |
| 034 | Người đi bộ băng ngang, sedan đen, xe máy, người lái xe cắt mép phải | `person` đi bộ, `car`, `motorcycle` + `person` rõ; xe bên phải `truncated=yes` | Xe xa dưới 20 px |
| 035 | 2 xe ba bánh vàng (1 chở hàng cồng kềnh), xe máy, ô tô trắng nhỏ | 2 `tuktuk` (không gồm bao tải); `motorcycle` + `rider`; `car` trắng | Hàng vượt thân xe (R-18) |
| 036 | Xe tải nhỏ xanh mui bạt đỗ sát lề, xe máy đỗ bên trái | `truck`; xe máy đỗ thấy rõ | Biển số bị làm mờ |
| 037 | Bán tải trắng có mui che, xe buýt xanh sau, người đi bộ | `truck` (R-06); `person` nếu ≥ 20 px | Xe buýt (R-07) |
| 038 | Tủ trưng bày đồ chơi, xe mô hình | Không gán | R-04 |
| 039 | Phố nhỏ, xe máy đỗ trái, nhiều xe máy/người xa | `motorcycle` đỗ trái; vật ≥ 20 px | Nhiều vật dưới ngưỡng (R-16) |
| 040 | Taxi xanh, người đội mũ bảo hiểm đen trên xe máy tiền cảnh (cắt mép), tuk-tuk vàng, SUV đen, xe buýt | `rider` (`truncated=yes`) + `motorcycle` nếu thấy bánh/thân (chỉ thấy gương → không gán); `car` taxi; `car` SUV; `tuktuk` vàng | Xe buýt (R-07) |

**Câu hỏi để nhóm chốt ở Pha 2:** (1) có thêm lớp `bus` / xe ba bánh / xe đạp không, hay giữ R-07 (xuất hiện ở img_003, 004, 009, 016, 023, 029, 031, 035, 037, 040); (2) `van` vs `truck` khi chỉ thấy đầu xe; (3) ngưỡng che 30% ở R-03 có hợp lý không.

> Lưu ý: bảng trên lập sau khi xem lại cả 40 ảnh ở độ phân giải cao. Số lượng box cụ thể chưa đếm; các ca ghi `can_review` cần xem lại trên CVAT trước khi chốt.

## 5. QC và phiên bản

- Ngưỡng QC theo `submission/taxonomy.json`: IoU ghép ≥ 0.5; IAA IoU ≥ 0.85, cùng lớp ≥ 0.95; lỗi theo ảnh ≤ 2%.
- Ca mơ hồ: tick `can_review`, ghi mã `R-xx`; ca chưa có box ghi vào `submission/qc/image_issues.csv` (cột `image,annotator,region,note`).
- Ca mơ hồ cấp guideline do 113 đề xuất, cả nhóm chốt ở Pha 2.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản giảng viên | — |
| v0.5 (113) | Rà từng ảnh trong 20 ảnh của 113 sau khi sinh nháp lại (tiling + conf 0.15): thêm phép thử đo được cho `rider`/`person` (≥ 35% chồng xe), 5 ca khó mới (img_003, 005, 028, 035) | img_003, 005, 028, 035 |
| v0.4 (113) | Thêm lớp `tuktuk` (xe 3 bánh có động cơ) và `rider` (người ngồi trên xe hở 2/3 bánh); `person` chỉ còn người không ngồi trên xe; thêm R-24, R-25, bảng ca biên rider/person; sửa R-02, R-07, R-23 và bảng đọc từng ảnh 004, 005, 010, 016, 023, 026, 029, 035, 040 | img_004, 005, 010, 016, 023, 026, 029, 035, 040, 019 |
| v0.3 (113) | Gom R-xx thành 4 nhóm A–D; thêm tóm tắt một trang + thứ tự quyết định; thêm R-21 (người tới bàn chân), R-22 (vẽ riêng trước ignore), R-23 (người trong khoang kín/hở); sửa R-18 (hàng vượt thân xe không vào box); làm rõ R-01 (đoạn khuất giữa thân vẫn trong box); thêm 8 ca khó từ khi gán tay | img_019 (gán tay), 001, 006, 014, 013, 011, 035, 009, 012, 026 |
| v0.2 (113) | Thêm R-01…R-20, ngưỡng `occluded_level`, quy tắc vật giả/phản chiếu, người + xe máy box riêng, xe chở xe, phương tiện ngoài lớp, sidecar, xe lễ hội; R-14…R-18 kế thừa từ BT2 v1.1; thêm bảng đọc từng ảnh cho cả 40 ảnh | Đã xem lại cả 40 ảnh; ca khó chính: img_002, 004, 005, 006, 008, 012, 017, 019, 020, 022, 024, 026, 027, 033, 040 |

## 6. Đối chiếu với guideline nhóm v1.0 (`guideline_v1.0_agreed.md`)

Từ v0.6 bản cá nhân này **chỉ còn là tài liệu Pha 1**; việc gán nhãn thật dùng taxonomy và quy tắc chung của nhóm. Bảng ánh xạ:

| Bản cá nhân (v0.5) | Nhóm v1.0 | Ghi chú |
|---|---|---|
| `rider` | `person` + `person_state=on_vehicle` | Cùng một lớp để mô hình chỉ phát hiện `person`; trạng thái dùng để lọc/đo riêng |
| `person` | `person` + `person_state=off_vehicle` | Đi bộ, đứng, ngồi quán, dắt xe, đứng cạnh xe |
| `tuktuk` | `tuk_tuk` | Chỉ đổi tên |
| xe buýt: bỏ (R-07) | lớp `bus` (≥ 5 cửa sổ bên) | Đã thêm box `bus` từ YOLO (img_037) |
| xe đạp, xích lô: bỏ | bỏ (R-11), người ngồi trên vẫn là `person` | Giống nhau |
| hàng nhô ra: nới box (v0.2) → không nới (v0.3) | không nới (R-09) | Giống v0.3 |
| vật bị che: vẽ nếu thấy ≥ 30% | vẽ khi nhận ra lớp (R-12) | Bỏ ngưỡng 30%; người thấy đầu + vai, xe thấy ≥ 1 bánh + phần thân |
| box < 20 px: ignore | không gán (R-04), không vẽ box | Đo bằng CVAT |
| R-02 (người + xe máy tách box) | R-02 | Giống nhau |
| R-21 (box người tới bàn chân) | không có | Giữ như quy ước cá nhân, không mâu thuẫn |
| R-25 (phép thử ≥ 35% chồng xe) | `person_state` theo "xe đỡ cơ thể" | Dùng làm gợi ý tự động, người duyệt quyết cuối |

Dữ liệu gán của 113 (20 ảnh theo `assignments/113.txt`) đã chuyển theo bảng trên bằng `lab07_to_v1.py`; `can_review` còn bật ở mọi box nháp và ở các ca ghi trong mục 4.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0.6 (113) | Thêm mục 6 đối chiếu v1.0 nhóm; dữ liệu 20 ảnh chuyển sang taxonomy nhóm | Nhóm chốt v1.0 (anh Việt merge), `rider` → `person_state` |
