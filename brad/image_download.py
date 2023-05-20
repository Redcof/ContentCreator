import requests
from pexels import Pexels

# Create a Pexels object
pexels = Pexels()

# Get a random image
image = pexels.get_random_image()

# Download the image
response = requests.get(image.url)

# Save the image to a file
with open("image.jpg", "wb") as f:
    f.write(response.content)

print("Image downloaded successfully!")