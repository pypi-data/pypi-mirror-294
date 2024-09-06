from habanero import Crossref
import pandas as pd

doi = ["10.1016/j.ecolmodel.2011.10.027", "10.1016/j.ecolmodel.2013.06.014"]

cr = Crossref()

papers = cr.works(ids=doi)
for paper in papers["message"]["items"]:
    # fill the dataframe. if the certain key is not present add empty string
    dataframe = {
        "doi":[],
        "title":[],
        "authors":[],
        "published":[],
        "link":[],
    }   
    
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
        dataframe["published"].append(paper["published"]["date-parts"][0])
    except KeyError:
        dataframe["published"].append("")
    try:
        dataframe["link"].append(paper["link"][0]["URL"])
    except KeyError:
        dataframe["link"].append("")
        
        
df = pd.DataFrame(dataframe)
