import requests
import os

# Set up the Pexels API key
API_KEY = "oOIT1S8sKtQqSf9pJxC1u5xhp1YlbguB3HqQpunjANvY0WcFq02irYH2"


def image_get_pexels(search_query_, no_images, output_dir):
    # Set the search query and the number of images to download
    search_query = search_query_
    num_images = no_images

    # Set the output directory to save the downloaded images
    output_directory = output_dir

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Construct the URL to request images from the Pexels API
    url = f"https://api.pexels.com/v1/search?query={search_query}&per_page={num_images}"

    # Set the headers with the API key
    headers = {"Authorization": API_KEY}

    # Send the HTTP GET request to retrieve the images
    response = requests.get(url, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Iterate over the images in the response
        for i, image_info in enumerate(data["photos"]):
            # Get the URL of the image
            image_url = image_info["src"]["large"]

            # Send another request to download the image
            image_response = requests.get(image_url, verify=False)

            # Save the image to the output directory
            image_path = os.path.join(output_directory, f"{search_query}_{i + 1}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_response.content)

            print(f"Downloaded image {i + 1}/{num_images}: {image_path}")
    else:
        print(f"Error retrieving images. Status code: {response.status_code}")
