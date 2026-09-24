# Colemak-Viet

Bố cục bàn phím cho người gõ **tiếng Việt** cả ngày và tiếng Anh phần còn lại.
Nó đi ra từ [Colemak](https://colemak.com) và
[bản mod DH](https://colemakmods.github.io/mod-dh/), rồi dời thêm mười hai phím
nữa — vì cả Colemak lẫn Colemak-DH đều được tối ưu cho tiếng Anh, mà tiếng Việt
gõ qua Telex là một luồng phím hoàn toàn khác.

English: [README.md](README.md)

```
 `   1  2  3  4  5  6  7  8  9  0  -  =
 Tab   q  w  f  g  b     ;  l  u  y  x   [  ]  \
 Caps   a  h  s  t  p     m  n  e  o  i   '
 Shift   j  v  r  c  z     k  d  ,  .  /
```

File dựng sẵn cho macOS, Windows và Linux nằm trong [`dist/`](dist/) —
[cách cài](#cài-đặt).

## Vì sao không dùng thẳng Colemak-DH

Tiếng Việt không được gõ theo cách nó được viết. Với Telex — thứ gần như mọi
người Việt đang dùng — `nhiều` là tám lần bấm, `nhieeuf`, và dấu thanh rơi xuống
cuối âm tiết. Nên tần suất đáng quan tâm là tần suất của *phím bấm*, và nó chẳng
giống tiếng Anh chỗ nào.

Colemak-DH dồn `k`, `h`, `n` lên ngón trỏ phải. Tiếng Việt mở khoảng một phần
tám số từ bằng `kh`, còn `nh` thì ở khắp nơi. Trên corpus OpenSubtitles 50 nghìn
từ tiếng Việt, riêng hai cặp ấy là 30 phần nghìn tổng số lần bấm, và cả hai đều
cùng ngón:

| bố cục | các cặp cùng ngón nặng nhất, tiếng Việt |
|---|---|
| Colemak-DH-angle | `nh` 19,8‰, `kh` 11,0‰, `wc` 5,5‰, `ax` 4,1‰, `nj` 4,1‰ |
| Colemak-Viet | `eu` 3,8‰, `ix` 2,0‰, `xi` 0,7‰, `aj` 0,5‰, `nd` 0,3‰ |

Toàn bộ ý tưởng nằm ở đó. Mọi thứ còn lại chỉ là gỡ mấy cặp ấy ra khỏi một ngón
mà không phá những chỗ Colemak vốn làm đúng.

## Các con số

Tự chạy lại: `./scripts/score-layouts.py --markdown`. Corpus là bảng tần suất
OpenSubtitles với số đếm thật, từ tiếng Việt được phân rã thành phím Telex
trước. Effort thấp là tốt; SFB là tỉ lệ cặp phím cùng ngón.

### Tiếng Việt

| bố cục | effort | SFB | hàng nhà | út phải | út trái | tay trái | đảo tay |
|---|---|---|---|---|---|---|---|
| **Colemak-Viet** | **1,629** | **0,91%** | 61% | 7,2% | 13,8% | 53% | 52% |
| Workman | 1,631 (+0%) | 2,84% | 63% | 5,9% | 11,0% | 54% | 53% |
| Colemak-DH | 1,700 (+4%) | 4,86% | 60% | 10,6% | 11,0% | 50% | 51% |
| Dvorak | 1,719 (+5%) | 3,40% | 67% | 7,6% | 10,8% | 45% | 57% |
| Colemak-DH-angle | 1,724 (+6%) | 5,29% | 60% | 10,6% | 12,4% | 50% | 51% |
| Colemak | 1,747 (+7%) | 4,86% | 66% | 10,6% | 11,0% | 50% | 51% |
| QWERTY | 1,863 (+14%) | 8,30% | 41% | 0,7% | 11,0% | 55% | 52% |

Cặp cùng ngón giảm sáu lần so với Colemak-DH-angle, và ngón út phải — thứ đang
gánh `o`, chữ nặng nhất tiếng Việt, trên Colemak gốc — bớt khoảng một phần ba việc.

### Tiếng Anh, nói thẳng

Tiếng Anh vẫn gõ được, và vẫn hơn QWERTY rất xa. Nhưng bố cục này được tinh
chỉnh trên corpus tiếng Việt, trong hàm mục tiêu không có một chữ tiếng Anh nào,
và điều đó lộ ra đúng chỗ ai cũng đoán được:

| bố cục | effort | SFB | hàng nhà | út phải | út trái | tay trái | đảo tay |
|---|---|---|---|---|---|---|---|
| **Colemak-Viet** | **1,555** | **5,79%** | 67% | 7,3% | 8,1% | 47% | 49% |
| Workman | 1,559 (+0%) | 2,47% | 68% | 7,2% | 7,9% | 50% | 53% |
| Colemak-DH | 1,575 (+1%) | **1,18%** | 67% | 9,1% | 7,9% | 44% | 55% |
| Colemak-DH-angle | 1,584 (+2%) | 1,31% | 67% | 9,1% | 7,9% | 44% | 55% |
| Colemak | 1,602 (+3%) | 1,18% | 71% | 9,1% | 7,9% | 44% | 55% |
| Dvorak | 1,687 (+9%) | 2,36% | 69% | 9,9% | 8,9% | 46% | 69% |
| QWERTY | 1,951 (+25%) | 5,93% | 32% | 1,5% | 7,9% | 54% | 51% |

Effort và hàng nhà thì ngang tầm Colemak. Cặp cùng ngón thì không: 5,79%, gấp
năm lần Colemak-DH và ngang ngửa QWERTY. Ba cặp chiếm phần lớn con số đó —
`yo` (17,5‰), `nd` (10,3‰), `wh` (7,8‰) — vì `o` dời xuống dưới `y`, `d` xuống
dưới `n`, và `h` xuống dưới `w`. Trên một bảng từ tiếng Anh nặng văn viết thay
vì phụ đề phim, tổng SFB còn 4,7%, vẫn gấp khoảng bốn lần Colemak-DH — tức không
phải do chữ *you* quá dày trong thoại phim.

**Vậy nên:** nếu bạn gõ chủ yếu tiếng Việt, đây là bàn phím tốt hơn và cái giá
phải trả cho tiếng Anh là có thật nhưng nhỏ. Nếu bạn gõ chủ yếu tiếng Anh, hãy
dùng [Colemak-DH](https://colemakmods.github.io/mod-dh/) — nó gõ tiếng Anh giỏi
hơn bố cục này mãi mãi.

## Đổi những gì, và vì sao

So với Colemak-DH-angle (`qwfpb jluy; / arstg mneio / xcdvz kh,./`), mười hai
phím dời chỗ:

| đổi | vì sao |
|---|---|
| `h` về hàng nhà trái, chỗ của `r` | giết sạch `kh` và `nh`; `h` chiếm 69‰ số lần bấm tiếng Việt so với 30‰ của `r`, nên nó xứng một phím hàng nhà hơn, và `ho hu ha` trở thành đảo tay |
| `r` xuống hàng dưới trái, chỗ của `d` | Cmd+R vẫn một tay |
| `d` sang ngón trỏ phải, hàng dưới | `dd` (ra `đ`) là lặp phím nên miễn phí, và `d` được ngồi cạnh nguyên âm |
| `c` ↔ `v` | `c` 42‰ nên lên ngón trỏ; `v` 11‰ thì về áp út được. Giết cặp `wc` |
| `p` ↔ `g` | `g` 51‰, phần lớn đến từ `ng` 44‰, không đáng phải trả giá cột giữa |
| `o` ↔ `i` | `o` là chữ nặng nhất tiếng Việt, 131‰. Nó không thể ngồi ngón út |
| `j` xuống góc trái dưới | `j` là dấu nặng; rời ngón trỏ phải thì hết đụng `nj`, `mj`, `hj` |
| `x` lên góc phải trên, chỗ của `;` | `x` là dấu hiếm nhất (5,5% số từ) nên chịu được ngón út; cái giá là cặp `ix` 2,0‰, cặp cùng ngón duy nhất nó thêm vào |
| `;` lên ô trỏ phải hàng trên, chỗ của `j` | ký tự duy nhất bị các phép đổi kia bỏ rơi; tiếng Việt gần như không dùng, và ô ấy là phím đắt nhất bàn phím |

Hai thứ bị giữ chặt, và chúng loại bỏ vài phương án chấm điểm cao hơn:

- **`c v s t r a z` ở lại nửa trái**, để Cmd+C/V/S/T/R/A/Z còn bấm một tay.
  Riêng Cmd+X phải sang tay phải. Bỏ
  ràng buộc này chỉ mua thêm khoảng 2% trong mô hình, đổi lại là mọi phím tắt
  bạn đã thuộc.
- **Năm phím dấu Telex `s f r x j` không bị xếp lại.** Đã duyệt: toàn bộ 55.440
  cách đặt năm dấu lên mười một phím an toàn, chấm trên corpus 117 triệu lần
  bấm, và Telex chuẩn đã nằm trong top 6%. Phương án tốt nhất chỉ hơn 1–3% tuỳ
  mô hình effort — tức nhiễu — mà cái giá thì trả mỗi ngày trên mọi bàn phím
  khác trong đời.

`z` giữ vị trí angle mod ở phím B: gần như 0‰ trong tiếng Việt, và ở đó
Cmd+Z (hoàn tác) vẫn bấm một tay.

Chi tiết hơn, gồm cả bảng xếp hạng với 28 bố cục khác và những phương án đã bị
loại: [docs/comparison.md](docs/comparison.md).

## Cài đặt

Bạn cần hai thứ: bố cục này, và một bộ gõ Telex. Chúng độc lập với nhau — bộ gõ
đọc *ký tự* chứ không đọc vị trí phím, nên Telex không phải chỉnh gì để chạy với
bàn phím đã đổi chỗ.

### macOS

Bảng phím này đang được dùng hằng ngày trên macOS 26. Tải repo về, rồi:

```bash
./scripts/build-layouts.py --install
```

hoặc tự chép `dist/macos/Colemak-Viet.bundle` vào `~/Library/Keyboard Layouts/`.
**Đăng xuất rồi đăng nhập lại** — macOS không nhận một bundle bố cục mới thêm
vào trước lúc đó — rồi thêm nó ở System Settings → Keyboard → Input Sources.

Muốn kiểm tra hệ thống có đang phục vụ đúng thứ trong repo này không:

```bash
swift scripts/verify-macos-layout.swift
```

Bộ gõ Telex: dùng bộ gõ tiếng Việt có sẵn của macOS, hoặc
[VTX](https://github.com/xkhanhs/vtx), hoặc bất kỳ bộ gõ Telex nào khác.

### Windows — chưa thử

`dist/windows/colemak-viet.klc` là file nguồn cho
[MSKLC](https://learn.microsoft.com/en-us/globalization/windows-keyboard-layouts),
công cụ biên dịch nó thành bộ cài. Mở lên, build, cài, rồi chọn bố cục ở
Settings → Time & Language → Language & region.

Chưa ai chạy thử trên Windows. Nếu nó sai, xin
[mở issue](../../issues) hoặc gửi PR — chỗ cần sửa là
`scripts/build-layouts.py`, không phải file đã sinh ra.

Bộ gõ Telex trên Windows: [Unikey](https://www.unikey.org) hoặc
[EVKey](https://evkeyvn.com).

### Linux — chưa thử

`dist/linux/colemak_viet` là file symbols của XKB:

```bash
sudo cp dist/linux/colemak_viet /usr/share/X11/xkb/symbols/
setxkbmap colemak_viet
```

Trên Wayland thì cùng file ấy được đọc qua phần cài đặt bàn phím của desktop chứ
không qua `setxkbmap`; trên GNOME có thể phải khai báo nó trong
`/usr/share/X11/xkb/rules/evdev.xml` thì nó mới hiện ra trong danh sách.

Cũng chưa thử. Rất hoan nghênh issue và PR.

Bộ gõ Telex trên Linux: [ibus-bamboo](https://github.com/BambooEngine/ibus-bamboo).

### Karabiner-Elements (macOS, không cần thêm input source)

`dist/karabiner/colemak-viet.json` đổi mười hai phím ấy đè lên bố cục bạn đang
dùng. Chép vào `~/.config/karabiner/assets/complex_modifications/` rồi bật rule
lên. Hữu ích khi trên máy có thứ gì đó đang ghim cứng vào một input source cụ
thể.

## Học mất bao lâu

Khoảng mười lăm giờ luyện là gõ được 50 wpm, đi lên từ Colemak-DH-angle. Đó là
trải nghiệm của một người, không phải một nghiên cứu — và nó là phép đo thật duy
nhất trong repo này, thứ duy nhất không phải mô hình. Đi lên từ QWERTY thì lâu
hơn, và phần lớn thời gian ấy là học Colemak chứ không phải học mười hai phím mà
bố cục này thêm vào.

Hai trong số các thay đổi — `d`↔`h` và `c`↔`v` — đã ăn khoảng 70% toàn bộ lợi
ích, nên có thể học chúng trước nếu muốn chia nhỏ ra.

## Dựng lại

```bash
./scripts/build-layouts.py          # layout.json → dist/
./scripts/test-layouts.py           # đọc ngược cả bốn file, đối chiếu
./scripts/build-layouts.py --check  # báo lỗi nếu dist/ đã cũ
./scripts/score-layouts.py          # các bảng ở trên
```

[`layout.json`](layout.json) là chỗ duy nhất các chữ cái được ghi ra. Mọi thứ
trong `dist/` đều sinh từ nó, nên một thay đổi ở đó hoặc tới được cả bốn nền
tảng, hoặc không tới nền tảng nào.

## Ghi công

- **Colemak**, của Shai Coleman — bố cục mà cái này là hậu duệ.
- **Colemak-DH** và **angle mod**, của Stevep99 và cộng đồng
  [ColemakMods](https://github.com/ColemakMods/mod-dh) — phần việc ở hàng nhà và
  hàng dưới mà bố cục này lấy làm điểm xuất phát.
- Các phép đo và phần thiết kế ban đầu được làm trong
  [keybear](https://github.com/xkhanhs/keybear) (một app luyện gõ) và
  [VTX](https://github.com/xkhanhs/vtx) (bộ gõ Telex cho macOS).

Colemak-Viet là một bản mod độc lập. Không có gì ở đây được hai dự án kia bảo
chứng, và sai sót nào trong đó là của repo này.

## Giấy phép

[MIT](LICENSE). Các file bố cục được `scripts/build-layouts.py` dựng từ đầu;
không có file nào của dự án bố cục khác được phát hành lại ở đây.
