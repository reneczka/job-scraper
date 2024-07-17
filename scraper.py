from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()
    page.goto('https://justjoin.it')
    
    page.wait_for_selector("#cookiescript_accept")
    page.click("#cookiescript_accept")
    page.click('a[href="/all-locations/python"]')    # select all elements with the tag a which has an attribute href with a value of all locations python
    page.click('button[name="sort_filter_button"]')  
    page.get_by_text("Latest").click()
    page.wait_for_load_state('networkidle')

    job_anchor = page.locator('a.offer_list_offer_link').first

    job_offer = job_anchor.locator('..')

    job_name = job_offer.locator('h3') # h3 tag 

    job_name_text = job_name.text_content()
    print(f"Job Name: {job_name_text}")

    job_name_parent = job_name.locator('..')

    job_name_parent_sibling = job_name_parent.locator("xpath=following-sibling::*[1]")

    company_name_text = job_name_parent_sibling.locator('span').first.text_content()
    print(f"Company Name: {company_name_text}")

    




time.sleep(5)

    


