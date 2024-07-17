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

    job_name_text = job_offer.locator('h3').text_content()
    print(f"Job Name: {job_name_text}")




time.sleep(5)

    


