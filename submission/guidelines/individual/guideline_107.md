# Guideline gán nhãn — v1.0 (nhóm thống nhất)

- Phiên bản: **v1.0** (khóa cho lượt gán độc lập Pha 3)
- Ngày: 2026-11-16
- Người viết / duyệt: 101, 102, 103, 104 (thay bằng mã thật của nhóm)
- Loại nhãn: bounding box trên ảnh 2D, CVAT, xuất COCO 1.0
- Taxonomy đi kèm: `submission/taxonomy.json` (`version: v1.0`)

---

## 1. Mục tiêu

Nhãn dùng để huấn luyện mô hình **phát hiện người và phương tiện tham gia giao thông** trên ảnh
đường phố (camera giao thông, hỗ trợ lái xe).

- **Sai nguy hiểm nhất:** bỏ sót người hoặc xe **thật** (mô hình không thấy vật có thể va chạm).
- **Sai tốn kém thứ hai:** gán box cho vật **không thật** (tượng, ảnh in, phản chiếu, đồ chơi) — mô hình học báo động giả.
- Vì vậy: vật thật thì gán; vật không thật thì không gán; vật thật nhưng không vẽ được chính xác thì phủ `ignore_region`.

## 2. Lớp và thuộc tính

### 2.1 Lớp

Phép thử chung khi chọn lớp: **nhìn vào phần thấy được, có biết chắc lớp không?** Nếu phải đoán → chọn theo quy tắc mặc định trong bảng và tick `can_review`.

| Lớp | Định nghĩa (một câu) | Ví dụ trong lô | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe ô tô chở người ≤ 9 chỗ: sedan, hatchback, SUV, MPV, taxi, xe mui trần. | img_015, img_023 (Civic), img_024 (Pacer), img_019 (xe diễu hành Dangermouse) | Pickup có thùng hở → `truck`. Xe thùng cao, cửa lùa → `van`. |
| `truck` | Xe có **khoang hàng tách khỏi cabin**: xe tải, xe ben, **pickup** (kể cả có nắp thùng), đầu kéo + rơ-moóc. | img_001, img_002, img_007, img_012, img_028, img_036, img_037 | SUV kín mui không có thùng → `car`. |
| `van` | Xe thân hộp liền một khối, mui cao, thường có cửa lùa, chở người/hàng, **≤ 16 chỗ**. | img_005 (xe 51LD-70.65), img_016 (HiAce trắng) | Minibus ≥ 20 chỗ, cửa kiểu buýt → `bus`. MPV gầm thấp → `car`. |
| `bus` | Xe chở khách thân dài, **cửa lên xuống kiểu xe buýt**, hàng ≥ 5 cửa sổ khách mỗi bên (gồm minibus/coaster). | img_009, img_031, img_037, img_040 | Van 16 chỗ → `van`. |
| `motorcycle` | Xe 2 bánh có động cơ: xe máy, tay ga, mô tô, xe máy điện; **kể cả sidecar / thùng kéo gắn liền**. | img_005, img_006, img_010, img_022 (sidecar), img_026, img_029 (xe điện) | Xe đạp điện **còn bàn đạp** → `bicycle`; xe máy điện không bàn đạp → `motorcycle`. Không thấy rõ → `motorcycle` + `can_review`. |
| `bicycle` | Phương tiện **đạp chân**, không động cơ: xe đạp, xe đạp chở hàng, **xích lô**. | img_003, img_006, img_023 (xích lô), img_029 | Xe 3 bánh có động cơ → `three_wheeler`. |
| `three_wheeler` | Xe **3 bánh có động cơ** chở khách/hàng, có mái: tuk-tuk, auto-rickshaw, xe lam. | img_004, img_016, img_035, img_040 | Xe máy kèm sidecar → `motorcycle`. Xích lô → `bicycle`. |
| `person` | Người thật, đi bộ, đứng, ngồi, hoặc **ngồi trên xe không có mái** (xe máy, xe đạp, xích lô, sidecar, xe mui trần). | img_014, img_026, img_034 | Tượng, ma-nơ-canh, hình nộm, người trong ảnh in → không gán (R-03). Người trong khoang có mái → không gán (R-07). |
| `ignore_region` | Vùng **không phải vật**: nơi có vật thật nhưng không gán từng cái được (đám đông, vật < 20 px, mờ chuyển động mạnh). Bỏ sót trong vùng này không tính lỗi. | img_021, img_030 (bãi xe), img_019 (khán giả) | Không dùng cho tượng / ảnh in / phản chiếu (những thứ đó đơn giản là không gán). |

**Vật không thuộc lớp nào:**
- Không phải phương tiện / người (con vật, cọc tiêu, biển báo, quang gánh, nón treo…) → **không gán gì**.
- Phương tiện thật ngoài taxonomy (tàu hỏa, máy công trình, xe đẩy tay) → `ignore_region` ôm vật đó. Không tạo lớp mới khi đang gán; ghi vào `image_issues.csv`.

### 2.2 Thuộc tính

| Thuộc tính | Mức | Ngưỡng đo |
|---|---|---|
| `occluded_level` | `0` | Bị vật khác che **< 10%** diện tích ước lượng của vật. |
| | `1` | Che **10% – < 40%**. |
| | `2` | Che **40% – < 75%**. |
| | `3` | Che **≥ 75%**, nhưng phần còn lại vẫn đủ nhận ra lớp (R-09). |
| `truncated` | `yes` | Box chạm mép ảnh (cách mép ≤ 2 px) **và** vật còn phần nằm ngoài khung. |
| | `no` | Mọi trường hợp còn lại. |
| `can_review` | tick | Phải **đoán** lớp hoặc biên box sau khi đã áp quy tắc. Không tick thay cho quy tắc đã có. |

Cách tính `occluded_level`:
- Chỉ tính phần bị **vật khác** che. Phần ra ngoài mép ảnh là `truncated`, không cộng vào che.
- Người ngồi trên xe che phần thân xe → **có** tính vào `occluded_level` của xe.
- Song hàng rào, lưới thưa, kính trong (img_018, img_030): nhìn rõ vật qua khe → tối đa mức `1`.
- `ignore_region` không cần thuộc tính (để mặc định).

## 3. Quy tắc vẽ box

| ID | Quy tắc |
|---|---|
| **R-01** | Box ôm sát **phần nhìn thấy** của vật (không đoán phần bị che). Sai số chấp nhận ≈ 2 px mỗi cạnh. |
| **R-02** | Gán mọi `person` và phương tiện **thật** thuộc taxonomy có box cao **≥ 20 px**. |
| **R-03** | **Không gán** vật không thật: tượng, tượng đài, ma-nơ-canh, hình nộm/mascot, mô hình, đồ chơi, ảnh in, biển quảng cáo, tranh tường, màn hình. Không cần `ignore_region`. |
| **R-04** | **Không gán** hình phản chiếu (gương, kính cửa hàng, mặt đường ướt, vũng nước). |
| **R-05** | **Phương tiện thật cỡ thật đang trưng bày / diễu hành / độ chế** vẫn gán theo lớp (img_011 xe độ, img_019 xe diễu hành, img_024 xe trong bảo tàng). Phép thử: *xe chạy được và đúng kích thước thật?* |
| **R-06** | **Người và xe là hai box riêng.** Mỗi người trên xe máy / xe đạp / xích lô / sidecar có một box `person`; xe có một box riêng. Hai người trên một xe → 3 box. |
| **R-07** | Người ngồi **trong khoang có mái** (ô tô, van, bus, cabin tải, tuk-tuk) → **không gán** `person`, kể cả thấy qua kính. Xe không mái (xe máy, xe đạp, sidecar, xe mui trần img_019) → gán. |
| **R-08** | **Box người** gồm mũ, nón lá, quần áo, ba lô đang đeo, chân đặt trên xe. **Không gồm** vật cầm tay / gánh: quang gánh (img_003), ống dài (img_029), túi xách cầm tay. |
| **R-09** | Phần nhìn thấy phải **đủ nhận ra lớp**: người thấy ít nhất **đầu hoặc thân**; xe thấy ít nhất **bánh + một phần thân/đèn**. Chỉ thấy tay/chân, chỉ thấy gương xe → không gán. |
| **R-10** | **Box xe** gồm thân, gương, giá nóc, thùng hàng, nắp thùng, sidecar, rơ-moóc dính liền. **Không gồm hàng hóa chất vượt ra ngoài thân xe** (bao tải trên nóc img_035, tượng ngựa img_028, xe mô hình trên nóc img_024). Lý do: biên thân xe rõ → hai người vẽ trùng; hàng hóa không có hình dạng cố định. |
| **R-11** | **Xe chở xe:** đầu kéo + khung chở là **một** box `truck` (theo R-10, tới đỉnh khung). Mỗi xe con trên khung là xe thật → gán `car` riêng, che bởi khung tính theo R-01/2.2 (img_002). |
| **R-12** | **Xe chủ (ego):** phần xe của người chụp (gương, khung cửa, capo, tay lái sát ống kính) → không gán (img_020). |
| **R-13** | **Vật nhỏ:** vật thật cao **< 20 px** → không vẽ box lớp. Phủ bằng `ignore_region`; các vật nhỏ nằm gần nhau gộp **một** vùng. |
| **R-14** | **Đám đông:** cụm **≥ 5 vật** chồng lấn mà đa số che ≥ 40% → vẽ **một** `ignore_region` ôm sát cả cụm (từ vật ngoài cùng trái → phải, trên → dưới). Vật trong cụm vẫn **gán riêng** nếu che < 40% và cao ≥ 20 px (box được phép nằm trong vùng ignore). |
| **R-15** | **Mờ chuyển động mạnh:** không xác định được biên vật trong khoảng ±10 px → `ignore_region` ôm vệt mờ, không gán lớp (img_014). Mờ nhẹ, vẫn thấy rõ hình dạng → gán bình thường (img_015, img_026). |
| **R-16** | **Pickup vs SUV:** thấy thùng hở / nắp thùng phía sau → `truck`; không thấy phần đuôi để phân biệt → `car` + tick `can_review`. |
| **R-17** | Ảnh **không có vật nào** cần gán (img_017, img_020, img_027, img_033, img_038) vẫn phải có mặt trong COCO export, không có annotation. |

Thứ tự áp dụng khi gặp một vật: **R-03/R-04 (thật không?) → R-12 (xe chủ?) → R-09 (nhận ra lớp?) → R-13/R-14/R-15 (vẽ riêng được không?) → chọn lớp (mục 2.1) → vẽ box (R-01, R-06, R-08, R-10) → thuộc tính.**

## 4. Ca khó theo ảnh (cả 40 ảnh)

> Cột “Gán” liệt kê lớp chính cần có và quyết định cho ca khó. Đây **không phải** đáp án đếm box; mỗi người vẫn tự gán và đếm.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_001 | Mini truck Suzuki chở ống; nhiều người ngồi quán phía sau; poster hot dog | R-10, R-02, R-03 | `truck` (truncated=yes, phải); mỗi người thật → `person` theo mức che; poster không gán | Xe có thùng hàng riêng → truck. Ống nằm trong thùng → không ảnh hưởng box. |
| img_002 | Xe chở xe con, 2 tầng; công nhân bên phải; xe nhỏ xa | R-11, R-10, R-13 | 1 `truck` (đầu kéo + khung); mỗi xe con trên khung → `car`; công nhân → `person`; xe xa < 20 px → `ignore_region` | Xe con là vật thật đúng lớp. Phần xe con nhô trên đỉnh khung không tính vào box truck. |
| img_003 | Người bán hàng quang gánh, nón lá; xe đạp; bãi xe máy phía sau | R-08, R-14, R-06 | `person` không gồm quang gánh, gồm nón lá; `bicycle`; cụm xe máy đỗ phía phải → `ignore_region` + xe rõ gán riêng | Vật gánh không phải phần cơ thể. |
| img_004 | 2 tuk-tuk đỗ, tài xế ngồi trong | R-07 | 2 `three_wheeler`; **không** gán tài xế | Tuk-tuk có mái → R-07. Cọc tiêu không gán. |
| img_005 | Cận cảnh người đi xe máy chen nhau; van bạc phía sau; tay người ở mép trái | R-06, R-09, R-01 | Mỗi người thấy đầu → `person`; xe máy thấy bánh/thân → `motorcycle`; xe 51LD → `van`; xe hộp trắng góc trái → `van` truncated; ô tô bạc trái → `car`; chỉ thấy tay → không gán | Nhiều xe máy chỉ thấy tay lái/gương → không đủ nhận ra (R-09). |
| img_006 | Dòng xe máy, xe đạp nhìn từ sau; taxi trái | R-06, R-14 | Mỗi xe + người phía trước gán riêng; `bicycle` + `person` cho cô gái áo kem; cụm xe xa → `ignore_region`; taxi → `car` truncated | Hàng xe xa chồng lấn → R-14. |
| img_007 | Kho tối: pickup có khung thùng, xe Isuzu, xe thùng phía sau | R-10, R-16, R-09 | Pickup → `truck`; Isuzu → `truck` truncated; xe thùng sau pickup → `truck` (che mức 2); bóng người giữa xe nếu thấy thân → `person` + `can_review` | Thiếu sáng: chỉ gán khi nhận ra theo R-09. |
| img_008 | Phố đêm, người mặc áo xe ôm, nhiều xe máy đỗ, đám đông xa | R-06, R-14 | Người áo số 4 + xe trắng → `person` + `motorcycle`; người áo số 7 → `person`; xe đỗ phía trước gán riêng; đám đông + xe xa → `ignore_region`; xe lớn ở giữa xa → `bus` + `can_review` | Hình vẽ nhân vật ở trái là poster → R-03. |
| img_009 | Minibus; người trên ban công; xe máy chạy và đỗ | R-07, R-02, R-13 | Minibus → `bus`; khách trong xe không gán; người đi xe máy trái → `person` + `motorcycle`; xe đỗ phải gán riêng; người ban công ≥ 20 px → `person`, nhỏ hơn → `ignore_region` | Minibus nhiều cửa sổ, cửa kiểu buýt → `bus`. Con chó không gán. |
| img_010 | 2 người trên xe ga; người bán chuối với xe đạp chở hàng; cô gái ngồi xe | R-06, R-10 | Xe 29-K1 → `motorcycle` + 2 `person`; xe đạp chở chuối → `bicycle`, không gồm chuối nhô lên; người bán → `person`; cô gái + xe 29-C1 → `person` + `motorcycle`; xe đỗ hai bên gán riêng | Hàng chất trên xe không vào box (R-10). |
| img_011 | Tượng Predator khổng lồ; mô tô độ bằng kim loại trưng bày; xe trắng; đám đông | R-03, R-05, R-14 | Tượng → không gán; mô tô độ cỡ thật → `motorcycle`; xe trắng → `van` (che bởi tượng); 2 người gần → `person`; đám đông xa → `ignore_region` | Đầu tượng to hơn người thật nhiều → không phải người hóa trang. Xe độ là xe thật (R-05). |
| img_012 | Pickup đầy hàng (nhìn từ thùng); Mazda; xe tải xa | R-16, R-10 | Pickup → `truck` truncated; Mazda → `car`; xe tải hộp → `truck`; xe xa nhỏ → `ignore_region` | Hàng nằm trong thùng. |
| img_013 | Đêm mưa: 2 người đi bộ; tượng rồng vàng, tượng đá; xe xa; cọc tiêu | R-03, R-04, R-13 | 2 `person`; xe trắng → `car`; xe máy đỗ có cọc che → `motorcycle`; dãy xe xa < 20 px → `ignore_region`; tượng và bóng phản chiếu → không gán | Phản chiếu mặt đường → R-04. |
| img_014 | 2 người đi bộ rõ; người đi xe máy mờ do lia máy | R-15 | 2 `person` rõ; mỗi vệt người+xe mờ mạnh → `ignore_region` | Biên mờ > ±10 px, hai người sẽ vẽ khác nhau. |
| img_015 | Xe đỏ, xe bạc cắt mép; xe mờ phía sau; mặt đường ướt phản chiếu | R-01, R-15, R-04 | Xe đỏ, xe bạc → `car` truncated; xe nền thấy rõ hình dạng → `car`; phản chiếu không gán | Xe đen mờ vẫn rõ hình → gán. |
| img_016 | Tuk-tuk trái, tuk-tuk xanh phải; Vespa chở hàng; HiAce; pickup; phụ nữ áo đỏ | R-07, R-10, R-16 | 2 `three_wheeler` (truncated); Vespa → `motorcycle` (không gồm hàng nhô ra) + `person`; HiAce → `van`; pickup Isuzu → `truck`; xe đen → `car`; phụ nữ → `person` truncated; khách trong tuk-tuk không gán | Mảng tóc góc trái dưới không đủ nhận ra → R-09. |
| img_017 | Tượng người cưỡi ngựa đội nón giao thông | R-03, R-17 | **Không gán**; ảnh vẫn có trong COCO | Tượng. |
| img_018 | Biển quảng cáo có người; bãi xe sau hàng rào; chụp qua kính | R-03, R-16, 2.2 | Người trên biển không gán; mỗi xe → `car` (che mức ≤ 1 do song rào); xe tối màu 9A6 → `car` + `can_review` (không thấy đuôi) | Song rào thưa → tối đa mức 1. |
| img_019 | Xe diễu hành Dangermouse có tài xế; mascot chuột; khán giả sau rào | R-05, R-07, R-03, R-14 | Xe → `car`; tài xế → `person` (xe không mui); mascot → không gán; khán giả → 1 `ignore_region` ôm đám đông sau rào; người áo phản quang phải → `person`; đầu người mờ góc phải dưới → `person` truncated | Xe thật, có biển số, chạy được. |
| img_020 | Gương chiếu hậu phản chiếu xe, cầu vồng | R-04, R-12, R-17 | **Không gán** | Xe trong gương là phản chiếu; gương là xe chủ. |
| img_021 | Dòng xe máy cực đông giờ cao điểm | R-14, R-06, R-13 | Các xe + người hàng trước, che < 40% → gán riêng; toàn bộ khối xe phía sau → 1 `ignore_region`; ô tô trắng trái → `car`; xe buýt xa → `bus` nếu ≥ 20 px | Ảnh tốn thời gian nhất: chia 2 người gán đều phải theo R-14 để vùng ignore khớp. |
| img_022 | Ảnh đen trắng: xe máy kèm sidecar, người ngồi sidecar; xe xa | R-05, R-06, R-13 | 1 `motorcycle` gồm sidecar; người trong sidecar (thấy đầu) → `person` occluded 3; xe xa nhỏ → `ignore_region` | Sidecar gắn liền thân xe (R-10). |
| img_023 | Xích lô; Civic đen; xe máy; người đi bộ, người ngồi lề | R-06, 2.1 | Xích lô → `bicycle` + `person` người đạp; Civic → `car`; xe máy + người giữa → `motorcycle` + `person`; người đứng/ngồi → `person`; dãy xe đỗ xa → `ignore_region` | Xích lô đạp chân → `bicycle`. |
| img_024 | Bảo tàng xe: Pacer đen chở xe mô hình vàng trên nóc | R-05, R-03, R-10, R-14 | Pacer → `car`, box **không** gồm xe vàng; xe vàng → không gán (mô hình thu nhỏ); xe hai bên → `car`; dãy xe xa → `ignore_region`; mảng xe cam góc trái dưới → `car` truncated | Xe trưng bày cỡ thật vẫn là xe (R-05). |
| img_025 | Phố đi bộ ven biển: người đi bộ, người ngồi ghế; xe máy kéo thùng; taxi | R-13, R-14, R-06 | Người gần → `person`; người xa < 20 px và cụm ghế bãi biển → `ignore_region`; xe máy kéo thùng → `motorcycle` (gồm thùng) + `person`; taxi, xe trắng → `car`; pickup mép phải → `truck` truncated | Thùng kéo gắn liền như sidecar. |
| img_026 | Cặp đôi đi xe máy; tranh tường cảng biển | R-06, R-03 | 1 `motorcycle` + 2 `person`; tranh tường không gán | Hai box người riêng. |
| img_027 | Bia mộ hình xe pickup bằng đá | R-03, R-17 | **Không gán** | Tượng/mô hình. |
| img_028 | Pickup cổ chở tượng ngựa; SUV đỏ phía sau | R-10, R-03 | Pickup → `truck`, box **không** gồm tượng ngựa; SUV → `car` (che bởi pickup) | Tượng là hàng chất vượt thân xe. |
| img_029 | Người đi xe điện và người đi xe đạp cùng khiêng ống dài; người đi bộ phía sau | R-08, R-06 | Xe điện → `motorcycle` + `person`; xe đạp → `bicycle` + `person`; ống không gán, không vào box nào; người đi bộ, người đạp xe xa → gán nếu ≥ 20 px | Ống là vật cầm tay (R-08). |
| img_030 | Bãi gửi xe máy dày đặc; bảo vệ; poster người | R-14, R-03 | Xe hàng trước che < 40% → `motorcycle` riêng; phần bãi còn lại → 1 `ignore_region`; bảo vệ → `person`; poster không gán | Đám đông xe (R-14). |
| img_031 | Đêm mưa Đài Bắc: ô tô, xe buýt, xe máy, người đi bộ; phản chiếu | R-04, R-06, R-13 | Ô tô → `car`; xe KKA-25 → `bus`; người đi xe máy → `person` + `motorcycle`; người đi bộ phải → `person`; cụm người vỉa hè trái nhỏ → `ignore_region`; phản chiếu, hình vẽ trên tòa nhà không gán | |
| img_032 | Nhóm ~30 người chờ xe buýt; xe đỗ phía sau; cọc tiêu | R-14, R-01 | Hàng người → 1 `ignore_region` + người che < 40% gán riêng; người đứng tách bên phải → `person`; xe xanh trái → `car` truncated; xe đỗ phía sau → `car` theo mức che | Poster trong nhà chờ không gán. |
| img_033 | Ma-nơ-canh; người trong ảnh in; phản chiếu xe trắng trên kính | R-03, R-04, R-17 | **Không gán** | Toàn bộ là vật không thật / phản chiếu. |
| img_034 | Người băng qua đường; Toyota đen; nhiều xe máy | R-06, R-13 | Người đi bộ → `person`; ô tô → `car`; mỗi xe máy + người ≥ 20 px → gán; người + xe đạp → `bicycle` + `person`; người ba lô xanh mép phải → `person` + `motorcycle` truncated; cụm xe xa → `ignore_region` | |
| img_035 | Auto-rickshaw chở bao tải chất cao; rickshaw thứ hai; xe máy | R-10, R-07 | Rickshaw → `three_wheeler`, box **chỉ thân xe** (không gồm bao tải); tài xế không gán; rickshaw phải → `three_wheeler` (che bởi người đi xe máy); 2 xe máy + người → `motorcycle` + `person`; 2 ô tô trắng → `car` | Ca tranh cãi nhất của lô: chốt theo R-10. |
| img_036 | Xe tải nhẹ Veryca phủ bạt; xe máy đỗ hai bên; người trong quảng cáo | R-10, R-14, R-03 | Xe → `truck`; xe máy đỗ rõ → `motorcycle`; cụm xe chồng nhau → `ignore_region`; người trong quảng cáo không gán; đầu người thật sau xe → `person` occluded 3 + `can_review` | |
| img_037 | Pickup có nắp thùng cao; xe buýt GO; người đi bộ | R-16 | Pickup → `truck`; xe buýt trái → `bus`; xe buýt sau pickup → `bus` (che); người đi bộ → `person` | Nắp thùng vẫn là pickup (R-16). |
| img_038 | Tủ kính đồ chơi: xe mô hình, búp bê, vịt | R-03, R-17 | **Không gán** | Đồ chơi. |
| img_039 | Phố Huế: người đi bộ, xe máy, xe đạp, dãy xe đỗ | R-06, R-14 | Mỗi người + xe gán riêng; xe máy đỗ trái → `motorcycle`; dãy xe đỗ chồng nhau → `ignore_region`; ô tô xa → `car` nếu ≥ 20 px | Biển hiệu không gán. |
| img_040 | Người đội mũ bảo hiểm sát ống kính; taxi xanh; tuk-tuk; SUV; xe buýt | R-09, R-07, R-03 | Người → `person` truncated; xe máy chỉ thấy gương → không gán (R-09); taxi → `car` truncated; tuk-tuk → `three_wheeler`; khách tuk-tuk không gán; SUV → `car`; xe buýt → `bus`; ảnh dán trên kính taxi không gán | |

## 5. QC và phiên bản

**Ngưỡng QC** (giữ nguyên `rules` trong taxonomy):

| Đại lượng | Ngưỡng |
|---|---|
| Box nhỏ nhất | cao ≥ 20 px (nhỏ hơn → `ignore_region`) |
| IoU đạt | box cao ≥ 50 px: 0.85; nhỏ hơn: 0.7 |
| IAA | IoU TB ≥ 0.85, cùng lớp ≥ 95% trên cặp ghép (IoU ghép ≥ 0.5) |
| Lỗi theo ảnh | ≤ 2% mới Release (lô 40 ảnh: 1 ảnh lỗi đã vượt) |

**Ai quyết ca mơ hồ:**
- Khi gán: không hỏi nhau, tick `can_review` hoặc ghi `image_issues.csv`.
- Pha 5 (calibration): cả nhóm họp; người điều phối chốt, ghi `nguoi_chot` vào `calibration_decisions.csv`. Quyết định đổi cách chọn vật/lớp/box → `semantic`, `pham_vi=lo`, kiểm lại cả lô.

**Phân vai nhóm 4 người** (mỗi ảnh 2 người gán độc lập → 80 lượt, ~20 ảnh/người):

| Mã | Vai chính | Vai phụ |
|---|---|---|
| 101 | Điều phối, chốt calibration | Chạy `split_assign.py`, `qc_compare.py` |
| 102 | Giữ taxonomy, `make_cvat_labels.py`, CVAT Project | Sửa nhãn calibration |
| 103 | Người kiểm QC (khác người sửa) | Điền `qc_review.csv` |
| 104 | Viết `QC_REPORT.md`, `TEAM.md` | Kiểm `check_submission.py` |

**Lịch sử thay đổi:**

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v1.0 | Thêm lớp `bus`, `bicycle`, `three_wheeler`; định nghĩa đo được cho mọi lớp và `occluded_level`; thêm R-01 → R-17 | v0 không có lớp cho tuk-tuk/xích lô/xe buýt (img_004, 009, 023, 035, 040); không nói về tượng/phản chiếu/đồ chơi (img_017, 020, 027, 033, 038); không nói người–xe tách box (img_005, 026); hàng chất trên xe (img_002, 024, 028, 035) |
