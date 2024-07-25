from playwright.sync_api import sync_playwright
import time

def get_jobs_set():
    job_anchors = page.locator('a.offer_list_offer_link')
    num_offers = job_anchors.count()
    jobs_set = []

    for i in range(num_offers):
        job_anchor = job_anchors.nth(i)
        job_info = get_job_info(job_anchor)
        jobs_set.append(job_info)

    # print(f"Number of offers extracted: {num_offers}")
    
    return jobs_set


def get_job_info(job_anchor):
    job_offer = job_anchor.locator('..')

    job_name = job_offer.locator('h3')

    job_name_text = job_name.text_content()
    # print(f"Job Name: {job_name_text}")

    container_company_location_remote = job_name.locator('..').locator("xpath=following-sibling::*[1]")

    company_name_text = container_company_location_remote.locator('span').first.text_content()
    # print(f"Company Name: {company_name_text}")

    job_location_text = container_company_location_remote.locator('span').nth(1).text_content()
    # print(f"Job Location: {job_location_text}")

    remote_tags = container_company_location_remote.get_by_text('remote')

    is_remote = True if remote_tags.count() > 0 else False
    # print(f"Is Remote: {is_remote}")

    salary = job_name.locator("xpath=following-sibling::*[1]").locator("xpath=./div[1]").text_content()
    # print(f"Salary: {salary}")

    job_url = 'https://justjoin.it' + job_anchor.get_attribute('href')
    # print(f"Job URL: {job_url}")
    
    # print("-" * 100)
    return {
        'job_name': job_name_text,
        'job_url': job_url
    }

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=250)
    page = browser.new_page()
    page.goto('https://justjoin.it')

    page.wait_for_selector("#cookiescript_accept")
    page.click("#cookiescript_accept")
    page.click('a[href="/all-locations/python"]')
    page.click('button[name="sort_filter_button"]')  
    page.get_by_text("Latest").click()

    page.wait_for_load_state('networkidle')
    all_offers = []

    initial_set = get_jobs_set()

    all_offers.extend(initial_set)

    for iteration in range(3):
        page.mouse.wheel(0, 2000)
        scrolled_set = get_jobs_set()
        all_offers.extend(scrolled_set)
        
    
    print(all_offers)

    time.sleep(5)


# 1: stworzenie listy ze wszystkimi ofertami
# 	a)stworzenie pustej listy
# 	b)dodanie inicjalnych ofert do listy
# 		b).1.nowa zmienna z id href
# 		b).2.returnowanie slownika z oferta
# 	c)dodanie ofert po scrolu w petli
# 	(sprawienie w tej petli zeby sie nie duplikowaly oferty)

# 2: wrzucic do bazy
