#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

URL = "https://www.fragrantica.com/perfume/Giorgio-Armani/Emporio-Armani-Stronger-With-You-Intensely-52802.html"
OUTPUT_HTML_PATH = "fragmentia-html-scraper-seasons.html"
DEBUG_IMAGE_PATH = "cloudflare_check_playwright.png"

def wrap_with_style(raw_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica - When To Wear</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* تکست‌های داخل مربع‌ها و لیبل‌ها کاملاً وسط‌چین شوند */
        .minimal-container * {{
            text-align: center !important;
        }}
        /* حفظ جهت طبیعی افقی (چپ به راست) برای نمودارها و باکس‌های فصول */
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
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        page = context.new_page()

        print(f"Opening: {URL}")
        page.goto(URL, wait_until="load", timeout=60000)
        
        print("Waiting 5 seconds for charts to render...")
        page.wait_for_timeout(5000)

        # گرفتن عکس برای اطمینان از رد شدن کلاودفلر
        page.screenshot(path=DEBUG_IMAGE_PATH)

        print("Searching for 'When To Wear' section...")
        
        # 🟢 اجرای یک اسکریپت جاوااسکریپت هوشمند درون مرورگر برای پیدا کردن کادر دقیق "When To Wear"
        raw_html = page.evaluate("""() => {
            // پیدا کردن المانی که متن درون آن دقیقاً When To Wear است
            const targetHeader = Array.from(document.querySelectorAll('*')).find(
                el => el.textContent && el.textContent.trim() === 'When To Wear'
            );
            
            if (targetHeader) {
                // پیدا کردن نزدیک‌ترین کادر مادر (کارت ریتینگ فصول)
                const container = targetHeader.closest('.tw-rating-card') || targetHeader.parentElement;
                return container.outerHTML;
            }
            return null;
        }""")

        if raw_html:
            final_html = wrap_with_style(raw_html)
            with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"🎉 فوق‌العاده! بخش When To Wear با موفقیت استخراج و ذخیره شد → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: بخش 'When To Wear' در صفحه یافت نشد. عکس دباگ را بررسی کنید.")

        page.wait_for_timeout(3000) 
        browser.close()

if __name__ == "__main__":
    main()
