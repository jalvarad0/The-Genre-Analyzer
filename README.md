# The Problem: "The Genre Analyzer"
Objective: Your client wants to analyze the pricing strategy of the "Travel" and "Mystery" genres on a competitor's bookstore. You need to scrape the books from these specific categories, clean the data, and produce a visualization comparing the average prices or price distribution.

# Technical Constraints (The OOP Requirement): You cannot write a single script. You must design a modular system using Classes. Your solution must include:

* Book: A data class to hold individual book state.
* WebScraper: An abstract base class (or interface) that defines a scraping contract.
* CategoryScraper: A concrete implementation that handles pagination (if applicable) and extraction.
* DataVisualizer: A class dedicated solely to rendering the output.

# Libraries Allowed:
* requests
* beautifulsoup4
* matplotlib (or seaborn)