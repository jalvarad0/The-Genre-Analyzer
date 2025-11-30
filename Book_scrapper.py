from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from enum import Enum
import json


class Rating(Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


# This class will scrape all books from the webpage


class Book:
    def __init__(self, title: str, price: float, rating: int):
        self.title = title
        self.price = price
        self.rating = rating

    def __repr__(self):
        return f"<{self.title} (${self.price}) ({self.rating})>"


class BaseScraper(ABC):
    """Abstract base class to enforce scraper structure."""

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def get_soup(self, url):
        """Helper to get soup object from URL."""
        response = self.session.get(url)
        if response.status_code == 200:
            return BeautifulSoup(response.text, "html.parser")
        print(f"Failed to get get data from {url}")
        return None

    @abstractmethod
    def scrape(self) -> list[Book]:
        """Must return a list of Book objects."""
        pass


# 3. IMPLEMENTATION


class CategoryScraper(BaseScraper):
    def __init__(self, category_url):
        super().__init__(category_url)
        self.books = []

    def scrape(self) -> list[Book]:
        # 1. Fetch the page (handle pagination if you want extra credit,
        #    but single page is fine for MVP).
        soup = self.get_soup(self.base_url)

        # 2. Find all book articles (look for <article class="product_pod">).
        books = soup.find_all(class_="product_pod")

        # 3. Extract Title, Price (remove the £ symbol and convert to float),
        #    and Rating (convert "Three" class to int 3 or keep as string).
        for book in books:
            # Get the title
            title = book.find(href=True).img.get("alt")
            # Get the price
            price = book.find(class_="price_color").text[2:]
            # Get the rating
            rating = Rating[
                book.find("p", class_=re.compile(r"star-rating"))["class"][1]].value
            b = Book(title, price, rating)
            # 4. Create Book objects and append to self.books.
            self.books.append(b)

# 4. VISUALIZATION
class DataVisualizer:
    @staticmethod
    def plot_price_distribution(genre_to_books: dict[str, list]):
        all_rows = []
        # 1. Map all genre to prices.
        for genre, books in genre_to_books.items():
            for b in books:
                all_rows.append({
                    "price":b.price,
                    "genre":genre
                    })
        df = pd.DataFrame(all_rows)
        # 2. Use matplotlib to create a histogram or boxplot.
        sns.boxplot(data=df, x="genre", y="price")
        # 3. Label axes and show the plot.clear
        plt.title(f"Price distribution by genre")
        plt.xlabel("Genre")
        plt.ylabel("Prices")
        plt.show()




# MAIN DRIVER
if __name__ == "__main__":
    # URLs for 'Travel' and 'Mystery' (Sandbox URLs)
    travel_url = ("http://books.toscrape.com/catalogue/category/books/travel_2/index.html")
    mystery_url = ("http://books.toscrape.com/catalogue/category/books/mystery_3/index.html")

    # Logic to instantiate scraper, get data, and visualize
    print("Starting Job...")

    # Initialize Scrapers -> Get Books
    travelBookScraper = CategoryScraper(travel_url)
    travelBookScraper.scrape()
    mysteryBookScraper = CategoryScraper(mystery_url)
    mysteryBookScraper.scrape()

    #Visualize the data
    dataVisualizer = DataVisualizer()
    genre_to_list = {'Travel':travelBookScraper.books, 'Mystery':mysteryBookScraper.books}
    dataVisualizer.plot_price_distribution(genre_to_list)

    
