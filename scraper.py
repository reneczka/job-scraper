from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto('https://justjoin.it')
    
    page.wait_for_selector("#cookiescript_accept")
    page.click("#cookiescript_accept")
    page.click('a[href="/all-locations/python"]')    
    time.sleep(5)