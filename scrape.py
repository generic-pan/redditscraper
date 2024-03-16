import requests

# Note: changes in Reddit API may have altered the effectiveness of the script

counter = 0
ops = []
subreddit = "pics"

response = requests.get("https://www.reddit.com/r/" + subreddit + "/hot.json", headers={"User-Agent": "Mozilla/5.0"})
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    posts = data['data']['children'][:100]
    for post in posts:
        if counter < 5:
            url = post['data']['url']
            if ".jpg" in url or ".png" in url and counter < 5:
                # Download the image
                image_response = requests.get(url)
                if image_response.status_code == 200:
                    file_extension = url.split(".")[-1]
                    file_name = f"{counter}.jpg"
                    
                    with open(file_name, "wb") as file:
                        file.write(image_response.content)
                    ops.append(post['data']['author'])
                    print(f"Downloaded {file_name}")
                    counter += 1
                else:
                    print(f"Failed to download image from {url}")
            
else:
    print("Request failed with status code:", response.status_code)
    
from PIL import Image, ImageDraw, ImageFont

def resize_image(image_path, max_width, max_height):
    image = Image.open(image_path)
    width, height = image.size

    # Calculate aspect ratios
    aspect_ratio = width / height
    target_ratio = max_width / max_height

    # Calculate new dimensions
    if aspect_ratio > target_ratio:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)
    else:
        new_width = int(max_height * aspect_ratio)
        new_height = max_height

    # Resize and center the image
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    padded_image = Image.new('RGB', (max_width, max_height), (0, 0, 0))
    offset = ((max_width - new_width) // 2, (max_height - new_height) // 2)
    padded_image.paste(resized_image, offset)

    return padded_image

def add_centered_text_with_border(image_path, text, font_size, border_size, output_path):
    # Open the image
    image = Image.open(image_path)

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(image)

    try:
        # Try to use Arial font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to a default font if Arial is not available
        font = ImageFont.load_default().font

    # Determine the text size
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position for the text
    image_width, image_height = image.size
    x = (image_width - text_width) // 2
    y = image_height - text_height - 300

    # Draw the black border
    border_coordinates = [
        (x - border_size, y - border_size),
        (x + text_width + border_size, y + text_height + border_size)
    ]
    draw.rectangle(border_coordinates, fill="black")

    # Draw the centered text
    draw.text((x, y), text, font=font, fill="white")

    # Save the modified image
    image.save(output_path)

from PIL import Image, ImageDraw, ImageFont

def add_top_centered_text_with_border(image_path, text, font_size, border_size, output_path):
    # Open the image
    image = Image.open(image_path)

    # Create a new ImageDraw object
    draw = ImageDraw.Draw(image)

    try:
        # Try to use Arial font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback to a default font if Arial is not available
        font = ImageFont.load_default().font

    # Determine the text size
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position for the text
    image_width, image_height = image.size
    x = (image_width - text_width) // 2
    y = 200  # 200 pixels from the top

    # Draw the black border
    border_coordinates = [
        (x - border_size, y - border_size),
        (x + text_width + border_size, y + text_height + border_size)
    ]
    draw.rectangle(border_coordinates, fill="black")

    # Draw the centered text
    draw.text((x, y), text, font=font, fill="white")

    # Save the modified image
    image.save(output_path)



for i in range(6):
    image_path = f'{i}.jpg'
    max_width = 1080
    max_height = 1920
    resized_image = resize_image(image_path, max_width, max_height)
    resized_image.save(f'{i}_resized.jpg')
    if i == 0:
        add_top_centered_text_with_border(f'{i}_resized.jpg', "Your Daily r/" + subreddit, 68, 5, f'{i}_raw.jpg')
        add_centered_text_with_border(f'{i}_raw.jpg', "By u/"+ ops[i], 68, 5, f'{i}_captioned.jpg')
    elif i == len(ops):
        add_top_centered_text_with_border(f'{i}_resized.jpg', "", 68, 5, f'{i}_captioned.jpg')
    else:
        add_centered_text_with_border(f'{i}_resized.jpg', "By u/"+ ops[i], 68, 5, f'{i}_captioned.jpg')
import subprocess
import shlex

# Command to create the slideshow video using ffmpeg
command = "ffmpeg -y -framerate 2/5 -i %d_captioned.jpg -vf 'fps=25' -c:v libx264 -r 25 -pix_fmt yuv420p output.mp4"

# Split the command into a list of arguments
args = shlex.split(command)

# Execute the command
subprocess.run(args)



desc = [""""""]

import subprocess
import random
randint = random.choice([*range(5)])

# Provide the paths to your video, audio, and output files
video_path = 'output.mp4'
audio_path = f'{randint}.mp3'
output_path = 'final.mp4'

print(desc[randint])

import shlex
subprocess.run(shlex.split(f"ffmpeg -y -i output.mp4 -ss 15 -i {audio_path} -c copy -map 0:v:0 -map 1:a:0 -t 17.5 final.mp4"))


print(desc[randint])
