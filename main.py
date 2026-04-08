import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_soup(url_0):
    res = requests.get(url_0)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")

    return soup


def get_job_details(url_1):
    response = requests.get(url_1)
    soup = BeautifulSoup(response.text, "html.parser")

    details = soup.find("div", class_="content").text.strip()

    return details


def get_job_listing(soup):
    base_url = "https://realpython.github.io"
    work_data = []

    all_jobs = soup.find_all("div", class_="column is-half")

    for job in all_jobs:
        title_tag = job.find("div", class_="media-content").h2
        job_title = title_tag.text.strip() if title_tag else "N/A"
        company_name = job.find("div", class_="media-content").h3.text.strip()
        location = job.find("p", class_="location").text.strip()
        info = job.find("footer", class_="card-footer").find_all("a")

        if len(info) > 1:
            correct_link = urljoin(base_url, info[1].get("href", ""))
        else:
            correct_link = "N/A"
        details = get_job_details(correct_link)

        job_data = {'Title': job_title, 'Company': company_name, 'Location': location, 'Details': details}

        if "Python" in job_data.get("Title"):
            work_data.append(job_data)

    return work_data


def save_to_csv(data):
    with open("result.csv", "w", encoding="utf-8", newline="") as f:
        fieldnames = data[0].keys()

        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)
    return f


if __name__ == "__main__":
    url_0 = "https://realpython.github.io/fake-jobs/"

    soup = get_soup(url_0)
    data = get_job_listing(soup)
    save_to_csv(data)
