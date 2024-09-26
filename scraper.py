from playwright.sync_api import sync_playwright
import time

def get_jobs_set(page):
    # select all job offer links using the class selector
    # this targets <a> elements with the class 'offer_list_offer_link'
    job_anchors = page.locator('a.offer_list_offer_link').locator('..')
    num_offers = job_anchors.count()
    jobs_set = []

    for i in range(num_offers):
        job_anchor = job_anchors.nth(i)
        job_info = get_job_info(page, job_anchor)
        jobs_set.append(job_info)
    
    return jobs_set

def get_job_info(page, job_anchor):
    # select the parent container of the job offer
    # uses '..' to move up one level in the DOM from the anchor
    job_offer = job_anchor.locator('..')

    # select the job title, which is in an <h3> element within the job offer container
    job_name = job_offer.locator('h3')
    job_name_text = job_name.text_content()

    # select the container with company name, location, and remote info
    # this uses xpath to find the first sibling element after the parent of the job name
    container_company_location_remote = job_name.locator('..').locator("xpath=following-sibling::*[1]")

    # select the company name (first <span> within the container)
    company_name_text = container_company_location_remote.locator('span').first.text_content()

    # select the job location (second <span> within the container)
    job_location_text = container_company_location_remote.locator('span').nth(1).text_content()

    # select the salary information
    # this uses xpath to find the first sibling after the job name, then selects its first div child
    salary = job_name.locator("xpath=following-sibling::*[1]").locator("xpath=./div[1]").text_content()

    # construct the full job URL by appending the href attribute to the base URL
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
    
    # select and extract type of work
    # uses text content to find the label, then selects its next sibling
    type_of_work_label = page.get_by_text('Type of work').first
    type_of_work = type_of_work_label.locator('xpath=following-sibling::*[1]').text_content()
    
    # select and extract experience level
    # uses text content to find the label, then selects its next sibling
    experience_label = page.get_by_text('Experience').first
    experience = experience_label.locator('xpath=following-sibling::*[1]').text_content()
    
    # select and extract employment type
    # uses text content to find the label, then selects its next sibling
    employment_type_label = page.get_by_text('Employment Type').first
    employment_type = employment_type_label.locator('xpath=following-sibling::*[1]').text_content()
    
    # select and extract operating mode
    # uses text content to find the label, then selects its next sibling
    operating_mode_label = page.get_by_text('Operating mode').first
    operating_mode = operating_mode_label.locator('xpath=following-sibling::*[1]').text_content()
    
    # select the tech stack container
    # finds the 'Tech stack' label, then navigates to its sibling <ul> element
    techstack_label = page.get_by_text('Tech stack').first
    techstack_container = techstack_label.locator("xpath=following-sibling::*[1]").locator("ul")
    tech_items = techstack_container.locator("> div")

    technologies = []
    for i in range(tech_items.count()):
        tech_item = tech_items.nth(i)

        # extract technology name from <h4> and level from <span> within each tech item
        technology = tech_item.locator("h4").inner_text()
        level = tech_item.locator("span").inner_text()
        tech_dict = {
            'tech': technology,
            'level': level
        }
        technologies.append(tech_dict)

    # select and extract job description
    # finds the 'Job description' label, moves up to its parent, then selects the next sibling div
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

        # wait for and click the cookie accept button using its id
        page.wait_for_selector("#cookiescript_accept")
        page.click("#cookiescript_accept")
        
        # navigate to python jobs by clicking the link with the specified href
        page.click('a[href="/all-locations/python"]')
        time.sleep(1)
        
        # open sort options and select "latest"
        page.click('button[name="sort_filter_button"]')
        page.get_by_text("Latest").click()
        time.sleep(1)
        
        # apply junior filter by opening more filters, selecting the checkbox, and submitting
        page.click('button[name="more_filters_button"]')
        page.click('input[name="experienceLevels-junior"]')
        page.click('button[name="more_filters_submit_button"]')
        
        # wait for the page to finish loading
        page.wait_for_load_state('networkidle')
        all_jobs = get_jobs_set(page)
        browser.close()
        return all_jobs