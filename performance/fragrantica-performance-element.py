#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

URL = "https://www.fragrantica.com/perfume/Creed/Aventus-9828.html"
OUTPUT_HTML_PATH = SCRIPT_DIR / "performance_cards_final.html"
DEBUG_IMAGE_PATH = SCRIPT_DIR / "cloudflare_perf_check.png"

OFFLINE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.bg-gray-50 { background-color: #f9fafb; }
.bg-white { background-color: #ffffff; }
.min-h-screen { min-height: 100vh; }
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.flex-1 { flex: 1 1 0%; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
.gap-8 { gap: 2rem; }
.gap-1\\.5 { gap: 0.375rem; }
.w-full { width: 100%; }
.w-8 { width: 2rem; }
.w-9 { width: 2.25rem; }
.w-20 { width: 5rem; }
.h-8 { height: 2rem; }
.h-full { height: 100%; }
.h-2\\.5 { height: 0.625rem; }
.max-w-4xl { max-width: 56rem; }
.min-w-\\[40px\\] { min-width: 40px; }
.shrink-0 { flex-shrink: 0; }
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.p-8 { padding: 2rem; }
.mt-1 { margin-top: 0.25rem; }
.mt-3 { margin-top: 0.75rem; }
.space-y-2 > * + * { margin-top: 0.5rem; }
.text-xs { font-size: 0.75rem; line-height: 1rem; }
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-\\[10px\\] { font-size: 10px; }
.font-medium { font-weight: 500; }
.text-right { text-align: right; }
.text-zinc-500 { color: #71717a; }
.text-zinc-600 { color: #52525b; }
.uppercase { text-transform: uppercase; }
.tracking-wide { letter-spacing: 0.025em; }
.line-clamp-1 { overflow: hidden; display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1; }
.bg-zinc-200 { background-color: #e4e4e7; }
.rounded-full { border-radius: 9999px; }
.rounded-2xl { border-radius: 1rem; }
.overflow-hidden { overflow: hidden; }
.cursor-pointer { cursor: pointer; }
.border { border-width: 1px; border-style: solid; }
.border-gray-100 { border-color: #f3f4f6; }
.shadow-sm { box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
.transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
.duration-300 { transition-duration: 300ms; }
.hover\\:shadow-md:hover { box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); }

@media (min-width: 640px) {
    .sm\\:gap-2 { gap: 0.5rem; }
    .sm\\:w-11 { width: 2.75rem; }
    .sm\\:w-24 { width: 6rem; }
    .sm\\:text-xs { font-size: 0.75rem; line-height: 1rem; }
    .sm\\:text-sm { font-size: 0.875rem; line-height: 1.25rem; }
}
@media (min-width: 768px) {
    .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (min-width: 1024px) {
    .lg\\:w-28 { width: 7rem; }
}

.minimal-container {
    direction: ltr !important;
    background-color: #ffffff !important;
    font-family: ui-sans-serif, system-ui, sans-serif;
    width: 100%;
}
.minimal-container div,
.minimal-container p,
.minimal-container span,
.minimal-container a {
    box-shadow: none !important;
}
.minimal-container .tw-perf-card,
.minimal-container .tw-perf-card h4,
.minimal-container .tw-perf-card b,
.minimal-container .tw-perf-card span,
.minimal-container .tw-perf-card p,
.minimal-container .tw-perf-card div {
    color: #4B5563 !important;
    font-weight: 600 !important;
}
.minimal-container .tw-perf-card svg,
.minimal-container .tw-perf-card svg path,
.minimal-container .tw-perf-card svg fill {
    fill: #4B5563 !important;
    stroke: #4B5563 !important;
}
.custom-track {
    width: 100%;
    height: 8px;
    background-color: #E5E7EB;
    border-radius: 999px;
    position: relative;
    overflow: hidden;
    margin-top: 6px;
}
.custom-fill {
    height: 100%;
    border-radius: 999px;
    position: absolute;
    left: 0;
    top: 0;
    transition: width 0.5s ease-in-out;
}
"""


def wrap_with_style(card_html):
    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '    <title>Fragrantica Performance Cards - Perfect</title>\n'
        '    <style>' + OFFLINE_CSS + '</style>\n'
        '</head>\n'
        '<body class="bg-gray-50 min-h-screen flex items-center justify-center p-6">\n'
        '\n'
        '    <div class="minimal-container bg-white p-8 rounded-2xl shadow-sm border border-gray-100 max-w-4xl transition-all duration-300 hover:shadow-md">\n'
        '        ' + card_html + '\n'
        '    </div>\n'
        '\n'
        '</body>\n'
        '</html>\n'
    )


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

        page.evaluate("""() => {
            const overlay = document.querySelector('[id^="sp_message_container"]');
            if (overlay) overlay.remove();
            document.documentElement.style.setProperty('overflow', 'auto', 'important');
            document.body.style.setProperty('overflow', 'auto', 'important');
        }""")
        page.wait_for_timeout(1000)

        for step in range(12):
            page.evaluate("window.scrollBy(0, 700);")
            page.wait_for_timeout(400)

        page.wait_for_timeout(3000)
        page.screenshot(path=str(DEBUG_IMAGE_PATH))

        extracted_html = page.evaluate("""() => {
            const allCards = Array.from(document.querySelectorAll('.tw-perf-card'));
            if (allCards.length === 0) return null;

            const longevityCard = allCards.find(card => card.className.includes('to-sky'));
            const sillageCard = allCards.find(card => card.className.includes('to-violet'));

            if (!longevityCard && !sillageCard) return null;

            let combinedHtml = '<div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full">';

            [longevityCard, sillageCard].forEach(card => {
                if (card) {
                    const clone = card.cloneNode(true);

                    // Capture computed background/border-radius from Fragrantica CSS
                    const cs = window.getComputedStyle(card);
                    clone.style.background = cs.background;
                    clone.style.borderRadius = cs.borderRadius;

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

                    clone.querySelectorAll('.sr-only').forEach(el => el.remove());

                    const sliders = clone.querySelectorAll('.vue-slider, [class*="vue-slider"]');
                    sliders.forEach(slider => {
                        const process = slider.querySelector('.vue-slider-process');
                        let width = '0%';
                        if (process && process.style.width) {
                            width = process.style.width;
                        }

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

            clean_html = re.sub(r'<vue-slider-marks.*?>.*?</vue-slider-marks>', '', clean_html, flags=re.DOTALL)
            clean_html = re.sub(r'<vue-slider-rail.*?>.*?</vue-slider-rail>', '', clean_html, flags=re.DOTALL)
            clean_html = clean_html.replace('vue-slider-marks', '')
            clean_html = clean_html.replace('vue-slider-rail', '')

            final_html = wrap_with_style(clean_html)

            with open(str(OUTPUT_HTML_PATH), "w", encoding="utf-8") as f:
                f.write(final_html)
            print(f"Done! Performance cards saved to {OUTPUT_HTML_PATH} (fully offline)")
        else:
            print("Error: longevity (to-sky) and sillage (to-violet) cards not found.")

        browser.close()

if __name__ == "__main__":
    main()
