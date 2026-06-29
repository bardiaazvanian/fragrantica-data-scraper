#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import re
from pathlib import Path

# 🎯 ذخیره فایل در پوشه فعلی
SCRIPT_DIR = Path(__file__).parent.resolve()

URL = "https://www.fragrantica.com/perfume/Creed/Aventus-9828.html"
OUTPUT_HTML_PATH = SCRIPT_DIR / "performance_cards_final.html"
DEBUG_IMAGE_PATH = SCRIPT_DIR / "cloudflare_perf_check.png"

def wrap_with_style(card_html):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fragrantica Performance Cards - Perfect</title>
    <script src="https://cdn.tailwindcss.com"></script>
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

        /* 🎯 اعمال رنگ دقیق #4B5563 روی تمام متون */
        .minimal-container .tw-perf-card,
        .minimal-container .tw-perf-card h4, 
        .minimal-container .tw-perf-card b,
        .minimal-container .tw-perf-card span,
        .minimal-container .tw-perf-card p,
        .minimal-container .tw-perf-card div {{
            color: #4B5563 !important;
            font-weight: 600 !important; 
        }}

        /* 🎨 اعمال رنگ دقیق #4B5563 روی آیکون‌ها */
        .minimal-container .tw-perf-card svg,
        .minimal-container .tw-perf-card svg path,
        .minimal-container .tw-perf-card svg fill {{
            fill: #4B5563 !important;
            stroke: #4B5563 !important; 
        }}

        /* 🎨 استایل نوارهای جایگزین شده برای رندر صحیح و آفلاین */
        .custom-track {{
            width: 100%;
            height: 8px;
            background-color: #E5E7EB;
            border-radius: 999px;
            position: relative;
            overflow: hidden;
            margin-top: 6px;
        }}
        .custom-fill {{
            height: 100%;
            border-radius: 999px;
            position: absolute;
            left: 0;
            top: 0;
            transition: width 0.5s ease-in-out;
        }}
    </style>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center p-6">

    <div class="minimal-container bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-4xl transition-all duration-300 hover:shadow-md">
        {card_html}
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
        
        page.wait_for_timeout(3000)

        # 🍪 قبول کردن بنر کوکی (نسخه کامل شامل ایفریم)
        try:
            cookie_selector = ".message-component.message-button.no-children.focusable.sp_choice_type_11"
            if page.locator(cookie_selector).is_visible(timeout=2000):
                page.locator(cookie_selector).click()
            else:
                for frame in page.frames:
                    iframe_btn = frame.locator(cookie_selector).first
                    if iframe_btn.is_visible(timeout=1500):
                        iframe_btn.click()
                        break
        except Exception:
            pass

        # 🔓 حذف لایه تاریک کوکی و باز کردن اسکرول
        page.evaluate("""() => {
            const overlay = document.querySelector('[id^="sp_message_container"]');
            if (overlay) overlay.remove();
            document.documentElement.style.setProperty('overflow', 'auto', 'important');
            document.body.style.setProperty('overflow', 'auto', 'important');
        }""")
        page.wait_for_timeout(1000)

        # ⚡ اسکرول نرم برای لود کامل چارت‌ها
        for step in range(12):
            page.evaluate("window.scrollBy(0, 700);")
            page.wait_for_timeout(400)

        page.wait_for_timeout(3000)
        page.screenshot(path=str(DEBUG_IMAGE_PATH))
        
        extracted_html = page.evaluate("""() => {
            const allCards = Array.from(document.querySelectorAll('.tw-perf-card'));
            if (allCards.length === 0) return null;

            // 🎯 پیدا کردن دقیق دو کلاس مدنظر شما (ماندگاری و پخش بو)
            const longevityCard = allCards.find(card => card.className.includes('to-sky'));
            const sillageCard = allCards.find(card => card.className.includes('to-violet'));
            
            if (!longevityCard && !sillageCard) return null;

            // ساخت یک کانتینر گرید (Grid) برای قرار دادن دو کارت دقیقاً کنار هم مثل عکس
            let combinedHtml = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">';

            [longevityCard, sillageCard].forEach(card => {
                if (card) {
                    const clone = card.cloneNode(true);

                    // ۱. مخفی کردن ردیف no vote بدون به هم ریختن چیدمان
                    const elements = Array.from(clone.querySelectorAll('*'));
                    elements.forEach(el => {
                        if (el.textContent.trim().toLowerCase() === 'no vote') {
                            let current = el;
                            while (current && current.parentElement) {
                                const parentText = current.parentElement.textContent.toLowerCase();
                                if (parentText.includes('longevity') || parentText.includes('sillage')) {
                                    current.style.display = 'none';
                                    break;
                                }
                                current = current.parentElement;
                            }
                        }
                    });

                    // ۲. حذف کامل متون مربوط به نابینایان (sr-only)
                    clone.querySelectorAll('.sr-only').forEach(el => el.remove());

                    // ۳. 🎯 حل مشکل نوارهای Vue: استخراج درصدها و جایگزینی با دیو خالص HTML
                    const sliders = clone.querySelectorAll('.vue-slider, [class*="vue-slider"]');
                    sliders.forEach(slider => {
                        const process = slider.querySelector('.vue-slider-process');
                        let width = '0%';
                        if (process && process.style.width) {
                            width = process.style.width;
                        }

                        // انتخاب رنگ سبز آبی (Teal) دقیقاً مشابه عکس ارسالی شما برای پر شدن نوارها
                        let barColor = '#009587'; 

                        const track = document.createElement('div');
                        track.className = 'custom-track';
                        
                        const fill = document.createElement('div');
                        fill.className = 'custom-fill';
                        fill.style.width = width;
                        fill.style.backgroundColor = barColor;
                        
                        track.appendChild(fill);
                        slider.replaceWith(track);
                    });

                    combinedHtml += clone.outerHTML;
                }
            });

            combinedHtml += '</div>';
            return combinedHtml;
        }""")

        if extracted_html:
            clean_html = extracted_html
            
            # 🧹 پاکسازی تگ‌های باقیمانده Vue
            clean_html = re.sub(r'<vue-slider-marks.*?>.*?</vue-slider-marks>', '', clean_html, flags=re.DOTALL)
            clean_html = re.sub(r'<vue-slider-rail.*?>.*?</vue-slider-rail>', '', clean_html, flags=re.DOTALL)
            clean_html = clean_html.replace('vue-slider-marks', '')
            clean_html = clean_html.replace('vue-slider-rail', '')

            final_html = wrap_with_style(clean_html)
            
            with open(str(OUTPUT_HTML_PATH), "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"🎉 فوق‌العاده! هر دو کارت پرفورمنس با موفقیت استخراج و کنار هم قرار گرفتند → {OUTPUT_HTML_PATH}")
        else:
            print("❌ خطا: کارت‌های ماندگاری (to-sky) و پخش بو (to-violet) یافت نشدند.")

        browser.close()

if __name__ == "__main__":
    main()
