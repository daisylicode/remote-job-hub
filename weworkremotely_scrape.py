from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import re
import os
import json

def fetch_jobs():
    url = "https://weworkremotely.com/remote-jobs"
    jobs = []
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("li.new-listing-container")
        job_cards = page.query_selector_all("li.new-listing-container")
        for card in job_cards:
            # 检查是否有"Anywhere in the World"
            region_tags = card.query_selector_all("p.new-listing__categories__category")
            if not any("Anywhere in the World" in tag.inner_text() for tag in region_tags):
                continue

            # 发布时间（只判断几天内）
            time_tag = card.query_selector("p.new-listing__header__icons__date")
            if not time_tag:
                continue
            days_text = time_tag.inner_text().strip()
            # print("days_text", days_text)
            if days_text == "NEW":
                pass  # NEW 直接通过
            elif days_text.endswith("d"):
                try:
                    days = int(days_text.replace("d", ""))
                except Exception:
                    continue
                if days > 7:
                    continue
            else:
                continue

            # 职位和公司
            job_title = card.query_selector("div.new-listing__header")
            company = card.query_selector("p.new-listing__company-name")
            # 获取公司链接
            company_link_tag = card.query_selector('div.tooltip--flag-logo a[href^="/company/"]')
            if company_link_tag:
                company_url = company_link_tag.get_attribute("href")
                if company_url and company_url.startswith("/"):
                    company_url = f"https://weworkremotely.com{company_url}"
            else:
                company_url = None

            # 获取职位详情页链接（li下第一个a，且href以/listings/开头）
            job_link_tag = card.query_selector('a[href^="/listings/"]')
            if job_link_tag:
                job_url = job_link_tag.get_attribute("href")
                if job_url and job_url.startswith("/"):
                    job_url = f"https://weworkremotely.com{job_url}"
            else:
                job_url = None

            if job_title and company:
                # 修正job_title，去除末尾的'\n\n1d'、'\n\nNEW'等
                raw_title = job_title.inner_text().strip()
                # 去除末尾的换行和天数/NEW
                cleaned_title = re.sub(r"\n\n(NEW|\d+d)$", "", raw_title).strip()
                # 获取job_type（职位类型）
                job_type = None
                # 用xpath查找最近的父section.jobs
                parent_section = card.query_selector('xpath=ancestor::section[contains(@class, "jobs")]')
                if parent_section:
                    h2_a = parent_section.query_selector('h2 > a')
                    if h2_a:
                        job_type = h2_a.inner_text().strip()

                job = {
                    "job_title": cleaned_title,
                    "company": company.inner_text().strip(),
                    "posted_date": days_text,
                    "job_link": job_url,
                    "company_link": company_url,
                    "job_type": job_type
                }
                print("job", job)
                jobs.append(job)
        browser.close()
    return jobs

if __name__ == "__main__":
    jobs = fetch_jobs()
    # 确保results目录存在
    os.makedirs("results", exist_ok=True)
    # 保存为json文件
    with open("results/weworkremotely.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(jobs)} 条数据到 results/weworkremotely.json")