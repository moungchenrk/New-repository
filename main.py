import asyncio
from playwright.async_api import async_playwright
from telegram import Bot

# ✅ টেলিগ্রাম বট সেটআপ
TELEGRAM_BOT_TOKEN = "8116152551:AAF3EjeKuNPGQS_MeHsvYAuP68FaKMHG_2c"
CHAT_ID = "-1002262735570"  # এখানে স্পেস ছিল, সেটা সরিয়ে দিয়েছি

bot = Bot(token=TELEGRAM_BOT_TOKEN)

previous_price = None

async def send_signal(signal):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=f"📈 Quotex Signal: {signal}")
        print(f"📤 Sent to Telegram: {signal}")
    except Exception as e:
        print("❌ Telegram Error:", e)

async def run():
    global previous_price
    async with async_playwright() as p:
        # Browser launch with additional arguments for 'no-sandbox' and 'disable-setuid-sandbox'
        browser = await p.chromium.launch(
            headless=True, 
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context()
        page = await context.new_page()

        print("🔓 Logging in to Quotex...")
        await page.goto("https://qxbroker.com/en/login")

        await page.fill('input[name="email"]', "putolrk10@gmail.com")
        await page.fill('input[name="password"]', "Laburkk1@")
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(5000)

        print("✅ Logged in. Going to trade page...")
        await page.goto("https://qxbroker.com/en/trade")
        await page.wait_for_timeout(10000)

        print("📡 Monitoring Live Price...")
        while True:
            try:
                price_element = await page.query_selector('div.price-value')
                price_text = await price_element.inner_text() if price_element else "0"
                current_price = float(price_text)
                print(f"💰 Price: {current_price}")

                if previous_price is not None:
                    if current_price > previous_price:
                        await send_signal("BUY")
                    elif current_price < previous_price:
                        await send_signal("SELL")
                previous_price = current_price

            except Exception as e:
                print("⚠️ Error fetching price:", e)

            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(run())
