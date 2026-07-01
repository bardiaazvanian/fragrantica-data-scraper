#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import os
import re
import urllib.request

URL = "https://www.fragrantica.com/perfume/Dior/Dior-Homme-Intense-2011-13016.html"
SELECTOR = ".mt-6.space-y-1"
OUTPUT_HTML_PATH = "fragrantica-html-top-notes.html"
DEBUG_IMAGE_PATH = "cloudflare_check_playwright.png"
NOTE_IMAGES_DIR = "note_images"

def wrap_with_style(raw_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica Notes Component</title>
    <style>
        /* Tailwind utility replacements for offline use */
        *, ::before, ::after {{ box-sizing: border-box; }}
        .bg-gray-50 {{ background-color: #f9fafb; }}
        .min-h-screen {{ min-height: 100vh; }}
        .flex {{ display: flex; }}
        .flex-col {{ flex-direction: column; }}
        .flex-wrap {{ flex-wrap: wrap; }}
        .items-center {{ align-items: center; }}
        .items-end {{ align-items: flex-end; }}
        .justify-center {{ justify-content: center; }}
        .p-4 {{ padding: 1rem; }}
        .p-8 {{ padding: 2rem; }}
        .px-2 {{ padding-left: 0.5rem; padding-right: 0.5rem; }}
        .py-3 {{ padding-top: 0.75rem; padding-bottom: 0.75rem; }}
        .mt-6 {{ margin-top: 1.5rem; }}
        .mt-1\\.5 {{ margin-top: 0.375rem; }}
        .mx-auto {{ margin-left: auto; margin-right: auto; }}
        .bg-white {{ background-color: #ffffff; }}
        .rounded-2xl {{ border-radius: 1rem; }}
        .rounded-md {{ border-radius: 0.375rem; }}
        .shadow-sm {{ box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }}
        .shadow-xs {{ box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.03); }}
        .border {{ border-width: 1px; border-style: solid; }}
        .border-gray-100 {{ border-color: #f3f4f6; }}
        .w-full {{ width: 100%; }}
        .max-w-md {{ max-width: 28rem; }}
        .max-w-xl {{ max-width: 36rem; }}
        .max-w-2xl {{ max-width: 42rem; }}
        .transition-all {{ transition-property: all; transition-timing-function: cubic-bezier(0.4,0,0.2,1); }}
        .transition-colors {{ transition-property: color, background-color, border-color; transition-timing-function: cubic-bezier(0.4,0,0.2,1); }}
        .duration-200 {{ transition-duration: 200ms; }}
        .duration-300 {{ transition-duration: 300ms; }}
        .ease-out {{ transition-timing-function: cubic-bezier(0,0,0.2,1); }}
        .relative {{ position: relative; }}
        .absolute {{ position: absolute; }}
        .inset-x-0 {{ left: 0; right: 0; }}
        .top-1\\/2 {{ top: 50%; }}
        .h-px {{ height: 1px; }}
        .text-center {{ text-align: center; }}
        .text-\\[11px\\] {{ font-size: 11px; }}
        .font-medium {{ font-weight: 500; }}
        .text-zinc-600 {{ color: #52525b; }}
        .whitespace-nowrap {{ white-space: nowrap; }}
        .ring-1 {{ box-shadow: 0 0 0 1px var(--ring-color, rgba(161,161,170,0.2)); }}
        .ring-zinc-200\\/20 {{ --ring-color: rgba(228,228,231,0.2); }}
        .space-y-1 > * + * {{ margin-top: 0.25rem; }}
        .bg-gradient-to-r {{ background-image: linear-gradient(to right, var(--tw-gradient-stops)); }}
        .from-transparent {{ --tw-gradient-from: transparent; --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to, transparent); }}
        .via-zinc-300\\/50 {{ --tw-gradient-stops: var(--tw-gradient-from), rgba(212,212,216,0.5), var(--tw-gradient-to, transparent); }}
        .to-transparent {{ --tw-gradient-to: transparent; }}
        .group:hover .group-hover\\:scale-110 {{ transform: scale(1.1); }}
        .group:hover .group-hover\\:shadow-md {{ box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }}
        .group:hover .group-hover\\:ring-teal-400\\/40 {{ --ring-color: rgba(45,212,191,0.4); box-shadow: 0 0 0 1px var(--ring-color); }}
        .group:hover .group-hover\\:text-teal-600 {{ color: #0d9488; }}
        .hover\\:shadow-md:hover {{ box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }}
        @media (min-width: 640px) {{ .sm\\:text-sm {{ font-size: 0.875rem; line-height: 1.25rem; }} }}
    </style>
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

def download_note_images(html):
    """Download all note images from fimgs.net and replace URLs with local paths."""
    os.makedirs(NOTE_IMAGES_DIR, exist_ok=True)
    img_urls = re.findall(r'https://fimgs\.net/mdimg/sastojci/(t\.\d+\.jpg)', html)
    for filename in set(img_urls):
        local_path = os.path.join(NOTE_IMAGES_DIR, filename)
        if not os.path.exists(local_path):
            url = f"https://fimgs.net/mdimg/sastojci/{filename}"
            print(f"Downloading {url}...")
            urllib.request.urlretrieve(url, local_path)
    return html.replace("https://fimgs.net/mdimg/sastojci/", f"{NOTE_IMAGES_DIR}/")

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
        
        # ۱. بررسی فوری کوکی بلافاصله پس از لود اولیه صفحه (قبل از هر کار دیگری)
        print("Checking for cookie banner immediately...")
        try:
            # سلکتور دقیق کلاس‌های ارسالی شما به فرم CSS Selector استاندارد
            cookie_selector = ".message-component.message-button.no-children.focusable.sp_choice_type_11"
            
            # کمی مکس برای رندر شدن لایه‌های حریم خصوصی وب‌سایت
            page.wait_for_timeout(2000)
            
            # پیدا کردن المنت در صورتی که داخل آی‌فریم اختصاصی Sourcepoint باشد
            cookie_inside_iframe = page.frame_locator("iframe[id^='sp_message_iframe']").locator(cookie_selector)
            # پیدا کردن المنت در صفحه اصلی (محض احتیاط)
            cookie_on_page = page.locator(cookie_selector)
            
            if cookie_inside_iframe.first.is_visible():
                cookie_inside_iframe.first.click()
                print("✅ Cookies ACCEPTED from iframe.")
                page.wait_for_timeout(1000)
            elif cookie_on_page.first.is_visible():
                cookie_on_page.first.click()
                print("✅ Cookies ACCEPTED from main page.")
                page.wait_for_timeout(1000)
            else:
                print("No cookie banner detected immediately.")
        except Exception as e:
            print(f"Cookie check finished with notice: {e}")

        # ۲. ادامه‌ی روند اسکرول برای لود شدن کامل محتوای اصلی نوت‌ها
        print("Auto-scrolling page...")
        for i in range(4):
            page.evaluate(f"window.scrollBy(0, 400)")
            page.wait_for_timeout(500)
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(2000)

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
            final_html = download_note_images(final_html)
            
            with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"🎉 تموم شد! خطوط کاملاً هم‌اندازه، متقارن و تا لب کانتینر فیت شدند → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: المنت پیدا نشد.")

        page.wait_for_timeout(3000) 
        browser.close()

if __name__ == "__main__":
    main()
