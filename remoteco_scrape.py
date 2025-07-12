import asyncio
import json
import os
from playwright.async_api import async_playwright

async def main():
    url = "https://remote.co/remote-jobs/search?remoteoptions=100%25%20Remote%20Work&useclocation=true&joblocations=Anywhere%2C%20null%2C%20%40%40%40%2C%20&anywhereinworld=1&loc.latlng=0%2C0&loc.radius=30"
    jobs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        await page.goto(url)
        await page.wait_for_selector('div[role="region"][aria-label="job-category-list"] div[id][data-isfreejob]')

        region = await page.query_selector('div[role="region"][aria-label="job-category-list"]')
        job_cards = await region.query_selector_all('div[id][data-isfreejob]')
        print("job_cards count:", len(job_cards))
        for card in job_cards:
            # 职位链接和名称
            a_tag = await card.query_selector('a[href^="/job-details/"]')
            job_link = ""
            job_title = ""
            if a_tag:
                href = await a_tag.get_attribute('href')
                if href:
                    job_link = "https://remote.co" + href
                job_title = (await a_tag.inner_text()).strip()
                # 去除 'New!'
                job_title = job_title.replace('New!', '').strip()

            # 公司名称
            company_tag = await card.query_selector('h3')
            company = (await company_tag.inner_text()).strip() if company_tag else ""

            # 发布时间
            posted_date = ""
            span_tags = await card.query_selector_all('span')
            for span in span_tags:
                text = (await span.inner_text()).strip()
                if any(x in text for x in ["day", "Yesterday", "hour", "minute", "Today"]):
                    posted_date = text
                    break

            # 只保留7天内的职位
            keep = False
            if posted_date:
                if posted_date in ["Today", "Yesterday"]:
                    keep = True
                elif "day" in posted_date:
                    try:
                        days = int(posted_date.split()[0])
                        if days <= 7:
                            keep = True
                    except Exception:
                        pass
            if not keep:
                continue

            # 地点
            # location_tag = await card.query_selector('span[class*="xGhZX"]')
            # location = (await location_tag.inner_text()).strip() if location_tag else ""

            jobs.append({
                "job_link": job_link,
                "job_title": job_title,
                "company": company,
                "posted_date": posted_date
            })
        await browser.close()

    os.makedirs("results", exist_ok=True)
    with open("results/remoteco.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"已抓取 {len(jobs)} 条职位信息，保存到 results/remoteco.json")

if __name__ == "__main__":
    asyncio.run(main())