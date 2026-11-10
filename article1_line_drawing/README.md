# مقالهٔ ۱: رسم خط روی پیکسل‌ها

DDA، برزنهام و ضددندانه‌شدن به روش وو.

| فایل | محتوا |
|---|---|
| `lines.py` | `dda`، `bresenham`، `wu_line`، `rasterize`، `rasterize_wu` |
| `lines_plots.py` | `lines_figure()`: برزنهام در کنار وو |
| `tests/test_lines.py` | تست‌ها |
| `figures/lines_bresenham_vs_wu.png` | تصویر مقاله |
| `local/line_drawing.ipynb` | نوت‌بوک محلی |
| `colab/line_drawing.ipynb` | نوت‌بوک Colab |

```python
from lines import bresenham
print(bresenham(1, 1, 8, 6))   # [(1,1),(2,2),(3,2),(4,3),(5,4),(6,5),(7,5),(8,6)]
```

## محدودیت‌ها

- `dda` در هر قدم یک جمع اعشاری دارد و خطای گردکردن با طول خط جمع می‌شود (تست `test_float32_increments_accumulate_error`). `bresenham` فقط عدد صحیح دارد؛ ضرب در ۲ فقط کسر ۰٫۵ را حذف می‌کند.
- `wu_line` نسخهٔ ساده است: `x0 < x1`، شیب بین ۰ و ۱، بدون مدیریت جداگانهٔ نقاط ابتدا و انتها و بدون تصحیح گاما.
