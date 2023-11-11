from selenium import webdriver
import time
import os
import getpass

def run_selenium_script(url, user_data_dir, download_dir):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        time.sleep(15)

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

        time.sleep(15)

        os.startfile(download_dir)

    finally:
        driver.quit()

if __name__ == "__main__":
    username = getpass.getuser()
    user_data_directory = f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default'
    download_directory = f'C:\\Users\\{username}\\Downloads'

    user_url = input("Enter the URL: ")

    if user_url.startswith("https://webdt.edunet.net/url/"):
        run_selenium_script(user_url, user_data_directory, download_directory)
    else:
        print("Invalid URL pattern. Please provide a valid URL.")
