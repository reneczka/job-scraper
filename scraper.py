from playwright.sync_api import sync_playwright
import time

def extract_job_info(job_anchor):
    job_offer = job_anchor.locator('..')
    job_name = job_offer.locator('h3')

    job_name_text = job_name.text_content()
    print(f"Job Name: {job_name_text}")

    container_company_location_remote = job_name.locator('..').locator("xpath=following-sibling::*[1]")

    company_name_text = container_company_location_remote.locator('span').first.text_content()
    print(f"Company Name: {company_name_text}")

    job_location_text = container_company_location_remote.locator('span').nth(1).text_content()
    print(f"Job Location: {job_location_text}")

    remote_tags = container_company_location_remote.get_by_text('remote')

    is_remote = True if remote_tags.count() > 0 else False
    print(f"Is Remote: {is_remote}")

    salary = job_name.locator("xpath=following-sibling::*[1]").locator("xpath=./div[1]").text_content()
    print(f"Salary: {salary}")
    
    print("-" * 50)

with sync_playwright() as p:
    browser = p.chromium.launch(slow_mo=250)
    page = browser.new_page()
    page.goto('https://justjoin.it')

    page.wait_for_selector("#cookiescript_accept")
    page.click("#cookiescript_accept")
    page.click('a[href="/all-locations/python"]')
    page.click('button[name="sort_filter_button"]')  
    page.get_by_text("Latest").click()

    page.wait_for_load_state('networkidle')

    job_anchors = page.locator('a.offer_list_offer_link') 

    for i in range(job_anchors.count()):
        job_anchor = job_anchors.nth(i)
        extract_job_info(job_anchor)

time.sleep(5)
