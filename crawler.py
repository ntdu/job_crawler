import bs4
import requests
from datetime import datetime
import time


def get_page_content(url):
    page = requests.get(url, verify=False, headers={"Accept-Language": "en-US"})
    return bs4.BeautifulSoup(page.content, "html.parser")

def topcv_crawler(job_stop_id=0):
    list_accepted = []
    i = 0

    for page in range(1, 401):
        jobs_html = get_page_content(f'https://www.topcv.vn/tim-viec-lam-moi-nhat?salary=0&exp=0&sort=new&page={page}')

        jobs = jobs_html.findAll('div', class_='job-item')
        for job in jobs:
            try:
                job_id = job['data-job-id']
                if job_stop_id == int(job_id): return list_accepted

                job_title = ''
                company_title = ''
                job_deadline = ''
                job_salary = ''
                job_vacancy_number = ''
                job_type = ''
                job_role = ''
                job_gender = ''
                job_experience = ''
                job_areas = ''
                
                list_accepted.append({
                    'job_id': job_id,
                    'job_title': '',
                    'company_title': '',
                    'job_deadline': '',
                    'job_salary': '',
                    'job_vacancy_number': '',
                    'job_type': '',
                    'job_role': '',
                    'job_gender': '',
                    'job_experience': '',
                    'job_areas': '',
                    'job_description': '',
                    'job_requirements': '',
                    'job_benefits': ''
                })
                
                job_detail_url = job.find('h3', class_='title').find('a')['href']
                detail_html = get_page_content(job_detail_url)

                detail_header_html = detail_html.find('div', class_='box-info-job')
                # job_title = detail_header_html.find('h1').find('a').text.strip()
                job_title = detail_header_html.find('h1').text.strip()
                company_title = detail_header_html.find('div', class_='company-title').find('a').text.strip()
                job_deadline = detail_header_html.find('div', class_='job-deadline').text.strip()
                list_accepted[-1]['job_title'] = job_title
                list_accepted[-1]['company_title'] = company_title
                list_accepted[-1]['job_deadline'] = job_deadline
                # print(job_title)
                # print(company_title)
                # print(job_deadline)

                detail_info_html = detail_html.find('div', id='tab-info')
                detail_general_info = list(map(lambda x: x.text.strip(), detail_info_html.find('div', class_='box-main').findAll('span')))

                # job_salary = detail_general_info[0]
                # job_vacancy_number = detail_general_info[1]
                # job_type = detail_general_info[2]
                # job_role = detail_general_info[3]
                # job_gender = detail_general_info[4]
                # job_experience = detail_general_info[5]
                
                list_accepted[-1]['job_salary'] = detail_general_info[0]
                list_accepted[-1]['job_vacancy_number'] = detail_general_info[1]
                list_accepted[-1]['job_type'] = detail_general_info[2]
                list_accepted[-1]['job_role'] = detail_general_info[3]
                list_accepted[-1]['job_gender'] = detail_general_info[4]
                list_accepted[-1]['job_experience'] = detail_general_info[5]
                
                areas_html = detail_info_html.find('div', class_='box-address').find('div')
                more_areas = []

                try:
                    areas_html.find('a').decompose()
                    more_areas = list(map(lambda x: x.text.strip(), areas_html.find('div', id='more-job-addresses').findAll('div')))
                    
                    areas_html.find('div', id='more-job-addresses').decompose()
                except: 
                    pass

                # job_areas = list(map(lambda x: x.text.strip(), areas_html.findAll('div'))) + more_areas
                list_accepted[-1]['job_areas'] = '\n'.join(list(map(lambda x: x.text.strip(), areas_html.findAll('div'))) + more_areas)

                detail_detail_info_html = detail_info_html.find('div', class_='job-data')
                detail_detail_info = list(map(lambda x: x.text.strip(), detail_detail_info_html.findAll('div')))

                # job_description = detail_detail_info[0]
                # job_requirements = detail_detail_info[1]
                # job_benefits = detail_detail_info[2]
            
                list_accepted[-1]['job_description'] = detail_detail_info[0]
                list_accepted[-1]['job_requirements'] = detail_detail_info[1]
                list_accepted[-1]['job_benefits'] = detail_detail_info[2]

            except:
                pass
        
        i += 1
        if i == 10: break
    
    return list_accepted