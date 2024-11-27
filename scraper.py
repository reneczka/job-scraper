from playwright.sync_api import sync_playwright
import time

def get_jobs_set(page):
    job_anchors = page.locator('a[href^="/job-offer/"]')
    num_offers = job_anchors.count()
    jobs_set = []

    for i in range(num_offers):
        job_anchor = job_anchors.nth(i)
        job_info = get_job_info(page, job_anchor)
        jobs_set.append(job_info)
    
    return jobs_set

def get_job_info(page, job_anchor):
    job_offer = job_anchor.locator('..')

    job_name = job_offer.locator('h3')
    job_name_text = job_name.text_content()

    container_company_location_remote = job_name.locator('..').locator("xpath=following-sibling::*[1]")

    company_name_text = container_company_location_remote.locator('span').first.text_content()

    job_location_text = container_company_location_remote.locator('span').nth(1).text_content()

    salary = job_name.locator("xpath=following-sibling::*[1]").locator("xpath=./div[1]").text_content()

    job_url = 'https://justjoin.it' + job_anchor.get_attribute('href')
    

    
    details = get_job_details(page, job_url)
    page.go_back()
    
    all_info =  {
        'job_name': job_name_text,
        'company_name': company_name_text,
        'job_location': job_location_text,
        'salary': salary,
        'job_url': job_url,
    }
    
    result = {**all_info, **details}
        
    return result

def get_job_details(page, job_url):
    time.sleep(1)
    page.goto(job_url)
    
    # offer details part 1
    type_of_work_label = page.get_by_text('Type of work').first
    type_of_work = type_of_work_label.locator('xpath=following-sibling::*[1]').text_content()
    
    # experience_label = page.get_by_text('Experience').first
    experience_label = page.locator('//div[text()="Experience"]')
    experience = experience_label.locator('xpath=following-sibling::*[1]').text_content()
    
    employment_type_label = page.get_by_text('Employment Type').first
    employment_type = employment_type_label.locator('xpath=following-sibling::*[1]').text_content()

    operating_mode_label = page.get_by_text('Operating mode').first
    operating_mode = operating_mode_label.locator('xpath=following-sibling::*[1]').text_content()

    # offer details part 2
    techstack_label = page.get_by_text('Tech stack').first
    techstack_container = techstack_label.locator("xpath=following-sibling::*[1]").locator("ul")
    tech_items = techstack_container.locator("> div")

    technologies = []
    for i in range(tech_items.count()):
        tech_item = tech_items.nth(i)

        technology = tech_item.locator("h4").inner_text()
        level = tech_item.locator("span").inner_text()
        tech_dict = {
            'tech': technology,
            'level': level
        }
        technologies.append(tech_dict)

    # offer details part 3
    job_description = page.get_by_text('Job description').first.locator('..').locator("xpath=following-sibling::div[1]").inner_text()

    return {
        'type_of_work': type_of_work,
        'experience': experience,
        'employment_type': employment_type,
        'operating_mode': operating_mode,
        'technologies': technologies,
        'job_description': job_description,
    }

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=250)
        page = browser.new_page()
        page.goto('https://justjoin.it')

        page.wait_for_selector("#cookiescript_accept")
        page.click("#cookiescript_accept")
        
        page.click('a[href="/job-offers/all-locations/python"]')
        time.sleep(1)
        
        page.click('button[name="sort_filter_button"]')
        time.sleep(1)
        page.get_by_text("Latest").click()
        time.sleep(1)
        
        page.click('button[name="more_filters_button"]')
        time.sleep(1)
        page.click('input[value="junior"]')
        page.click('button[name="more_filters_submit_button"]')
        time.sleep(1)
      
        page.wait_for_load_state('networkidle')
        all_jobs = get_jobs_set(page)
        browser.close()
        return all_jobs