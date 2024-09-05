import requests
import bs4 as bs
from dateutil import parser
from pytz import timezone
from dataclasses import dataclass

class EasyRSS():
    def __init__(self, feed_url:str):
        self.articles = []
        self.feed = feed_url

    def get_news(self):
        self.articles = []
        xml = requests.get(self.feed, timeout=10)
        if (xml.status_code != 200):
            raise ConnectionError(f"({xml.status_code}) error getting feed from {self.feed} \n [ {xml.content} ]", )
        
        soup = bs.BeautifulSoup(xml.content, "xml")
        return self._process(soup)
    
    def _process(self, soup:bs.BeautifulSoup):
        if soup.find("feed"):
            self.articles = self._parse_atom(soup)
        else:
            self.articles = self._parse_rss(soup)
        
        return self.articles
    
    def _parse_rss(self, soup:bs.BeautifulSoup):
        items = soup.find_all('item')
        articles = []
        for tag in items:
            articles.append(self._create_item(tag))
        return articles

    def _parse_atom(self, soup:bs.BeautifulSoup):
        items = soup.find_all('entry')
        articles = []
        for tag in items:
            articles.append(self._create_entry(tag))
        return articles

    def _create_item(self, tag:bs.element.Tag):
        title = tag.find('title').text if tag.find('title') else "" 
        date = tag.find('pubDate').text if tag.find('pubDate') else None
        desc = tag.find('description').text if tag.find('description') else ""
        link = tag.find("link").text if tag.find("link") else None

        return Item(title, link, date, desc)
    
    def _create_entry(self, tag:bs.element.Tag):
        title = tag.find('title').text if tag.find('title') else "" 
        date = tag.find('published').text if tag.find('published') else None
        desc = tag.find('summary').text if tag.find('summary') else ""
        link = tag.find("link").text if tag.find("link") else None
        authors = [ author.find('name').text for author in tag.find_all("author") if author.find('name')]
        return Entry(title, link, date, desc, authors)
    
@dataclass
class Entry:
    title:str
    link:str 
    published:str 
    summary:str 
    authors:list 
    def __post_init__(self):
        self.summary = self.summary.strip()
        if self.published:
            self.published = parser.parse(self.published.strip())
            self.published = self.published.astimezone(timezone('US/Eastern'))
            self.published = self.published.strftime("%b %d, %Y %I:%M%p")

@dataclass
class Item:
    title:str
    link:str 
    pubDate:str 
    description:str 
    def __post_init__(self):
        self.description = self.description.strip()
        if self.pubDate:
            self.pubDate = parser.parse(self.pubDate.strip())
            self.pubDate = self.pubDate.astimezone(timezone('US/Eastern'))
            self.pubDate = self.pubDate.strftime("%b %d, %Y %I:%M%p")
