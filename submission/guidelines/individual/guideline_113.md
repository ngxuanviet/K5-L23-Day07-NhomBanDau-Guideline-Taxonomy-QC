# Guideline gán nhãn — v0.2 (cá nhân) — mã 113

- Phiên bản: v0.2 (bản cá nhân, viết từ `guideline_v0_starter.md`, chưa phải bản nhóm)
- Ngày: 2026-11-16
- Người viết: mã thành viên **113** (nhóm NhomBanDau). Chưa ai duyệt.
- Phạm vi khảo sát: cả 40 ảnh `data/images/`; ví dụ dẫn bằng mã ảnh `img_0xx`. Dấu (P) = ảnh thuộc lô pilot 12 ảnh cũ; upstream đã bỏ pilot, nay gán cả 40 ảnh nên dấu này chỉ còn là ghi chú.
- Phần gán của 113: theo `submission/qc/assignment.csv` chung của nhóm (nhóm trưởng chạy `split_assign.py` với danh sách mã thật).
- Kế thừa cách viết của guideline BT2 v1.1 (`bt2_submit/guideline_v1.1.md`: ngưỡng số, thuộc tính đo được, quyết định từng ca). Khác BT2 ở chỗ lab này có lớp `person` và `ignore_region`, nên **người và xe máy tách box** (R-02), không gộp như BT2 C9.

## 1. Mục tiêu

Nhãn dùng huấn luyện mô hình **phát hiện vật 2D** (người và phương tiện) cho camera giao thông / xe tự lái. Hai kiểu sai nguy hiểm nhất:

- **Báo nhầm** vật không thật (tượng, đồ chơi, hình in, phản chiếu) thành người/xe → phanh nhầm, đếm sai lưu lượng.
- **Bỏ sót** người đi xe máy, người bị che một phần → rủi ro an toàn.

Quy tắc ưu tiên: *chỉ gán vật thật đang có mặt trong cảnh; đã gán thì ôm đúng phần nhìn thấy.*

## 2. Lớp và thuộc tính

### Lớp (mỗi vật thuộc đúng một lớp)

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con 4 bánh chở người (sedan, hatchback, SUV, taxi). | img_015 (hai xe ở mép ảnh), img_025 (sedan đen), img_040 (P, taxi) | img_012 (P) bán tải → `truck`; img_009 xe buýt mini → ngoài lớp (R-07) |
| `truck` | Xe có **thùng hàng riêng** phía sau cabin: xe tải, bán tải, xe tải nhỏ thùng hở/bạt. | img_002 (P, đầu kéo chở xe), img_012 (P, bán tải chở hàng, chụp từ phía sau), img_036 (xe tải nhỏ xanh mui bạt), img_037 (bán tải trắng có mui che), img_007 (bán tải Hilux và xe tải Isuzu), img_001 (bán tải thùng hở) | Xe thùng kín cỡ nhỏ → có thể là `van` (R-06) |
| `van` | Xe **thùng kín liền khối** cỡ nhỏ, không có thùng hàng tách khỏi cabin. | img_016 (van trắng giữa ảnh), img_005 (P, van trắng phía sau) | Xe có thùng hàng hở → `truck` |
| `motorcycle` | Xe hai bánh có động cơ (xe máy, xe ga, mô tô), **chỉ phần xe**, không gồm người ngồi. | img_005 (P), img_006 (P), img_008 (P), img_026 (P), img_030 | Xe đạp, xích lô, xe ba bánh → ngoài lớp (R-07) |
| `person` | Người thật (đi bộ, đứng, ngồi trên xe). | img_014, img_034, img_005 (P) | Tượng, ma-nơ-canh, hình in (R-04) |
| `ignore_region` | Vùng không tách được từng vật hoặc ngoài phạm vi gán; bỏ sót ở đây không tính lỗi. | img_021 (rừng xe máy phía sau), img_030 (bãi xe), img_032 (đám đông xa) | Không dùng để "né" vật rõ ràng gán được |

**Vật không thuộc lớp nào** (xe đạp, xích lô, tuk-tuk, xe buýt…): **không vẽ box cho vật đó** (R-07). Người ngồi/đi trên chúng vẫn gán `person`. Ghi vào `image_issues.csv` để nhóm quyết có thêm lớp không.

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

## 3. Quy tắc vẽ box

| ID | Quy tắc |
|---|---|
| R-01 | **Ôm sát phần nhìn thấy.** Cạnh box chạm điểm ngoài cùng của vật, sai số ≤ 2 px khi vật cao > 50 px, ≤ 1 px khi nhỏ hơn. Không bù phần bị che. |
| R-02 | **Người + xe máy = box riêng.** `motorcycle` ôm xe (không gồm thân người), `person` ôm phần người nhìn thấy gồm cả phần ngồi lên xe. Hai box được phép chồng nhau. Mỗi người trên xe một `person`. Ví dụ: img_026 (P, 2 người 1 xe → 2 `person` + 1 `motorcycle`), img_005 (P, mỗi người đội mũ một `person`). |
| R-03 | **Vật bị che:** chỉ vẽ nếu còn thấy ≥ 30% hoặc nhận ra rõ lớp (xe thấy bánh + đầu xe, người thấy đầu + vai). Che nặng hơn, không nhận ra → không vẽ; nếu cả cụm như vậy dùng `ignore_region` (R-05). Gán `occluded_level` theo bảng. |
| R-04 | **Không gán vật giả:** tượng, mô hình, đồ chơi, ma-nơ-canh, hình in/áp phích/tranh tường, **phản chiếu** trong gương/kính/nước. Ví dụ không gán: img_017 (P, tượng người cưỡi ngựa), img_027 (P, tượng xe tải trên bệ), img_033 (P, ma-nơ-canh), img_038 (tủ xe đồ chơi), img_018 (ảnh người trên biển quảng cáo), img_020 (P, xe trong gương chiếu hậu), img_026 (P, tàu trên tranh tường), img_028 (tượng ngựa trên thùng xe: không gán ngựa, xe tải cổ thật vẫn gán `truck`). |
| R-05 | **Đám đông / bãi xe dày đặc:** vật tách được rõ và cao ≥ 20 px (`min_box_height_px`) → vẽ từng box. Phần dính liền không tách được hoặc < 20 px → khoanh **một** `ignore_region` ôm cả cụm đó, không vẽ nửa vời. Ví dụ: img_021 (hàng đầu vẽ từng vật, phía sau ignore), img_006 (P) và img_008 (P) (hàng xe đậu sát), img_030 (bãi xe), img_032 (đám đông xa). |
| R-06 | **Phân `truck` / `van`:** thấy thùng hàng hở, thùng bạt hoặc thùng tách khỏi cabin → `truck`. Thân kín liền cabin kiểu xe thùng nhỏ → `van`. Chỉ thấy đầu xe, không phân được → chọn theo nóc xe (liền khối → `van`, ngược lại `truck`) và tick `can_review`. Bán tải có **mui che/canopy** sau cabin (img_037) hoặc thùng bạt (img_036) vẫn là `truck`. |
| R-07 | **Phương tiện ngoài taxonomy** (xe đạp, xích lô, tuk-tuk/xe ba bánh, xe buýt, xe buýt mini): **không vẽ box xe**, người ngồi trên vẫn gán `person`. Ví dụ: img_004 (P, hai tuk-tuk: bỏ xe, gán `person` tài xế thấy ≥ 30%), img_025 (xích lô: bỏ xe, gán người đạp), img_009 (xe buýt mini: bỏ), img_040 (P, tuk-tuk phía sau: bỏ). |
| R-08 | **Xe chở xe / xe chở vật:** xe **được chở** là xe thật thì vẫn gán theo lớp riêng, kèm `occluded_level` nếu bị che. Xe chở gán một box riêng. Hai box chồng nhau là bình thường. Ví dụ: img_002 (P: 1 `truck` cho đầu kéo + khung chở, mỗi `car` trên khung một box nếu thấy ≥ 30%), img_024 (xe nhỏ vàng trên mui xe đen: gán `car` + `can_review`). Vật được chở **không phải xe** (hàng, rau, tượng) không gán và không cắt khỏi box xe chở (img_012 P: một `truck` ôm cả thùng, không box riêng cho kiện hàng). |
| R-09 | **Vật dài nhô ra** (thanh dài người chở, img_029): box người/xe chỉ ôm người/xe, **không** kéo dài theo vật nhô ra. |
| R-10 | **Xe chủ (ego) / bộ phận xe của người chụp:** gương chiếu hậu, nắp ca-pô, tay lái của xe đang chụp không gán (img_020 P). Chỉ gán xe/người **khác** trong cảnh. |
| R-11 | **Bị cắt mép ảnh:** vẽ phần nằm trong ảnh, `truncated=yes`. Phần còn lại < 20% vật hoặc < 20 px thì không vẽ. |
| R-12 | **Chuyển động nhòe** (img_014): vẫn gán nếu nhận ra hình dạng, box ôm vùng nhòe thấy được; mờ tới mức không đoán được lớp → `ignore_region` + `can_review`. |
| R-13 | **Ban đêm / thiếu sáng** (img_008 P, img_026 P, img_031): chỉ gán vật nhận ra bằng mắt thường, không đoán vật chìm trong tối. |
| R-14 | **Cạnh dưới box phương tiện dừng ở điểm tiếp đất của bánh**, không tính chân chống, bóng đổ, bàn đạp thò xuống (kế thừa BT2 C10). Ví dụ: img_026 (P), img_005 (P). |
| R-15 | **Một vật một box.** Không vẽ hai box đè lên cùng một vật; không gộp nhiều xe thành một box (kế thừa BT2 quy tắc 3.9). Ngoại lệ duy nhất: `ignore_region` ở R-05. |
| R-16 | **Soát vùng nền sau/xa trước khi nộp:** vật cao ≥ 20 px và nhận ra được lớp phải có box, kể cả nằm sau cột, sau người, kẹt giữa hai xe lớn (BT2 C6: bỏ sót xe nhỏ/xa là nguồn bất đồng lớn nhất). |
| R-17 | **Vật ngập nước / có bóng phản chiếu** (img_015, img_031): chỉ vẽ phần nổi trên mặt nước, không vẽ bóng (kế thừa BT2 ca khó 2, hợp R-04). |
| R-19 | **Xe máy có thùng bên (sidecar)** (img_022, ảnh đen trắng, xa): một `motorcycle` ôm cả xe + thùng bên; người ngồi gán `person` nếu nhận ra, nhỏ quá thì bỏ (R-16). |
| R-20 | **Xe lễ hội / xe chế tạo riêng** (img_019, xe vàng hình xe đua có người lái bên trong): xe thật đang chạy trên đường thì gán `car` + `can_review`; nhân vật bông/chuột trên xe không gán; người lái gán `person`. Đám đông sau hàng rào gán `ignore_region`. |
| R-18 | **Hàng nhô ra khỏi xe:** xe chở hàng cồng kềnh vẫn giữ lớp xe; box mở rộng bao phần hàng gắn liền xe, trừ vật dài nhô quá thân (R-09). Hàng nằm trong thùng thì bao theo R-08. |

## 4. Ca khó

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

### Bảng đọc từng ảnh (đã xem lại ở độ phân giải cao)

| Ảnh | Có gì | Gán | Không gán / lưu ý |
|---|---|---|---|
| 001 | Bán tải trắng thùng hở, người ngồi quán bia phía sau | `truck`; `person` thấy ≥ 30% (che, `occluded_level` 1–2) | Bàn ghế, hình trên bảng hiệu |
| 002 | Đầu kéo chở 8 ô tô, 2 tầng | 1 `truck`; từng `car` thấy ≥ 30% (tầng dưới che nhiều) | Người xa mép phải nếu < 20 px |
| 003 | Người bán rong gánh trái cây, người dắt xe đạp, xe máy phía sau | `person` (3–4 người rõ), `motorcycle` thấy ≥ 30% | Xe đạp (ngoài lớp); nền xe máy xa dính liền → `ignore_region` |
| 004 | Hai tuk-tuk xanh, tài xế ngồi trong | `person` tài xế nếu thấy ≥ 30% | Tuk-tuk (ngoài lớp), nón cone |
| 005 | 4 người đội mũ bảo hiểm ngồi sát trên xe máy, van trắng sau | `person` từng người; `motorcycle` thấy ≥ 30%; `van` | Che nhiều giữa người với nhau → `occluded_level` 2 |
| 006 | Nhiều xe máy nhìn từ phía sau, 1 taxi trắng, xe đạp | Từng `motorcycle` + `person` rõ; `car` taxi (cắt mép trái, `truncated=yes`) | Xe đạp; hàng xa dính liền → `ignore_region` |
| 007 | Bán tải Hilux trắng + xe tải Isuzu trong gara tối | 2 `truck` | Rào chắn cam |
| 008 | Đêm, xe máy đỗ dày, 2 tài xế áo cam | Xe/người rõ phía trước | Dãy xe sau → `ignore_region` (R-05, R-13) |
| 009 | Xe buýt mini đang chạy, nhà dân | Không có vật thuộc lớp rõ | Xe buýt mini bỏ (R-07); xe máy xa dưới 20 px bỏ |
| 010 | Chợ: xe máy 2 người, người bán rau, 2 xe máy đỗ | `motorcycle` (3), `person` (≥ 4) | Xe đẩy rau (ngoài lớp); hàng hóa |
| 011 | Tượng Predator + xe máy điêu khắc kim loại, hội chợ | Không gán tượng / xe điêu khắc (R-04) | Người xa dưới 20 px bỏ |
| 012 | Thùng bán tải đầy hàng (cắt mép), Mazda xám phía sau | `truck` (`truncated=yes`); `car` | Hàng trong thùng không box riêng (R-08) |
| 013 | Đêm, quán nhỏ, 2–3 người và xe rất xa | Chỉ vật ≥ 20 px, nhận ra được | Ảnh gần rỗng (R-13, R-16) |
| 014 | 2 người đi bộ rõ giữa xe máy nhòe | 2 `person` rõ | Nền nhòe: nhận ra thì gán, không thì `ignore_region` (R-12) |
| 015 | Xe đỏ (trái) và SUV bạc (phải) cắt mép, xe nền, mặt đường phản chiếu | 2 `car` `truncated=yes`; xe nền nếu nhận ra | Bóng phản chiếu trên mặt đường (R-17) |
| 016 | 2 tuk-tuk, Vespa xanh có tài xế, van trắng, người góc dưới phải cắt mép | `motorcycle` + `person` tài xế; `van`; `person` góc phải `truncated=yes` | Tuk-tuk (R-07) |
| 017 | Tượng người cưỡi ngựa, nón cone trên đầu | Không gán | R-04 |
| 018 | Biển quảng cáo có chân dung, bãi xe sau hàng rào | `car` thấy ≥ 30% sau hàng rào (`occluded_level` 1–2) | Chân dung trên biển (R-04) |
| 019 | Xe vàng hình xe đua, người lái, chuột bông, đám đông sau rào | `car` + `can_review` (R-20); `person` lái | Chuột bông; đám đông → `ignore_region` |
| 020 | Gương chiếu hậu có phản chiếu | Không gán | R-04, R-10 |
| 021 | Rừng xe máy đông, hàng đầu rõ | `motorcycle` + `person` hàng 1–2 | Phía sau `ignore_region` (R-05) |
| 022 | Ảnh đen trắng, xe máy sidecar xa trên đường rừng | `motorcycle` (R-19) nếu ≥ 20 px | Người nhỏ có thể bỏ |
| 023 | Honda sedan đen, xích lô, xe máy xa | `car`; `person` đạp xích lô; `person` + `motorcycle` xa nếu ≥ 20 px | Xích lô (R-07) |
| 024 | Xe wagon đen, xe vàng nhỏ trên mui, nhiều xe cổ bảo tàng | `car` đen; `car` vàng + `can_review`; xe cổ phía sau nếu rõ | Biển Texaco |
| 025 | Đại lộ ven biển, người đi bộ xa, taxi/xe máy xa | Chỉ vật ≥ 20 px | Nhiều vật dưới ngưỡng, ảnh gần rỗng |
| 026 | Đêm, 2 người trên xe máy đỏ, tranh tường cảng | 2 `person` + `motorcycle` | Tranh tường (R-04) |
| 027 | Bia mộ hình xe tải đá đen trên cỏ | Không gán | R-04 |
| 028 | Xe tải cổ thật chở ngựa tượng, xe đỏ phía sau | `truck`; `car` đỏ | Ngựa tượng (R-04) |
| 029 | Xe máy chở ống dài, người đạp xe đạp | 2 `person` + `motorcycle` | Xe đạp (R-07); ống dài (R-09); người nhỏ xa bỏ |
| 030 | Bãi xe máy dày, người áo xanh | Vài `motorcycle` hàng trước; `person` áo xanh | Phần còn lại `ignore_region` (R-05) |
| 031 | Đêm mưa, SUV trắng, xe khác, xe buýt xa | `car` rõ | Xe buýt (R-07), phản chiếu mặt đường (R-17) |
| 032 | Đám đông xếp hàng chờ xe, sedan xanh cắt mép trái | `car` `truncated=yes` | Đám đông xa → `ignore_region`; nón cone không gán |
| 033 | Ma-nơ-canh, quần áo, gương xe tải | Không gán | R-04 |
| 034 | Người đi bộ băng ngang, sedan đen, xe máy, người lái xe cắt mép phải | `person` đi bộ, `car`, `motorcycle` + `person` rõ; xe bên phải `truncated=yes` | Xe xa dưới 20 px |
| 035 | 2 xe ba bánh vàng (1 chở hàng cồng kềnh), xe máy, ô tô trắng nhỏ | `motorcycle` + `person`; `car` trắng | Xe ba bánh bỏ (R-07) |
| 036 | Xe tải nhỏ xanh mui bạt đỗ sát lề, xe máy đỗ bên trái | `truck`; xe máy đỗ thấy rõ | Biển số bị làm mờ |
| 037 | Bán tải trắng có mui che, xe buýt xanh sau, người đi bộ | `truck` (R-06); `person` nếu ≥ 20 px | Xe buýt (R-07) |
| 038 | Tủ trưng bày đồ chơi, xe mô hình | Không gán | R-04 |
| 039 | Phố nhỏ, xe máy đỗ trái, nhiều xe máy/người xa | `motorcycle` đỗ trái; vật ≥ 20 px | Nhiều vật dưới ngưỡng (R-16) |
| 040 | Taxi xanh, người đội mũ bảo hiểm đen trên xe máy tiền cảnh (cắt mép), tuk-tuk vàng, SUV đen, xe buýt | `person` + `motorcycle` (gương chrome) `truncated=yes`; `car` taxi; `car` SUV | Tuk-tuk, xe buýt (R-07) |

**Câu hỏi để nhóm chốt ở Pha 2:** (1) có thêm lớp `bus` / xe ba bánh / xe đạp không, hay giữ R-07 (xuất hiện ở img_003, 004, 009, 016, 023, 029, 031, 035, 037, 040); (2) `van` vs `truck` khi chỉ thấy đầu xe; (3) ngưỡng che 30% ở R-03 có hợp lý không.

> Lưu ý: bảng trên lập sau khi xem lại cả 40 ảnh ở độ phân giải cao. Số lượng box cụ thể chưa đếm; các ca ghi `can_review` cần xem lại trên CVAT trước khi chốt.

## 5. QC và phiên bản

- Ngưỡng QC theo `submission/taxonomy.json`: IoU ghép ≥ 0.5; IAA IoU ≥ 0.85, cùng lớp ≥ 0.95; lỗi theo ảnh ≤ 2%.
- Ca mơ hồ: tick `can_review`, ghi mã `R-xx`; ca chưa có box ghi vào `submission/qc/image_issues.csv` (cột `image,annotator,region,note`).
- Ca mơ hồ cấp guideline do 113 đề xuất, cả nhóm chốt ở Pha 2.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản giảng viên | — |
| v0.2 (113) | Thêm R-01…R-20, ngưỡng `occluded_level`, quy tắc vật giả/phản chiếu, người + xe máy box riêng, xe chở xe, phương tiện ngoài lớp, sidecar, xe lễ hội; R-14…R-18 kế thừa từ BT2 v1.1; thêm bảng đọc từng ảnh cho cả 40 ảnh | Đã xem lại cả 40 ảnh; ca khó chính: img_002, 004, 005, 006, 008, 012, 017, 019, 020, 022, 024, 026, 027, 033, 040 |
