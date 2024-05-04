from github import Github
import requests
import os
import concurrent.futures
import time


class GithubScraper:
    """
    Class GithubScraper provides functionality to scrape .md files from a specific repository and directory.
    """
    def __init__(self, access_token, repo_owner, repo_name, sub_dir, local_dir="../ModelCards"):
        """
        Constructor to initialize GithubScraper.
        """
        self.github_instance = Github(access_token)
        self.repo = self.github_instance.get_repo(f"{repo_owner}/{repo_name}")
        self.sub_dir = sub_dir
        self.local_dir = local_dir
        os.makedirs(self.local_dir, exist_ok=True)

    def save_file(self, content_file):
        """
        Saves the file from a given URL to the local directory.
        """
        # Define local file path
        local_file_path = f'{self.local_dir}/{content_file.name}'

        # Check if file already exists
        if os.path.isfile(local_file_path):
            print(f"File {content_file.name} already exists. Skipping download.")
            return

        # If file does not exist, download and save it
        response = requests.get(content_file.download_url)
        with open(f'{self.local_dir}/{content_file.name}', 'wb') as file:
            file.write(response.content)
        print(f"File {content_file.name} downloaded to {self.local_dir}")

    def process_directory(self, path):
        """
        Process the directory and calls itself recursively if a directory is found.
        If a .md file is found, calls save_file method.
        """
        contents = self.repo.get_contents(path)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for content_file in contents:
                if content_file.type == "dir":
                    self.process_directory(content_file.path)
                elif content_file.name.endswith(".md"):
                    executor.submit(self.save_file, content_file)

    def scrape(self):
        """
        Public method to start the scraping process.
        """
        self.process_directory(self.sub_dir)

    def txt_to_html(self, file_name):
        """
        Converts the combined.txt file to a .html file.
        """
        # Define input and output paths
        input_file = file_name
        output_file = '../Document_Source/model_cards.html'

        # Read text file
        with open(input_file, 'r') as f:
            text = f.read()

        # Wrap text in HTML tags
        html = '<html>\n<body>\n<p>\n' + text + '\n</p>\n</body>\n</html>'

        # Write HTML to file
        with open(output_file, 'w') as f:
            f.write(html)

    def combine_md_files(self, output_filename="combined.txt"):
        """
        Combines all .md files text into a single .txt file.
        """
        # delete file if exists
        if os.path.isfile(output_filename):
            os.remove(output_filename)

        with open(output_filename, 'w') as outfile:
            for md_file in os.listdir(self.local_dir):
                if md_file.endswith('.md'):
                    with open(f"{self.local_dir}/{md_file}", 'r') as infile:
                        outfile.write(infile.read())
                        outfile.write("\n\n")

        self.txt_to_html(output_filename)
        print(f"All .md files combined into {output_filename} and {output_filename} converted to .html in src/data/sDocument_Source")

    



# This script uses a ThreadPoolExecutor to download and write files concurrently. 
# The submit method of the executor starts a new thread and calls self.save_file on that thread.
if __name__ == "__main__":
    # Your personal Github Access Token
    ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

    # Owner and name of the repository you want to scrape
    REPO_OWNER = "JohnSnowLabs"
    REPO_NAME = "johnsnowlabs"

    # Sub-directory in the repository from where you want to start scraping
    SUB_DIR = "docs/_posts"

    # Create a GithubScraper instance and start scraping
    scraper = GithubScraper(ACCESS_TOKEN, REPO_OWNER, REPO_NAME, SUB_DIR)

    scraper.scrape()

    # start = time.perf_counter()

    # Combine all .md files into a single .txt file
    scraper.combine_md_files()

    # end = time.perf_counter()
    # print(f"Finished in {round(end-start, 2)} second(s)")
