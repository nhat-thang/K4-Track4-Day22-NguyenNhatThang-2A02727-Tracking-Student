# Báo cáo lab: chọn tracker cho 5 video

**Nhóm:** Nguyễn Nhật Thăng — 2A202602727 **Thành viên:** Nguyễn Nhật Thăng (MSSV 2A202602727)

Detector cố định: `yolo26n.pt`, ảnh 640 px, Re-ID `osnet_x0_25_msmt17`. Không đổi các mục này trong bài nộp chính.

## 1. Cấu hình đã chọn

Mỗi video: tracker bạn nộp, `conf`, `iou`, điều bạn **nhìn thấy** trên video, và một cấu hình đã thử rồi loại.

| Video | Tracker | conf | iou | Quan sát khi xem video | Đã thử nhưng loại |
|---|---|---|---|---|---|
| video_1 (quảng trường, tĩnh, ban ngày) | `botsort` | 0.1 | 0.5 | Bắt thêm nhiều người nhỏ ở xa so với conf 0.3 (frame 600: 11 hộp so với 7). Người đi gần camera giữ ID ổn định. Vẫn sót đám đông ở cuối quảng trường và người đi xe đạp. | `bytetrack` conf 0.3: ít đổi ID nhất (12) nhưng sót quá nhiều người, HOTA 26.9. `strongsort` conf 0.1: IDF1 cao (32.6) nhưng đổi ID 197 lần, MOTA còn 15.6. |
| video_2 (phố đêm, tĩnh, rất đông) | `botsort` | 0.1 | 0.5 | Người ở xa chỉ cao khoảng 70 px nên conf thấp mới bắt được. Ở conf 0.1 không thấy hộp giả trên đèn hay bóng; các hộp thêm đều là người thật. Người đứng cạnh xe máy (ID 4) giữ một ID suốt video. Đám đông góc trên trái vẫn bị sót. | `bytetrack` conf 0.3: ID rất ổn định nhưng chỉ ~9 hộp/frame, sót cả nhóm người ở giữa đường (frame 500: 6 hộp so với 13 của BoT-SORT). `strongsort` conf 0.3: bắt số người tương đương nhưng số ID tăng nhanh hơn hẳn (cuối video ID đã lên ~120 so với ~90 của BoT-SORT), tức đổi ID nhiều hơn. |
| video_3 (camera di động, ảnh nhỏ) | `ocsort` | 0.3 | 0.5 | Người đi rất gần camera, hộp to và bị che liên tục. OC-SORT giữ track dài nhất và bắt được nhóm người ở xa (frame 800: 9 hộp so với 7 của ByteTrack). | `botsort` conf 0.3: Re-ID trên ảnh 640×480, khung hình chậm không giúp, nhiều track ngắn hơn hẳn (93 so với 67). `ocsort` conf 0.15: hộp nhấp nháy, ID tăng vọt, có hộp giả trên túi xách đỏ. |
| video_4 (trong nhà, camera di chuyển) | `botsort` | 0.15 | 0.5 | Người đàn ông áo trắng giữ ID 45 từ frame 400 đến 650, kể cả khi đi sát camera ở mép khung. Không thấy hộp giả trên phản chiếu sàn hay kính ở conf 0.15. | `bytetrack` conf 0.15: ít ID hơn nhưng bắt ít người hơn, nhất là người ở xa và ở mép khung (frame 650: 7 hộp so với 9). `botsort` conf 0.5: mất bớt người ở xa trong hành lang. |
| video_5 (trên xe bus, giao lộ đông) | `botsort` | 0.15 | 0.5 | Camera rung mạnh; BoT-SORT có bù chuyển động camera nên track dài nhất và ít vụn nhất trong các tracker bắt đủ người. Bắt được người đi bộ ở xa cuối đường (frame 740: 4 hộp so với 2). | `bytetrack` conf 0.3: chỉ ~2.7 hộp/frame, mất cả nhóm người qua đường bên trái (frame 350). `ocsort` conf 0.15: hộp vụn, số ID tăng gấp đôi. |

## 2. Số liệu video_1

Dán bảng HOTA / MOTA / IDF1 do `scripts/evaluate_practice.py` in ra.

```
HOTA: nguyennhatthang_video1-pedestrian HOTA      DetA      AssA      DetRe     DetPr     AssRe     AssPr     LocA      OWTA      HOTA(0)   LocA(0)   HOTALocA(0)
video_1                                 29.523    19.561    44.952    20.335    75.327    47.931    82.084    82.598    30.152    36.707    76.442    28.059

CLEAR: nguyennhatthang_video1-pedestrian MOTA      MOTP      MODA      CLR_Re    CLR_Pr    MTR       PTR       MLR       sMOTA     CLR_TP    CLR_FN    CLR_FP    IDSW      MT        PT        ML        Frag
video_1                                  21.005    80.163    21.129    24.062    89.135    12.903    20.968    66.129    16.232    4471      14110     545       23        8         13        41        64

Identity: nguyennhatthang_video1-pedestrian IDF1      IDR       IDP       IDTP      IDFN      IDFP
video_1                                     30.3      19.24     71.272    3575      15006     1441

Count: nguyennhatthang_video1-pedestrian Dets      GT_Dets   IDs       GT_IDs
video_1                                  5016      18581     56        62
```

So sánh các cấu hình đã thử trên video_1 (cùng script chấm):

| Tracker | conf | iou | HOTA | MOTA | IDF1 | Đổi ID |
|---|---|---|---|---|---|---|
| **botsort** (nộp) | 0.1 | 0.5 | 29.5 | **21.0** | 30.3 | 23 |
| botsort | 0.15 | 0.7 | **29.7** | 20.3 | 29.9 | 39 |
| botsort | 0.3 | 0.5 | 29.5 | 19.8 | 29.4 | 25 |
| botsort | 0.5 | 0.5 | 27.2 | 15.3 | 24.6 | 10 |
| strongsort | 0.15 | 0.5 | 29.2 | 19.9 | 32.6 | 110 |
| strongsort | 0.3 | 0.5 | 28.7 | 19.7 | 29.9 | 41 |
| ocsort | 0.3 | 0.5 | 27.5 | 19.8 | 28.7 | 42 |
| deepocsort | 0.3 | 0.5 | 27.4 | 19.8 | 27.8 | 51 |
| bytetrack | 0.3 | 0.5 | 26.9 | 17.3 | 25.7 | 12 |

Chọn `botsort` conf 0.1 thay vì cấu hình HOTA cao nhất (conf 0.15, iou 0.7) vì HOTA chỉ kém 0.14 nhưng MOTA cao hơn và đổi ID ít hơn gần một nửa (23 so với 39).

`video_2` đến `video_5` không có nhãn trong gói lab. Không điền số cho các video đó.

## 3. Phân tích

**video_1 (có nhãn).** Điểm thấp chủ yếu do phát hiện, không phải do tracker: recall chỉ ~24% trong khi precision ~89%, và DetA (19.6) thấp hơn nhiều so với AssA (45.0). Người ở cuối quảng trường quá nhỏ với detector 640 px, nên hạ `conf` từ 0.3 xuống 0.1 là cách tăng điểm hiệu quả nhất: MOTA tăng từ 19.8 lên 21.0, recall từ 21.8% lên 24.1%. BoT-SORT hợp cảnh camera tĩnh, mật độ vừa này vì Re-ID giúp nối lại người sau khi bị che ngắn, trong khi ByteTrack giữ ID gọn (12 lần đổi) nhưng bỏ sót nhiều người hơn hẳn nên HOTA thấp nhất.

**video_3 (chỉ xem bằng mắt).** Camera cầm tay di chuyển, ảnh nhỏ 640×480 và khung hình chậm, nên mỗi người dịch chuyển rất xa giữa hai frame và hình cắt người dùng cho Re-ID chỉ vài chục pixel. Trên video, các tracker có Re-ID (BoT-SORT, StrongSORT, DeepOCSORT) tách cùng một người thành nhiều track ngắn hơn hẳn. OC-SORT dựa vào chuyển động nhưng sửa lỗi Kalman bằng quan sát mới (observation-centric), nên chịu được chuyển động không đều và bị che lâu: track dài nhất, bắt thêm người ở xa. Hạ `conf` xuống 0.15 làm hộp nhấp nháy và sinh hộp giả, nên giữ 0.3.

**video_5 (chỉ xem bằng mắt).** Camera trên xe bus rung lắc làm cả khung hình dịch chuyển, nên các tracker chỉ dựa vào chuyển động dự đoán sai vị trí và mất người. BoT-SORT có bù chuyển động camera (GMC) và Re-ID, nên trên video track dài nhất và ít vụn hơn các tracker có cùng độ phủ. ByteTrack mất cả nhóm người đang qua đường. Người ở giao lộ thường nhỏ và xa nên `conf` 0.15 giúp giữ thêm người mà chưa thấy hộp giả.

**video_2 (chỉ xem bằng mắt).** Cảnh đêm nhìn từ trên cao, người nhỏ và tối. Hạ `conf` xuống 0.1 vừa tăng số người được bắt vừa làm track dài hơn, vì detector không còn bỏ sót người ở vài frame rồi bắt lại với ID mới. Camera tĩnh và người ít bị che lâu nên BoT-SORT giữ ID ổn định hơn StrongSORT.

## 4. Nếu có thêm thời gian

Quét `conf` mịn hơn quanh 0.1–0.2 riêng cho từng video và thử chỉnh ngưỡng bên trong tracker (ngưỡng tạo track mới, số frame giữ track bị mất) như một phần mở rộng. Xem kỹ các frame ở video_2 nơi đám đông bị sót để xác nhận giới hạn nằm ở kích thước ảnh 640 px của detector chứ không phải ở tracker.
