import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://www.workingnomads.com/jobs?location=anywhere&postedDate=7"
    jobs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800}
        )
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector('div.jobs-list')

        # 滚动加载更多职位（可根据需要调整次数）
        scroll_times = 3
        for _ in range(scroll_times):
            await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)

        job_cards = await page.query_selector_all('div.jobs-list > div[ng-repeat]')
        print("job_cards count:", len(job_cards))
        for card in job_cards:
            # 职位链接和名称
            a_tag = await card.query_selector('a[href^="/jobs/"]')
            job_link = ""
            job_title = ""
            if a_tag:
                href = await a_tag.get_attribute('href')
                if href:
                    job_link = "https://www.workingnomads.com" + href
                job_title = (await a_tag.inner_text()).strip()

            # 公司名称
            company_tag = await card.query_selector('div.company.hidden-xs a.ng-binding')
            company = (await company_tag.inner_text()).strip() if company_tag else ""

            # 发布时间
            date_tag = await card.query_selector('div.job-col.job-right-col div.date.hidden-xs.ng-binding')
            posted_date = (await date_tag.inner_text()).strip() if date_tag else ""

            # 只保留7天内的职位
            keep = False
            if posted_date.endswith('day ago'):
                try:
                    days = int(posted_date.split()[0])
                    if days <= 7:
                        keep = True
                except Exception:
                    pass
            elif posted_date.endswith('days ago'):
                try:
                    days = int(posted_date.split()[0])
                    if days <= 7:
                        keep = True
                except Exception:
                    pass
            elif posted_date in ['Today', 'Yesterday']:
                keep = True

            if not keep:
                continue

            jobs.append({
                "job_link": job_link,
                "job_title": job_title,
                "company": company,
                "posted_date": posted_date
            })

        await browser.close()

    os.makedirs("results", exist_ok=True)
    with open("results/workingnomads.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"已抓取 {len(jobs)} 条职位信息，保存到 results/workingnomads.json")

if __name__ == "__main__":
    asyncio.run(main())

