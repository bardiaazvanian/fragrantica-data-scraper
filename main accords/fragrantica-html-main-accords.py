#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

URL = "https://www.fragrantica.com/perfume/Giorgio-Armani/Emporio-Armani-Stronger-With-You-Intensely-52802.html"
TARGET_CLASSES = ["flex", "flex-col", "w-full"]
OUTPUT_HTML_PATH = "fragrantica-html-main-accords.html"

def wrap_with_style(raw_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica Minimal Component</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* 🟢 فقط متن‌ها وسط‌چین می‌شن، بدون اینکه ساختار افقی مربع‌ها خراب بشه */
        .minimal-container * {{
            text-align: center !important;
        }}
        /* حفظ جهت چپ به راست برای ساختار سایت */
        .minimal-container {{
            direction: ltr !important;
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">

    <div class="minimal-container bg-white p-8 rounded-2xl shadow-sm border border-gray-100 w-full max-w-3xl transition-all duration-300 hover:shadow-md">
        {raw_html}
    </div>

</body>
</html>
"""

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        print(f"Opening: {URL}")
        page.goto(URL, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(3000)

        for sel in ["#didomi-notice-agree-button", "[aria-label='Accept']"]:
            try:
                btn = page.locator(sel)
                if btn.is_visible(timeout=2000):
                    btn.click()
                    page.wait_for_timeout(500)
            except Exception:
                pass

        all_elements = page.query_selector_all("*")
        matched = []
        for el in all_elements:
            el_classes = el.get_attribute("class") or ""
            el_class_set = set(el_classes.split())
            if all(c in el_class_set for c in TARGET_CLASSES):
                matched.append(el)

        if matched:
            element = matched[0]
            raw_html = element.evaluate("el => el.outerHTML")
            final_html = wrap_with_style(raw_html)
            
            with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
                
            print(f"✅ فایل شیک و مینیمال ذخیره شد → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: المنت پیدا نشد.")

        page.wait_for_timeout(2000) 
        browser.close()

if __name__ == "__main__":
    main()
