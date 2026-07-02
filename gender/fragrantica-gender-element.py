#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time
import re
import urllib.request

URL = "https://www.fragrantica.com/perfume/Giorgio-Armani/Emporio-Armani-Stronger-With-You-Intensely-52802.html"
OUTPUT_HTML_PATH = "fragrantica-gender-element.html"
DEBUG_IMAGE_PATH = "cloudflare_gender_check.png"

def download_tailwind():
    """Download Tailwind CSS JS so the output HTML works offline."""
    url = "https://cdn.tailwindcss.com"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8")
    except Exception as e:
        print(f"⚠️ Could not download Tailwind CSS: {e}")
        return None

def wrap_with_style(card_html, tailwind_js=None):
    if tailwind_js:
        tailwind_tag = f"<script>{tailwind_js}</script>"
    else:
        tailwind_tag = '<script src="https://cdn.tailwindcss.com"></script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica Gender Card - Perfect Color</title>
    {tailwind_tag}
    <style>
        /* استایل پایه مینیمال */
        .minimal-container {{
            direction: ltr !important;
            background-color: #ffffff !important;
            font-family: ui-sans-serif, system-ui, sans-serif;
            width: 100%;
        }}
        
        /* حذف سایه‌ها */
        .minimal-container div,
        .minimal-container p,
        .minimal-container span,
        .minimal-container a {{
            box-shadow: none !important;
        }}

        /* 🎯 اعمال رنگ دقیق #4B5563 روی تمام متون، لایبل‌ها، عنوان و درصدها */
        .minimal-container .tw-perf-card,
        .minimal-container .tw-perf-card h4, 
        .minimal-container .tw-perf-card b,
        .minimal-container .tw-perf-card span,
        .minimal-container .tw-perf-card p,
        .minimal-container .tw-perf-card div {{
            color: #4B5563 !important;
            font-weight: 600 !important; /* ضخامت مناسب برای خوانایی بهتر با این رنگ */
        }}

        /* 🎨 اعمال رنگ دقیق #4B5563 روی لوگو/آیکون جنسیت (SVG) */
        .minimal-container .tw-perf-card svg,
        .minimal-container .tw-perf-card svg path,
        .minimal-container .tw-perf-card svg fill {{
            fill: #4B5563 !important;
            stroke: #4B5563 !important; /* در صورتی که آیکون با استروک رسم شده باشد */
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-6">

    <div class="minimal-container bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-xl transition-all duration-300 hover:shadow-md">
        {card_html}
    </div>

</body>
</html>
"""

def main():
    print("Downloading Tailwind CSS for offline use...")
    tailwind_js = download_tailwind()
    if tailwind_js:
        print(f"✅ Tailwind CSS downloaded ({len(tailwind_js)//1024} KB) - HTML will work offline")
    else:
        print("⚠️ Tailwind not downloaded - HTML will need internet")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900}
        )
        page = context.new_page()

        print(f"Opening: {URL}")
        page.goto(URL, wait_until="load", timeout=60000)
        
        page.wait_for_timeout(3000)

        # 🍪 قبول کردن بنر کوکی
        try:
            if page.locator(".sp_choice_type_11").is_visible(timeout=2000):
                page.locator(".sp_choice_type_11").click()
            else:
                iframe_btn = page.frame_locator("iframe[id^='sp_message_iframe']").locator(".sp_choice_type_11")
                if iframe_btn.is_visible(timeout=2000):
                    iframe_btn.click()
        except Exception:
            pass

        # 🔓 باز کردن اسکرول صفحه
        page.evaluate("""() => {
            document.documentElement.style.setProperty('overflow', 'auto', 'important');
            document.body.style.setProperty('overflow', 'auto', 'important');
        }""")
        page.wait_for_timeout(1000)

        # ⚡ اسکرول نرم برای لود کامل چارت‌ها
        for step in range(12):
            page.evaluate("window.scrollBy(0, 700);")
            page.wait_for_timeout(400)

        page.wait_for_timeout(3000)
        page.screenshot(path=DEBUG_IMAGE_PATH)
        
        extracted_html = page.evaluate("""() => {
            const allCards = Array.from(document.querySelectorAll('.tw-perf-card'));
            if (allCards.length === 0) return null;

            // پیدا کردن کارت جنسیت
            const genderCard = allCards.find(card => {
                const text = card.textContent.toLowerCase();
                return text.includes('unisex') || text.includes('more male') || text.includes('more female');
            });
            
            if (!genderCard) return null;

            // 🎯 کپی گرفتن از کارت برای جلوگیری از دستکاری مجدد توسط Vue.js
            const clone = genderCard.cloneNode(true);

            // ۱. حذف ردیف no vote با حفظ فاصله‌ها
            const elements = Array.from(clone.querySelectorAll('*'));
            elements.forEach(el => {
                if (el.textContent.trim().toLowerCase() === 'no vote') {
                    let current = el;
                    while (current && current.parentElement) {
                        const parentText = current.parentElement.textContent.toLowerCase();
                        if (parentText.includes('unisex') || parentText.includes('male') || parentText.includes('female')) {
                            current.style.visibility = 'hidden';
                            break;
                        }
                        current = current.parentElement;
                    }
                }
            });

            // ۲. حذف کامل متون مربوط به نابینایان (sr-only) برای جلوگیری از تکرار
            const srOnlyElements = clone.querySelectorAll('.sr-only');
            srOnlyElements.forEach(el => el.remove());

            // ۳. حذف تگ‌های مزاحم Vue روی نسخه کلون شده
            const vueTags = clone.querySelectorAll('vue-slider-marks, .vue-slider-marks, vue-slider-rail, .vue-slider-rail');
            vueTags.forEach(el => el.remove());

            return clone.outerHTML;
        }""")

        if extracted_html:
            clean_html = extracted_html
            
            # 🧹 پاکسازی تگ‌ها و کلاس‌های Vue
            clean_html = re.sub(r'<vue-slider-marks.*?>.*?</vue-slider-marks>', '', clean_html, flags=re.DOTALL)
            clean_html = re.sub(r'<vue-slider-rail.*?>.*?</vue-slider-rail>', '', clean_html, flags=re.DOTALL)
            clean_html = clean_html.replace('vue-slider-marks', '')
            clean_html = clean_html.replace('vue-slider-rail', '')
            
            # 🎨 تغییر رنگ دقیق بک‌گراند نوارها به #E5E7EB
            clean_html = clean_html.replace('bg-zinc-200', 'bg-[#E5E7EB]')
            clean_html = clean_html.replace('dark:bg-zinc-700', '') # حذف دارک‌مود برای جلوگیری از تداخل رنگ

            # پاکسازی استایل اینلاین در صورت وجود
            clean_html = clean_html.replace('style="background-color: rgb(229, 231, 235) !important; background-image: none !important;"', '')

            final_html = wrap_with_style(clean_html, tailwind_js)
            with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"🎉 فوق‌العاده! رنگ متون و لوگو با موفقیت به #4B5563 تغییر یافت → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: کارت یافت نشد.")

        browser.close()

if __name__ == "__main__":
    main()
