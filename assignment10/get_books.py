# Web scraping script for Durham County Library
# Extracts book search results and saves to CSV and JSON

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time

def main():
    print("Starting web scraping for Durham County Library...")

    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Task 2: Load the search results page
        url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
        driver.get(url)

        # Wait for page to load
        time.sleep(3)
        #-----------------------------------------------------------------------------------------
        # Task 3: Find all book result elements
        # Based on inspecting the page structure
        book_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-list-item")

        print(f"Found {len(book_elements)} book results")

        # Create empty list for results
        results = []

        # Main loop: Extract data from each book element
        for book in book_elements:
            try:
                # Extract title
                title_element = book.find_element(By.CSS_SELECTOR, "h3.cp-title a")
                title = title_element.text.strip()

                # Extract authors (multiple possible)
                author_elements = book.find_elements(By.CSS_SELECTOR, "span.cp-author a")
                authors = [author.text.strip() for author in author_elements]
                author_text = "; ".join(authors) if authors else "Unknown Author"

                # Extract format and year
                format_element = book.find_element(By.CSS_SELECTOR, "div.cp-formats")
                format_year = format_element.text.strip()

                # Create dictionary for this book
                book_data = {
                    "Title": title,
                    "Author": author_text,
                    "Format-Year": format_year
                }

                results.append(book_data)

                # Print progress
                print(f"Extracted: {title[:50]}...")

            except Exception as e:
                print(f"Error extracting book data: {e}")
                continue

        # Create DataFrame
        df = pd.DataFrame(results)

        # Print the DataFrame
        print("\nExtracted Data:")
        print(df)
        #----------------------------------------------------------------------------------------
        # Task 4: Write to files
        # Save to CSV
        df.to_csv("get_books.csv", index=False)
        print("\nSaved data to get_books.csv")

        # Save to JSON
        with open("get_books.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print("Saved data to get_books.json")

    except Exception as e:
        print(f"Error during scraping: {e}")

    finally:
        # Close the browser
        driver.quit()
        print("\nBrowser closed. Scraping completed!")

if __name__ == "__main__":
    main()