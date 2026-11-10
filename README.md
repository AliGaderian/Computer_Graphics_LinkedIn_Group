# Computer Graphics LinkedIn Group

کد کامل و تست‌شدهٔ مقاله‌های سری «گرافیک کامپیوتری». هر مقاله فقط شبه‌کد دارد و پیاده‌سازی پایتون در پوشهٔ همان مقاله است. مقاله‌ها یکی‌یکی منتشر می‌شوند و پوشهٔ هر مقاله هم همزمان با آن به مخزن اضافه می‌شود.

## مقاله‌ها

| مقاله | پوشه | نوت‌بوک محلی | نوت‌بوک Colab |
|---|---|---|---|
| ۱. رسم خط: DDA، برزنهام و ضددندانه‌شدن (وو) | [article1_line_drawing](article1_line_drawing) | [local](article1_line_drawing/local/line_drawing.ipynb) | [colab](article1_line_drawing/colab/line_drawing.ipynb) |

## ساختار

هر مقاله یک پوشهٔ مستقل است و می‌شود جدا برداشت و اجرا کرد:

```
Computer_Graphics_LinkedIn_Group/
├── article1_line_drawing/
│   ├── lines.py              کد مقاله
│   ├── lines_plots.py        رسم نمودار
│   ├── notebook_cells.py     متن نوت‌بوک‌ها (برای ساختشان)
│   ├── tests/                تست‌ها
│   ├── figures/              تصویر مقاله
│   ├── local/                نوت‌بوک برای اجرای محلی
│   └── colab/                همان نوت‌بوک برای Google Colab
├── scripts/                  ساخت تصویرها و نوت‌بوک‌ها
├── conftest.py, pytest.ini   تنظیم تست
└── requirements*.txt
```

## دو راه اجرا

- **محلی:** پوشهٔ `local/` هر مقاله. نوت‌بوک را با Jupyter باز کنید؛ سلول اول پوشهٔ کد را پیدا می‌کند.
- **Google Colab:** پوشهٔ `colab/` هر مقاله. بالای هر نوت‌بوک دکمهٔ «Open in Colab» هست. سلول اول مخزن را clone می‌کند و NumPy و matplotlib را دوباره نصب نمی‌کند.

دو نسخه فقط در سلول اول (و دکمهٔ Colab) فرق دارند و هر دو با `scripts/make_notebooks.py` از یک منبع ساخته می‌شوند. خروجی‌ها در فایل ذخیره شده‌اند، پس در GitHub بدون اجرا هم دیده می‌شوند.

> دکمهٔ Colab فقط وقتی کار می‌کند که مخزن عمومی باشد و فایل‌ها روی شاخهٔ `main` push شده باشند. اگر نام مخزن عوض شد، `python scripts/make_notebooks.py --repo <owner>/<name>` را دوباره اجرا کنید.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt          # فقط اجرای کد
pip install -r requirements-dev.txt      # تست و ساخت نوت‌بوک‌ها
```

## Run the tests

```bash
python -m pytest
```

## Regenerate the figures and notebooks

```bash
python scripts/make_figures.py
python scripts/make_notebooks.py
```

هر دو اسکریپت همهٔ پوشه‌های `article*` موجود را پردازش می‌کنند. با `--article article1_line_drawing` فقط یکی ساخته می‌شود. کد رسم نمودارها (`*_plots.py`) فقط شکل برمی‌گرداند و backend را عوض نمی‌کند، پس در Colab هم نمایش داده می‌شود.

## Notes and limits

- نسخهٔ Colab در خود Colab اجرا نشده است؛ نسخهٔ محلی اجرا و خروجی‌ها ذخیره شده‌اند.
- محدودیت‌های هر الگوریتم در README همان مقاله آمده است.

## License

[MIT](LICENSE) © 2026 Ali Gaderian (علی قادریان). مجوز برای کد و نوت‌بوک‌های این مخزن است. منبع مقاله‌ها جزوهٔ درس گرافیک کامپیوتری است.
