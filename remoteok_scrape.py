
# https://remoteok.com/?location=Worldwide

import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://remoteok.com/?location=Worldwide"
    jobs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        # 增加更多伪装
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            viewport={"width": 1280, "height": 800}
        )
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_selector('table#jobsboard')
        print("page loaded")

        # 自动滚动5次，加载更多职位
        scroll_times = 2
        for _ in range(scroll_times):
            await page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            await asyncio.sleep(1)
        print(f"已自动滚动{scroll_times}次，加载更多职位。")

        job_rows = await page.query_selector_all('table#jobsboard tr')
        print("job_rows count:", len(job_rows))
        for row in job_rows:
            
            # 判断是否为职位行（有 h2[itemprop="title"] 才是职位）
            h2_tag = await row.query_selector('h2[itemprop="title"]')
            if not h2_tag:
                continue
            # 职位链接
            a_tag = await row.query_selector('a.preventLink[itemprop="url"]')
            job_link = ""
            if a_tag:
                href = await a_tag.get_attribute('href')
                if href:
                    job_link = "https://remoteok.com" + href

            # 职位名称
            h2_tag = await row.query_selector('h2[itemprop="title"]')
            job_title = (await h2_tag.inner_text()).strip() if h2_tag else ""

            # 公司名称
            h3_tag = await row.query_selector('h3[itemprop="name"]')
            company = (await h3_tag.inner_text()).strip() if h3_tag else ""

            # 发布时间
            time_tag = await row.query_selector('time')
            posted_date = (await time_tag.inner_text()).strip() if time_tag else ""

            # 只保留xh或xd且天数<=7的职位
            keep = False
            if posted_date.endswith('h'):
                keep = True
            elif posted_date.endswith('d'):
                try:
                    days = int(posted_date[:-1])
                    if days <= 7:
                        keep = True
                except Exception:
                    pass
            if not keep:
                continue

            # 地点
            location_tag = await row.query_selector('div.location')
            location = (await location_tag.inner_text()).strip() if location_tag else ""

            jobs.append({
                "job_link": job_link,
                "job_title": job_title,
                "company": company,
                "posted_date": posted_date,
                "location": location
            })

        await browser.close()

    os.makedirs("results", exist_ok=True)
    with open("results/remoteok.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"已抓取 {len(jobs)} 条职位信息，保存到 results/remoteok.json")

if __name__ == "__main__":
    asyncio.run(main())
