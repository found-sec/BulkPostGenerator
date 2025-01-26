import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
import textwrap
import time  # Import time module for delay

import re

# Function to fetch a random quote from Forismatic API
def get_random_quote():
    try:
        response = requests.get(
            'https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
        )
        if response.status_code == 200:
            data = response.json()
            quote = data.get('quoteText', '').strip()
            author = data.get('quoteAuthor', 'Unknown').strip()

            # Sanitize the quote text by escaping problematic characters
            if quote:
                quote = re.sub(r'\\([^\n])', r'\\\\\1', quote)  # Escape backslashes
                return f"{quote}\n- {author}" if quote else None
            else:
                return None
        else:
            print(f"Failed to fetch quote. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote from API: {e}")
        return None

# Function to get paths of image files from a directory
def get_im_paths(dir_path):
    return [file for file in os.listdir(dir_path) if is_img(file)]

# Function to check if a file path is an image
def is_img(file_name):
    ext = os.path.splitext(file_name)[1].lower()
    return ext in ['.jpg', '.jpeg', '.png']

# Function to apply a tint color to the image
def apply_tint(im, tint_color):
    # Ensure the image is in 'RGB' mode to avoid mode mismatch
    if im.mode != 'RGB':
        im = im.convert('RGB')
    
    # Create a new tint image with the same size as the background image
    tint_image = Image.new('RGB', im.size, tint_color)
    
    # Apply the tint
    tinted_im = ImageChops.multiply(im, tint_image)
    
    # Enhance the brightness of the tinted image
    tinted_im = ImageEnhance.Brightness(tinted_im).enhance(0.6)
    
    return tinted_im

# Function to place a logo at the bottom of the image
def place_logo(bkg, logo, trademark, font):
    bkg_width, bkg_height = bkg.size
    logo_width, logo_height = logo.size
    draw = ImageDraw.Draw(bkg)
    text_width, text_height = draw.textbbox((0, 0), trademark, font=font)[2:]
    spacing = 10  # Increase spacing to give room for the logo
    
    # Resize the logo to a smaller size (e.g., 15% of the image width)
    logo_size = int(bkg_width * 0.2)  # 20% of the background image width
    logo = logo.resize((logo_size, int(logo.size[1] * logo_size / logo.size[0])), Image.Resampling.LANCZOS)
    logo_width, logo_height = logo.size
    
    # Center the logo horizontally and place it near the bottom with extra space for the trademark
    x_position = int((bkg_width - logo_width) / 2)
    y_position = bkg_height - logo_height - text_height - spacing  # Place it above the trademark

    # Ensure logo has an alpha channel for transparency handling
    logo = logo.convert("RGBA")
    bkg.paste(logo, (x_position, y_position), logo)  # Use logo as the mask for transparency
    return bkg


# Function to place a trademark text at the bottom of the image
def place_trademark(im, trademark, font):
    draw = ImageDraw.Draw(im)
    W, H = im.size
    text_width, text_height = draw.textbbox((0, 0), trademark, font=font)[2:]
    x = (W - text_width) / 2
    y = H - text_height - 10  # 10 pixels from the bottom
    draw.text((x, y), trademark, font=font, fill="white")
    return im

# Function to place the quote in the center of the image
def place_quote(im, quote, font):
    draw = ImageDraw.Draw(im)
    W, H = im.size
    lines = textwrap.wrap(quote, width=24)
    n_lines = len(lines)
    pad = -10
    current_h = H / 2 - (n_lines * draw.textbbox((0, 0), lines[0], font=font)[3] / 2)
    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:]
        draw.text(((W - text_width) / 2, current_h), line, font=font, fill="white")
        current_h += text_height + pad

# Function to build and save the image
def build_image(im_path, quote, im_count='', include_trademark=False, include_logo=False):
    W = H = 1080
    im = Image.open(os.path.join("in", "raw", im_path)).resize((W, H))
    im = apply_tint(im, (200, 200, 200))
    draw = ImageDraw.Draw(im)
    cap_font = ImageFont.truetype("utils/BebasNeue.otf", 115)
    place_quote(im, quote, cap_font)
    
    if include_trademark:
        trademark = "YOUR_TRADEMARK"
        tm_font = ImageFont.truetype("utils/BebasNeue.otf", 52)
        place_trademark(im, trademark, tm_font)
    
    if include_logo:
        try:
            logo = Image.open("shelby.png")  # Replace with actual path to logo file
            place_logo(im, logo, trademark, tm_font)
        except Exception as e:
            print(f"Error loading logo: {e}")

    if not os.path.exists("out"):
        os.makedirs("out")
    
    file_name = f"{im_count}_{quote[:10].replace(' ', '_')}.png"
    im.save(f'out/{file_name}')
    print(f"Output image saved as: out/{file_name}")

def main():
    dir_paths = "in/raw"
    im_paths = get_im_paths(dir_paths)
    
    if not im_paths:
        print(f"No image files found in {dir_paths}. Exiting...")
        return
    
    # Ask for the number of quotes to fetch
    num_quotes = int(input("How many quotes would you like to generate? ").strip())
    
    # Ask whether to include trademark
    include_trademark = input("Include trademark? (y/n): ").strip().lower() == 'y'
    
    # Ask whether to include logo
    include_logo = input("Include logo? (y/n): ").strip().lower() == 'y'
    
    # Ensure that only the specified number of images are processed
    im_paths = im_paths[:num_quotes]  # Limit images to the number of quotes
    
    # Generate images for each quote
    for i, im_path in enumerate(im_paths):  # Ensure we only process the limited images
        quote = get_random_quote()  # Fetch a new quote for each image
        if quote:
            print(f"Overlaying {im_path} with quote: {quote}...")
            build_image(im_path, quote, f"{i}", include_trademark, include_logo)
            time.sleep(2)  # Add a 2-second delay after each quote is fetched
        else:
            print(f"Failed to fetch a quote for {im_path}. Skipping...")


if __name__ == "__main__":
    main()
