"""Notebook cells for article1_line_drawing (used by scripts/make_notebooks.py)."""
from notebook_tools import code, md

TITLE = 'رسم خط: DDA، برزنهام و وو'
MODULE = 'lines'        # code module that marks this article's folder
FILE_NAME = 'line_drawing'

ITEMS = [
    md("""
# رسم خط روی پیکسل‌ها: DDA، برزنهام و وو

نوت‌بوک همراه مقالهٔ ۱ از سری گرافیک کامپیوتری. کد کامل در `lines.py` است و اینجا قدم‌به‌قدم اجرا می‌شود.
"""),
    code("""
import numpy as np
import matplotlib.pyplot as plt

from lines import bresenham, dda, rasterize, rasterize_wu, wu_line
"""),
    md("""
## DDA

روی محور بلندتر یک پیکسل یک پیکسل جلو می‌رویم و مختصات دیگر را با یک گام اعشاری جمع می‌کنیم.
"""),
    code("""
print(dda(1, 1, 8, 6))
"""),
    md("""
## برزنهام

فقط عدد صحیح. برای همین خط، همان پیکسل‌های DDA انتخاب می‌شوند.
"""),
    code("""
points = bresenham(1, 1, 8, 6)
print(points)
assert points == dda(1, 1, 8, 6)   # same pixels for this particular line
"""),
    code("""
grid = rasterize(points, (8, 10))
plt.imshow(grid, origin="lower", cmap="gray_r")
plt.title("Bresenham (1,1) -> (8,6)")
plt.show()
"""),
    md("""
## خطای جمع اعشاری در DDA

DDA در هر گام یک عدد اعشاری جمع می‌کند و خطای گردکردن با تعداد گام‌ها روی هم جمع می‌شود. با `float32` این خطا دیدنی است. برزنهام این منبع خطا را ندارد، چون فقط عدد صحیح به کار می‌برد.
"""),
    code("""
step, n = np.float32(0.1), 100_000
total = np.float32(0.0)
for _ in range(n):
    total += step

print("sum of 100000 steps of 0.1 in float32:", float(total))
print("exact value:", n * 0.1)
print("accumulated error:", abs(float(total) - n * 0.1))
"""),
    md("""
## ضددندانه‌شدن به روش وو

شدت روشنایی بین دو پیکسل مجاور تقسیم می‌شود. این نسخه ساده است: `x0 < x1` و شیب بین ۰ و ۱.
"""),
    code("""
samples = wu_line(1, 1, 10, 6)
print([(x, y, round(a, 2)) for x, y, a in samples[:6]])
"""),
    code("""
hard = rasterize(bresenham(1, 1, 10, 6), (9, 12))
soft = rasterize_wu(samples, (9, 12))

fig, ax = plt.subplots(1, 2, figsize=(9, 4))
ax[0].imshow(hard, origin="lower", cmap="gray_r", vmin=0, vmax=1)
ax[0].set_title("Bresenham")
ax[1].imshow(soft, origin="lower", cmap="gray_r", vmin=0, vmax=1)
ax[1].set_title("Wu")
plt.show()
"""),
    md("""
## تمرین

- خط دیگری انتخاب کنید (مثلاً با شیب تند یا منفی) و خروجی `bresenham` را با `dda` مقایسه کنید.
- `wu_line` را طوری تغییر دهید که شیب بیشتر از ۱ را هم پوشش دهد.
"""),
]
