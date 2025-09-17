# Scrapes OWASP Top 10 security risks

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def main():
    print("Scraping OWASP Top 10 Security Risks...")

    # Set up Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        # Load the OWASP Top 10 page
        url = "https://owasp.org/www-project-top-ten/"
        driver.get(url)

        # Wait for page to load
        time.sleep(3)

        # Find all vulnerability items using XPath
        # The vulnerabilities are in a list with specific class names
        vulnerabilities = driver.find_elements(By.XPATH, "//div[contains(@class, 'topten__item')]")

        print(f"Found {len(vulnerabilities)} vulnerabilities")

        # List to store results
        results = []

        # Extract data from each vulnerability
        for vuln in vulnerabilities:
            try:
                # Extract title and link
                title_element = vuln.find_element(By.TAG_NAME, "a")
                title = title_element.text.strip()
                link = title_element.get_attribute("href")

                # Add to results
                results.append({
                    "Vulnerability": title,
                    "Link": link
                })

                print(f"Extracted: {title}")

            except Exception as e:
                print(f"Error extracting vulnerability: {e}")
                continue

        # Create DataFrame and save to CSV
        df = pd.DataFrame(results)
        df.to_csv("owasp_top_10.csv", index=False)
        print("\nSaved OWASP Top 10 to owasp_top_10.csv")

        # Print results
        print("\nOWASP Top 10 Security Risks:")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['Vulnerability']}")

    except Exception as e:
        print(f"Error during scraping: {e}")

    finally:
        driver.quit()
        print("\nBrowser closed. OWASP scraping completed!")

if __name__ == "__main__":
    main()