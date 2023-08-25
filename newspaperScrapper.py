import os
import requests
from urllib.parse import urlparse
from datetime import datetime, timedelta
import logging
from PIL import Image
from io import BytesIO
import json
import argparse

class NewspaperDownloader:
    def __init__(self, storage_path, date_format):
        self.output_main_directory = storage_path
        self.date_format = date_format

        # Configure logging
        logging.basicConfig(filename="error_log.txt", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")


    def download_image_for_timeperiod(self, start_date, end_date):
        # Define the output format
        output_format = self.date_format

        # Loop through the dates
        current_date = start_date
        while current_date <= end_date:
            formatted_date = current_date.strftime(output_format)
            print(formatted_date)
            # fetch newspaper images by date wise
            self.fetch_and_store_images(formatted_date)
            
            # Increment the current date by one day
            current_date += timedelta(days=1)

    def fetch_and_store_images(self, date):
        raise NotImplementedError("Subclasses must implement this method")

class AnandaBazar(NewspaperDownloader):
    def __init__(self, storage_path):
        super().__init__(storage_path, date_format="%d%m%Y")

    def fetch_and_store_images(self, date):

        output_directory = "/".join([self.output_main_directory, 'Bengali'])

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Convert the input date string to a datetime object
        date_object = datetime.strptime(date, "%d%m%Y")
        # Format the datetime object as a string in the desired format
        formatted_date = date_object.strftime("%Y_%m_%d")  # Example format: YYYY_MM_DD

        for i in range(1, 22):

            # URL of the image you want to fetch
            image_url = f"https://epaper.anandabazar.com/epaperimages////{date}////{date}-md-hr-{i}ll.png"

            # Parse the URL to extract the image name
            parsed_url = urlparse(image_url)
            image_name = os.path.basename(parsed_url.path)

            article_image_name = 'anandabazar_'+str(formatted_date)+'_'+image_name

            # Full path to save the image
            image_path = os.path.join(output_directory, article_image_name)

            try:
                # Send an HTTP GET request to the image URL
                response = requests.get(image_url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Read the image content from the response
                    image_content = response.content

                    # Create a PIL Image object from the image content
                    image = Image.open(BytesIO(image_content))

                     # Save the image in the specified directory
                    image.save(image_path)

                    print("Image fetched and processed successfully.")

                else:
                    print("Failed to fetch the image")

            except Exception as e:
                error_message = f"An error occurred in iteration {i}: {e}"
                print(error_message)
                logging.error(error_message)
                break

class VijayVani(NewspaperDownloader):
    def __init__(self, storage_path):
        super().__init__(storage_path, date_format="%Y%m%d")

    def fetch_and_store_images(self, date):

        output_directory = "/".join([self.output_main_directory, 'Kannada'])

        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        # Convert the input date string to a datetime object
        date_object = datetime.strptime(date, "%Y%m%d")
        # Format the datetime object as a string in the desired format
        formatted_date = date_object.strftime("%Y_%m_%d")  # Example format: YYYY_MM_DD

        # URL of the image you want to fetch
        image_url = f"https://www.enewspapr.com/OutSourcingData.php?operation=getPageArticleDetails&selectedIssueId=VVAANINEW_HUB_{date}&data=0"

        try:
            # Send an HTTP GET request to the image URL
            response = requests.get(image_url)

            if response.status_code == 200:
                response_content = response.content
                # Decode UTF-8 bytes to Unicode, and convert single quotes 
                # to double quotes to make it valid JSON
                response_content_decode = response_content.decode('utf8').replace("'", '"')

                # Load the JSON to a Python list & dump it back out as formatted JSON
                response_content_json = json.loads(response_content_decode)

                if response_content_json:
                    for articles in response_content_json:
                        for article in articles['Articles']:
                            imagename = article['Article']['imagename']
                            article_image_name_with_ext = imagename.rsplit('/', 1)[-1]
                            article_image_name = 'vivajvani_HUB_'+str(formatted_date)+'_'+article_image_name_with_ext
                            image_url = f"https://www.enewspapr.com/{imagename}"

                            # Full path to save the image
                            image_path = os.path.join(output_directory, article_image_name)

                            # Send an HTTP GET request to the image URL
                            response = requests.get(image_url)

                            # Check if the request was successful (status code 200)
                            if response.status_code == 200:
                                # Read the image content from the response
                                image_content = response.content

                                # Create a PIL Image object from the image content
                                image = Image.open(BytesIO(image_content))

                                # Save the image in the specified directory
                                image.save(image_path)

                                print("Image fetched and processed successfully.")

                            else:
                                print("Failed to fetch the image")

        except Exception as e:
            error_message = f"An error occurred in iteration {i}: {e}"
            print(error_message)
            logging.error(error_message)

def main():
    parser = argparse.ArgumentParser(description="Download newspaper images")
    parser.add_argument("newspaper", choices=["anandabazar", "vijayvani"], help="Name of the newspaper")
    parser.add_argument("start_date", help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", help="End date in YYYY-MM-DD format")
    args = parser.parse_args()

    # Directory where images gets stored
    output_main_directory = "IMAGES"
    # Define the start and end dates for the loop
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") # YYYY, MM, DD
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d") # YYYY, MM, DD

    if args.newspaper == "anandabazar":
        downloader = AnandaBazar(output_main_directory)
    elif args.newspaper == "vijayvani":
        downloader = VijayVani(output_main_directory)
    else:
        print("Invalid newspaper name")
        return

    # Call the download_image method to download and save the image
    downloader.download_image_for_timeperiod(start_date, end_date)

if __name__ == "__main__":
    main()