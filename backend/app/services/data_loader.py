import os
import requests
import xml.etree.ElementTree as ET
from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import TokenTextSplitter

def process_file(contents, filename):
    with open(filename, "wb") as f:
        f.write(contents)
    with open(filename, "r") as f:
        text = f.read()
    os.remove(filename)
    text_splitter = TokenTextSplitter(chunk_size=1028, chunk_overlap=0)
    split_docs = text_splitter.split_documents([text])
    return split_docs

def process_youtube_link(youtube_link):
    response = requests.get(youtube_link)
    xml_data = response.content
    root = ET.fromstring(xml_data)
    namespaces = {
        "atom": "http://www.w3.org/2005/Atom",
        "media": "http://search.yahoo.com/mrss/",
    }
    youtube_links = [
                        link.get("href")
                        for link in root.findall(".//atom:link[@rel='alternate']", namespaces)
                    ][1:]
    all_docs = []
    for link in youtube_links:
        loader = YoutubeLoader.from_youtube_url(link)
        docs = loader.load()
        all_docs.extend(docs)
    text_splitter = TokenTextSplitter(chunk_size=128, chunk_overlap=0)
    split_docs = text_splitter.split_documents(all_docs)
    return split_docs
