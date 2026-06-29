#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

URL = "https://www.fragrantica.com/perfume/Giorgio-Armani/Emporio-Armani-Stronger-With-You-Intensely-52802.html"
SELECTOR = ".mt-6.space-y-1"
OUTPUT_HTML_PATH = "fragrantica-html-top-notes.html"
DEBUG_IMAGE_PATH = "cloudflare_check_playwright.png"

def wrap_with_style(raw_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica Notes Component</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* ۱. وسط‌چین کردن سراسری و حذف تمام فاصله‌های منبع اصلی عطرها */
        .minimal-container * {{
            text-align: center !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
            box-sizing: border-box !important;
        }}
        
        .minimal-container {{
            direction: ltr !important;
            background-color: #ffffff !important;
        }}
        
        /* ۲. حذف تمام بک‌گراندها و سایه‌های مزاحم */
        .minimal-container div,
        .minimal-container p,
        .minimal-container span,
        .minimal-container a {{
            background-color: transparent !important;
            background: transparent !important;
            box-shadow: none !important;
        }}

        /* رنگ خاکستری متون در حالت عادی */
        .minimal-container,
        .minimal-container div, 
        .minimal-container span, 
        .minimal-container p,
        .minimal-container a {{
            color: #52525B !important;
            text-decoration: none !important;
        }}
        
        /* 🖤 استایل خطوط باریک، ظریف و مشکی مماس با لبه‌های کانتینر */
        .note-section-header {{
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            max-width: 100% !important;
            margin-top: 2rem !important; /* فاصله منطقی با بخش قبلی */
            margin-bottom: 0.5rem !important; /* فاصله کم و شیک تا آیکون‌ها */
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.1em !important;
            color: #18181B !important;
        }}
        
        /* خط سمت چپ: کاملاً مماس با لبه چپ کانتینر */
        .note-section-header::before {{
            content: "" !important;
            flex: 1 !important;
            border-bottom: 1px solid #18181B !important;
            opacity: 0.15 !important;
            margin-right: 15px !important; /* فاصله تا متن تایتل */
            margin-left: 0 !important;    /* چسبیده به لبه کانتینر */
        }}
        
        /* خط سمت راست: کاملاً مماس با لبه راست کانتینر */
        .note-section-header::after {{
            content: "" !important;
            flex: 1 !important;
            border-bottom: 1px solid #18181B !important;
            opacity: 0.15 !important;
            margin-left: 15px !important;  /* فاصله تا متن تایتل */
            margin-right: 0 !important;   /* چسبیده به لبه کانتینر */
        }}
        
        /* حذف مارجین تاپِ تایتل اول برای چسبیدن به سقف کادر */
        .minimal-container .note-section-header:first-of-type {{
            margin-top: 0.5rem !important;
        }}
        
        /* تراز کردن کانتینر اصلی نوت‌ها برای تضمین یکسانی ۱۰۰٪ عرض ردیف‌ها */
        .minimal-container .pyramid-level-container {{
            width: 100% !important;
            max-width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            flex-wrap: wrap !important;
        }}
        
        /* تنظیم فاصله جزئی بین خود آیکون‌های نوت */
        .minimal-container img {{
            margin-bottom: 0.25rem !important;
        }}
        
        /* ✨ حالت هاور فیروزه‌ای اختصاصی شما روی نوت‌ها */
        .minimal-container a:hover,
        .minimal-container a:hover * {{
            color: #43B1A8 !important;
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-4">

    <div class="minimal-container bg-white p-8 rounded-2xl shadow-sm border border-gray-100 w-full max-w-2xl transition-all duration-300 hover:shadow-md">
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
        
        print("Waiting 5 seconds for page load...")
        page.wait_for_timeout(5000)

        page.screenshot(path=DEBUG_IMAGE_PATH)

        print("Processing HTML and synchronizing all line widths...")
        element = page.locator(SELECTOR).first

        if element.count() > 0 and element.is_visible():
            # تزریق کلاس به تایتل‌ها و همزمان یکسان‌سازی عرض تمام کانتینرهای والد
            raw_html = element.evaluate("""el => {
                const tags = Array.from(el.querySelectorAll('div, p, span, b, strong, h4, h5'));
                tags.forEach(node => {
                    const text = node.textContent ? node.textContent.trim().toUpperCase() : '';
                    if (text === 'TOP NOTES' || text === 'MIDDLE NOTES' || text === 'BASE NOTES') {
                        node.className = ''; // پاکسازی کامل کلاس‌های مزاحم قدیمی
                        node.classList.add('note-section-header');
                        
                        // هماهنگ کردن عرض کانتینر بالادستی ردیف برای فیت شدن کامل خطوط با لب کانتینر
                        let parent = node.parentElement;
                        if (parent) {
                            parent.style.setProperty('width', '100%', 'important');
                            parent.style.setProperty('max-width', '100%', 'important');
                            parent.style.setProperty('display', 'flex', 'important');
                            parent.style.setProperty('flex-direction', 'column', 'important');
                            parent.style.setProperty('align-items', 'center', 'important');
                        }
                    }
                });
                return el.outerHTML;
            }""")
            
            final_html = wrap_with_style(raw_html)
            
            with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"🎉 تموم شد! خطوط کاملاً هم‌اندازه، متقارن و تا لب کانتینر فیت شدند → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: المنت پیدا نشد.")

        page.wait_for_timeout(3000) 
        browser.close()

if __name__ == "__main__":
    main()
