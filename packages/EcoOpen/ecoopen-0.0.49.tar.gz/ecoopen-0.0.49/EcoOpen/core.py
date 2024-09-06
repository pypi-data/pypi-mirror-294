from habanero import Crossref
import numpy as np
import re
from tqdm import tqdm
import pandas as pd
import itertools
from pathlib import Path
import sys
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
# from urllib.error import 
import pathlib
from time import sleep
import pdfplumber
from pprint import pprint
from tqdm import tqdm
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from EcoOpen.utils.keywords import keywords
from EcoOpen.data_download import *


def get_date_string(published):
    
    return "-".join([str(i) for i in published])
    

def FindPapers(query="", doi=[], number_of_papers=10, start_year=2010, 
               end_year=datetime.now().year+1, sort="relevance", order="desc"):

    number_of_papers = int(number_of_papers)
    cr = Crossref()
    if query != "":
        papers = cr.works(
            query=query,
            limit=number_of_papers,
            filter = {
                "type": "journal-article",
                'from-pub-date': str(start_year),
                'until-pub-date': str(end_year)})
    elif doi != []:
        cr = Crossref()
        papers = cr.works(ids=doi)
    else:
        raise ValueError("Please provide a keyword, doi, title or author")
    dataframe = {
        "doi":[],
        "title":[],
        "authors":[],
        "published":[],
        "link":[],
    }

    if type(papers) == dict:
        if doi != []:
            if type(papers["message"]) == dict:
                paper = papers["message"]
                try:
                    dataframe["doi"].append(paper["DOI"])
                except KeyError:
                    dataframe["doi"].append("")
                try:
                    dataframe["title"].append(paper["title"][0])
                except KeyError:
                    dataframe["title"].append("")
                try:
                    authors = ""
                    for author in paper["author"]:
                        authors += author["given"] + " " + author["family"] + ", "
                    authors = authors[:-2]
                
                    dataframe["authors"].append(authors)
                except KeyError:
                    dataframe["authors"].append("")
                try:
                    date = get_date_string(paper["published"]["date-parts"][0])
                    dataframe["published"].append(date)
                except KeyError:
                    dataframe["published"].append("")
                try:
                    dataframe["link"].append(paper["link"][0]["URL"])
                except KeyError:
                    dataframe["link"].append("")
        else:
            for paper in papers["message"]["items"]:
                # fill the dataframe. if the certain key is not present add empty string
                try:
                    dataframe["doi"].append(paper["DOI"])
                except KeyError:
                    dataframe["doi"].append("")
                try:
                    dataframe["title"].append(paper["title"][0])
                except KeyError:
                    dataframe["title"].append("")
                try:
                    authors = ""
                    for author in paper["author"]:
                        authors += author["given"] + " " + author["family"] + ", "
                    authors = authors[:-2]
                
                    dataframe["authors"].append(authors)
                except KeyError:
                    dataframe["authors"].append("")
                try:
                    date = get_date_string(paper["published"]["date-parts"][0])
                    dataframe["published"].append(date)
                except KeyError:
                    dataframe["published"].append("")
                try:
                    dataframe["link"].append(paper["link"][0]["URL"])
                except KeyError:
                    dataframe["link"].append("")
    elif type(papers) == list:
        for p in papers:
            # fill the dataframe. if the certain key is not present add empty string
            paper = p["message"]
            try:
                dataframe["doi"].append(paper["DOI"])
            except KeyError:
                dataframe["doi"].append("")
            try:
                dataframe["title"].append(paper["title"][0])
            except KeyError:
                dataframe["title"].append("")
            try:
                authors = ""
                for author in paper["author"]:
                    authors += author["given"] + " " + author["family"] + ", "
                authors = authors[:-2]
                dataframe["authors"].append(authors)
            except KeyError:
                dataframe["authors"].append("")
            try:
                date = get_date_string(paper["published"]["date-parts"][0])
                dataframe["published"].append(date)
            except KeyError:
                dataframe["published"].append("")
            try:
                dataframe["link"].append(paper["link"][0]["URL"])
            except KeyError:
                dataframe["title"].append("")
                
    df = pd.DataFrame(dataframe)
    o = False
    if order == "asc":
        o = True
    if sort == "published":
        df = df.sort_values(by="published", ascending=o, ignore_index=True)
    
    return df
    # return papers


def get_journal_info(journal_name):
    cr = Crossref()
    journal = cr.journals(query=journal_name)
    return journal


def get_paper_by_keyword(keyword):
    cr = Crossref()
    papers = cr.works(query=keyword)
    return papers


def get_papers(journal_list="available_journals.csv"):
    df = pd.read_csv(journal_list, index_col=0)
    df = df.dropna()
    df = df.reset_index()
    # print(df)

    for i in range(200, len(df)):
        # i = 101
        journal_title = df["Title"][i]
        expected_papers = df["Number of papers since 2010"][i]
        issn = df["ISSN"][i]
        issn = issn.replace("'", "")
        issn = issn.replace("[", "").replace("]", "")
        issn = issn.replace(" ", "").split(",")

        print(issn)

        noffsets=1
        if expected_papers/1000 >=1:
            noffsets = expected_papers//1000
        cr = Crossref()
        print(f"Searching for papers in {journal_title} since 01-01-2010")
        for iss in issn:
            jinfo = cr.journals(
                ids=issn,
                works=True,
                sort="published",
                order="asc",
                cursor="*",
                cursor_max=int(expected_papers),
                filter = {'from-pub-date': '2010-01-01'},
                progress_bar = True,
                limit=1000)

            print(type(jinfo))
            print(iss)

            if type(jinfo) == dict:
                items = jinfo["message"]["items"]
                if len(items) > 0:
                    break
            else:
                print(sum(len(z["message"]["items"]) for z in jinfo))

                items = [z["message"]["items"] for z in jinfo]
                items = list(itertools.chain.from_iterable(items))

        papers = {}

        keys = [
            "title",
            "published",
            "DOI",
            "type",
            #"abstract",
            "link",
            "is-referenced-by-count",
            "publisher",
            "author" # TODO: format
        ]
        for key in keys:
            papers[key] = []
        n=1
        for item in items:
            for key in keys:
                try:
                    value = item[key]
                    if key=="title":
                        value = value[0]
                    elif key in ("published", "issued"):
                        value = value["date-parts"][0]
                        if len(value) == 3:
                            value = f"{value[0]}-{value[1]}-{value[2]}"
                        elif len(value) == 2:
                            value = f"{value[0]}-{value[1]}"
                        else:
                            value = f"{value[0]}"
                    elif key == "link":
                        for v in value:
                            # print(v["URL"])
                            if "xml" not in v["URL"]:
                                value = v["URL"]
                            if "pdf" in v["URL"]:
                                value = v["URL"]
                                break
                            else:
                                value="no link"

                    if key == "author":
                        author_string=""
                        for a in value:
                            author_string+=a["given"] + " "
                            author_string+=a["family"]
                            if a["affiliation"] != []:
                                author_string+=" (" + str(a["affiliation"][0]["name"]) + "),"                    
                        value= author_string

                    papers[key].append(value)
                except KeyError:
                    # print(f"KeyError: {key}")
                    if key == "link":
                        key="URL"
                        try:
                            papers["link"].append(item[key])
                        except KeyError:
                            papers[key].append("")
                    else:
                        papers[key].append("")

            #print([item[k] for k in keys])

        jdf = pd.DataFrame(papers)
        jj = journal_title.replace(" ", "_")
        idx_ = i+1
        jdf.to_csv(f"data/papers/{idx_:03d}_{jj}.csv", sep=",", quoting=2)

    return "done!"

def custom_tokenizer(text):
    pattern = r"(?u)\b\w\w+\b[!]*"
    return re.findall(pattern, text) 

def gather_journal_info(list_of_journals, path_to_save=None):
    ISSNs = []
    titles = []
    query = []
    available = []
    dois = []
    number_of_papers_since_2010 = []
    journals = tqdm(list_of_journals, colour="green")

    for i in journals:
        jinfo = get_journal_info(i)

        if jinfo['message']["total-results"] > 0:

            # find item wit the most similar title
            # finding the right journal
            # in majority of cases the idx of the most similar journal title
            # will be 0, however sometimes API returns more popular journal
            # title as the first choice therefore an similarity checks between
            # query and result needs to be performed
            titles_ = [j["title"] for j in jinfo["message"]["items"]]
            qq = i
            vectorizer = TfidfVectorizer(
                tokenizer=custom_tokenizer, token_pattern=None)
            combined_list = titles_ + [qq]
            tfidf_matrix = vectorizer.fit_transform(combined_list)
            # print(tfidf_matrix)
            cosine_sim = cosine_similarity(
                tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

            idx = cosine_sim.argmax()
            # sanity check
            # if idx!=0:
            #     print(titles_)
            #     print(cosine_sim)
            ### idx points to the most similiar title
            
            available.append(1)
            ISSNs.append(jinfo['message']['items'][idx]['ISSN'])
            titles.append(jinfo['message']['items'][idx]['title'])
            
            npapers = 0
            dj = jinfo[
                "message"
                ]["items"][idx]["breakdowns"]["dois-by-issued-year"]
            for year in dj:
                if int(year[0]) >= 2010:
                    npapers += year[1]
            number_of_papers_since_2010.append(npapers)
            # print(
            #     i, "|",
            #     jinfo['message']["total-results"], "|",
            #     npapers, "|",
            #     titles[-1], "|",
            #     idx)
            res = jinfo['message']["total-results"]
            # Setting tqdm description is buggy
            # journals.set_description(
            #    f"{i} | {res} | {npapers} | {titles[-1]} | {idx}"
            #    )

        else:
            available.append(0)
            ISSNs.append("")
            titles.append("")
            number_of_papers_since_2010.append("")
            # print(
            #     i,
            #     jinfo['message']["total-results"]
            #     )
            # journals.set_description(f"{i} | no result found")
        query.append(i)

    df = pd.DataFrame({
        "Journal query": query,
        "Title": titles,
        "ISSN": ISSNs,
        "Available": available,
        "Number of papers since 2010": number_of_papers_since_2010
    })
    # drop duplicate rows
    # df.drop_duplicates()
    if path_to_save:
        df.to_csv(path_to_save)
    return df

def pdf_download(url, title, output_dir):
    
    # # print(pdf_url)
    
    # if pdf_url.startswith('//'):
    #     pdf_url = f"https:{pdf_url}"
    # elif pdf_url.startswith('/'):
    #     pdf_url = f"https:/{pdf_url}"
    
    # try:
    #     pdf_response = requests.get(pdf_url)
        
    #     if pdf_response.status_code == 200:
    #         file_name = f"{title.replace(' ', '_').replace('.', '_').replace('/', '_')}.pdf"
    #         file_path = f"{output_dir}/{file_name}"

    #         # Create the output directory if it doesn't exist
    #         os.makedirs(output_dir, exist_ok=True)
    #         # Save the content of the response as a PDF file
    #         with open(file_path, 'wb') as f:
    #             f.write(pdf_response.content)
            
    #         return True
    #     else:
    #         # print("Failed to download PDF")
    #         return None
    # except requests.exceptions.ConnectionError:
    #     return None
    # except:
    
    #     return None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    file_name = f"{title.replace(' ', '_').replace('.', '_').replace('/', '_')}.pdf"
    # print(url)
    # print(output_dir)
    # print(file_name)
    try:
        # Send a GET request to the URL
        response = requests.get(url,  headers=headers, stream=True)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Create the output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Define the file path
            file_path = os.path.join(output_dir, file_name)
            
            # Save the content of the response as a file
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            # print(f"File downloaded successfully and saved as {file_path}")
            return True
        else:
            # print(f"Failed to download file. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # print(f"An error occurred: {e}")
        return None


def other_sources_download(doi, title, output_dir):
    output_dir = Path(os.path.expanduser(output_dir))
    output_dir = output_dir.absolute()
    # print(output_dir)

    if not os.path.exists(output_dir):
        os.system(f"mkdir {output_dir}")
        
    site_url = "https://sci-hub.se/"
    
    download_link = site_url+doi
    # Send a GET request to the Sci-Hub page
    response = requests.get(download_link, timeout=10)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the iframe or embed tag containing the PDF
        iframe = soup.find('iframe')
        if iframe:
            pdf_url = iframe['src']
        else:
            embed = soup.find('embed')
            if embed:
                pdf_url = embed['src']
            else:
                # print("PDF URL not found")
                return None
        # Handle relative URLs
        if pdf_url.startswith("/downloads"):
            pdf_url = f"https://sci-hub.se{pdf_url}"
        if pdf_url.startswith('//'):
            pdf_url = f"https:{pdf_url}"
        elif pdf_url.startswith('/'):
            pdf_url = f"https:/{pdf_url}"
            
        # Send a GET request to the extracted PDF URL
        # print(pdf_url)
        try:
            pdf_response = requests.get(pdf_url, timeout=3)

            # Check if the request was successful
            if pdf_response.status_code == 200:
                
                # remove non alphanumeric characters from the title
                title = re.sub(r'\W+', '', title)
                
                file_name = f"{title.replace(' ', '_').replace('.', '_').replace('/', '_')}.pdf"
                file_path = f"{output_dir}/{file_name}"

                # Create the output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)
                # Save the content of the response as a PDF file
                with open(file_path, 'wb') as f:
                    f.write(pdf_response.content)
                # print(f"Downloaded {file_name}")
                return True
            else:
                pass
        except requests.exceptions.ConnectionError:
            print("Connection error")
            print(pdf_url)
    else:
        pass


def download_paper(paper, output_dir, other_sources=False):
    output_dir = Path(os.path.expanduser(output_dir))
    output_dir = output_dir.absolute()
    # print(output_dir)

    link = paper["link"]
    title = paper["title"]
    doi = paper["doi"]

    # print(doi, title, link)
    
    download_link = ""

    if "pdf" not in link and link != "":
        download_link = link
        download_link = find_pdf(download_link)
    else:
        download_link = link

    # print(download_link, "!!!", title)

    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except FileNotFoundError:
            os.makedirs(output_dir, exist_ok=True)
    existing_papers = list(Path(f"{output_dir}").glob("**/*.pdf"))
    
    new_path = ""
    # print(download_link, "download link")
    if download_link == "":
        # print("PDF link was not found in the paper metadata or on the webpage")
        # print("Switching to Sci-Hub")
        if other_sources == True:
            try:
                r = other_sources_download(doi, title, output_dir)
                if r != None:
                    new_path = f'{output_dir}/{title.replace(" ", "_").replace(".","_").replace("/", "_")}.pdf'
            except ConnectionError:
                # print("Download failed")
                new_path = ""
        else:
            # print("No PDF link found")
            new_path
    elif "pdf" in download_link:
        # print("Downloading PDF from the provided link", download_link)
        r = pdf_download(download_link, title, output_dir)
        # print(r, "vanilla")
        if r != None:
            new_path = f'{output_dir}/{title.replace(" ", "_").replace(".","_").replace("/", "_")}.pdf'
    
    # print(new_path, "path")
    if new_path == "":
        return None
    elif Path(new_path).exists():
        # get path to the downloaded file that was not present before
        # print("Download successful", title)
        return new_path
    else:
        # print("Download failed")
        return None

def find_pdf(url):
    # Requests URL and get response object
    try:
        response = requests.get(url, timeout=3)
        # print(response.url)
        # Parse text obtained
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            soup = BeautifulSoup(response.text, "lxml")
        # Find all hyperlinks present on webpage
        links = soup.find_all('a')
        i = 0
        # From all links check for pdf link and
        # if present download file
        the_link = ""
        for link in links:
            # print(link)
            if ('pdf' in link.get('href', [])):
                i += 1
                # print(link.get('href', []))
                the_link = link.get('href', [])
                break

        # print(the_link, "The link")
        if the_link == "":
            return ""
        elif "http" not in the_link:
            return "http://"+urlparse(response.url).netloc+the_link
        else:
            return the_link
    except requests.exceptions.ConnectionError:
        return ""

def find_das(sentences):
    """Find data availability sentences in the text"""
    das_keywords = keywords["data_availability"]
    das_sentences = [sentence for sentence in sentences if any(kw.lower() in sentence.lower() for kw in das_keywords)]
    return das_sentences

def find_keywords(sentences):
    """find keywords in sentences"""
    detected = []
    kw = keywords.copy()
    kw.pop("data_availability")
    for k in kw.keys():
        kk = kw[k]
        for sentence in sentences:
            if any(kw.lower() in sentence.lower() for kw in kk):
                detected.append(sentence)
    return detected

def find_dataKW(path):
    """Find data keywords in the text"""
    raw = ReadPDF(path)
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', raw)
    das_sentences = find_das(sentences)
    keyword_sentences = find_keywords(sentences)
    
    
    # detect links in the sentences
    data_links = []
    for sentence in keyword_sentences:
        link = re.findall(r'(https?://\S+)', sentence)
        if link != []:
            data_links.append(link)
    
    # clean the links
    dl = []
    for i in data_links:
        for j in i:
            # split merged links
            if len(j.split("http")) > 2:
                for k in j.split("http"):
                    if k != "":
                        if ("http"+k) not in dl:
                            dl.append("http"+k)
            else:
                if j not in dl:
                    dl.append(j)
    # clean special non standard url characters
    dl = [i.replace(")", "").replace("]", "").replace("}", "") for i in dl]
    dl = [i.replace("(", "").replace("[", "").replace("{", "") for i in dl]
    dl = [i.replace(";", "").replace(",", "") for i in dl]
    return das_sentences, dl

def DownloadPapers(papers, output_dir, other_sources=False):
    print("Downloading papers")
    download_results = {"doi":[], "path": [], "result":[]}
    
    pbar = tqdm(total=len(papers))
    # with tqdm(total=len(papers)) as pbar:
    for idx, paper in tqdm(papers.iterrows()):
    
        paper = papers.iloc[idx]
        result = download_paper(paper, output_dir, other_sources)
        doi = paper["doi"]
        # pbar.set_description(f"Downloading {doi}")
        
        # print(type(result), "result")
        if result != None:
            download_results["doi"].append(doi)
            download_results["path"].append(result)
            download_results["result"].append("Success")
        else:
            download_results["doi"].append(doi)
            download_results["path"].append("Article publicly unavailable")
            download_results["result"].append("Article unavailable")
            
        pbar.update(1)


    # merge the results by doi
    download_results =  pd.DataFrame(download_results)

    download_results = pd.merge(papers, download_results, on="doi")

    return download_results


def ReadPDF(filepath):
    # parse PDF using 
    raw = ""
    try:
        pdf = pdfplumber.open(filepath)
        for page in pdf.pages:
            raw += page.extract_text()
        pdf.close()
    except:
        pass
    return raw.replace("\n", "")

def ReadPDFs(filepaths):
    # if filepaths is a dataframe extract filepaths
    if type(filepaths) == pd.core.frame.DataFrame:
        filepaths = filepaths["path"].tolist()
    raws = []
    for file in filepaths:
        if type(file) == pathlib.PosixPath:
            file = str(file)
        raw = ReadPDF(file)
        raws.append(raw)
    return raws


def FindOpenData(files, method="keywords"):
    """Prototype function to find open data in scientific papers"""

    # if "path" not in files.columns:
    #     print("Dataframe does not contain path column")
    #     print("Downloading papers")
    #     if output_dir == "":
    #         raise ValueError(
    #             "Please provide output directory using output_dir argument")
    #     files = download_papers(files, output_dir, scihub=False)
    print(f"Finding open data using '{method}' method:")
    data_links = []

    if method == "keywords":
        for i in tqdm(files["path"].tolist()):
            try:
                das, dl = find_dataKW(i)
                data_links.append(dl)
            except FileNotFoundError:
                data_links.append([])
    elif method == "web":
        for i in tqdm(files["doi"].tolist()):
            dl = find_data_web(i)
            data_links.append(dl)
    else:
        raise ValueError("Method not recognized, use keywords or web!")

    # print(len(files))
    # print(len(data_links))
    files["data_links"+f"_{method}"] = data_links

    return files

def analyze_reference_document(path):
    """
    Analyze reference document for data availability
    Used to analyze references in pdf or other text documents
    """

    # reference document analysis routine
    result = {
        "doi":[],
        "title":[],
        "authors":[],
        "original_data_present": [],
        "data_links": []
    }
    return result


if __name__ == "__main__":
    papers = FindPapers("Hackenberger")
