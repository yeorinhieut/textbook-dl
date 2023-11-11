from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import getpass

def wait_and_redirect(driver, redirect_url):
    try:
        WebDriverWait(driver, 30).until(EC.url_to_be(redirect_url))
    except Exception as e:
        print(f"Timeout waiting for redirect to {redirect_url}. Error: {e}")

def run_selenium_script(driver, url, user_data_dir, download_dir):
    driver.execute_script(f'window.open("{url}","_blank");')
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    time.sleep(20)

    try:
        script = """
        if (window.location.href === "https://webdt.edunet.net/pdf") {
            console.log("Extracting...");
        } else if (window.location.href === "https://webdt.edunet.net/viewer") {
            console.log("Viewer not supported");
        } else {
            console.log("Invalid URL.");
        }

        var scriptText = document.querySelectorAll('body > script:nth-child(35)')[0].textContent;

        var match = scriptText.match(/if \\("pdf" == "pdf"\\) {\\s+parent\\.contentInformationURL = "(.*?)";/);
        if (match) {
            var pdfLink = match[1];
            console.log("Extracted PDF link:", pdfLink);

            fetch(pdfLink, { headers: { 'Referer': 'https://webdt.edunet.net/' } })
                .then(response => response.blob())
                .then(blob => {
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = document.querySelector('#toc_bookNm').textContent + ".pdf";
                    link.click();
                })
                .catch(error => console.error("Error:", error));
        } else {
            console.log("Failed to extract PDF link");
        }
        """
        driver.execute_script(script)

        time.sleep(10)

        os.startfile(download_dir)

    finally:
        driver.close()

if __name__ == "__main__":
    username = getpass.getuser()
    user_data_directory = f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    download_directory = f'C:\\Users\\{username}\\Downloads'

    driver = webdriver.Chrome(options=webdriver.ChromeOptions())
    driver.get("https://webdt.edunet.net/login")

    input("Please log in")

    wait_and_redirect(driver, "https://webdt.edunet.net/")

    user_url = input("Enter the URL: ")

    if user_url.startswith("https://webdt.edunet.net/url/"):
        run_selenium_script(driver, user_url, user_data_directory, download_directory)
    else:
        print("Invalid URL pattern. Please provide a valid URL.")
