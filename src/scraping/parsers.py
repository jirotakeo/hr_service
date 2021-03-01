from random import randint
import requests
from bs4 import BeautifulSoup as BS


__all__ = ('work', 'rabota')


headers = [{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': '*/*', 'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'},
           {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) '
                          'Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]


def work(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='pjax-job-list')
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'job-link'})
                for div in div_list:
                    title = div.find('h2')
                    href = title.a['href']
                    content = div.p.text
                    company = 'Компания скрыта'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain+href, 'description': content,
                                 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'div does not exists'})
        else:
            errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 1)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
            if not new_jobs:
                table = soup.find('table', id='ctl00_content_vacancyList_gridList')
                if table:
                    tr_lst = table.find_all('tr', attrs={'id': True})
                    for tr in tr_lst:
                        div = tr.find('div', attrs={'class': 'card-body'})
                        if div:
                            title = div.find('h2', attrs={'class': 'card-title'})
                            href = title.a['href']
                            content = div.find('div', attrs={'class': 'card-description'}).text
                            company = 'Компания скрыта'
                            p = div.find('p', attrs={'class': 'company-name'})
                            if p:
                                company = p.a.text
                            jobs.append({'title': title.text, 'url': domain+href, 'description': content,
                                         'company': company, 'city_id': city, 'language_id': language})
                else:
                    errors.append({'url': url, 'title': 'table does not exists'})
            else:
                errors.append({'url': url, 'title': 'page is empty'})
        else:
            errors.append({'url': url, 'title': 'page do not response'})

    return jobs, errors


if __name__ == '__main__':
    url = 'https://rabota.ua/zapros/python/%D0%BA%D0%B8%D0%B5%D0%B2'
    jobs, errors = rabota(url)
    h = open('../work.text', 'w')
    h.write(str(jobs))
    h.close()
