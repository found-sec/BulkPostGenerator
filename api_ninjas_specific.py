import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
import textwrap
import random

# Function to get image paths from a directory
def get_im_paths(dir_path):
    return [os.path.join(dir_path, file) for file in os.listdir(dir_path) if os.path.splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png']]

# Function to apply a tint color to the image
def apply_tint(im, tint_color):
    if im.mode != 'RGB':
        im = im.convert('RGB')
    
    # Create a tint image with the same size as the background image
    tint_image = Image.new('RGB', im.size, tint_color)
    
    # Apply the tint
    tinted_im = ImageChops.multiply(im, tint_image)
    
    # Enhance the brightness of the tinted image
    tinted_im = ImageEnhance.Brightness(tinted_im).enhance(0.6)
    
    return tinted_im

# Function to fetch quotes from the API
def get_quotes_from_api(author_name, num_quotes):
    api_key = 'lsF7Veyacbi2n4M4lix2ow==apdeMV6V2St8Ec1X'  # Replace with your actual API key
    quotes = []
    try:
        for _ in range(num_quotes):
            url = f'https://api.api-ninjas.com/v1/quotes?author={author_name}'
            headers = {'X-Api-Key': api_key}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    quotes.append(f"{data[0]['quote']} - {author_name}")
                else:
                    print("No quote returned in API response.")
            else:
                print(f"Failed to fetch quote. HTTP {response.status_code}: {response.text}")
        return quotes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quotes from API: {e}")
        return []

# Function to resize the logo
def resize_logo(logo, max_width, image_width):
    logo_width, logo_height = logo.size
    if logo_width > max_width:
        aspect_ratio = logo_height / logo_width
        new_height = int(max_width * aspect_ratio)
        logo = logo.resize((max_width, new_height), Image.Resampling.LANCZOS)
    return logo

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

# Function to place trademark at the bottom of the image
def place_trademark(im, trademark, font):
    draw = ImageDraw.Draw(im)
    W, H = im.size
    text_width, text_height = draw.textbbox((0, 0), trademark, font=font)[2:]
    x = (W - text_width) / 2
    y = H - text_height - 10  # 10 pixels from the bottom
    draw.text((x, y), trademark, font=font, fill="white")
    return im

# Function to place logo at the bottom-center of the image
def place_logo(im, logo, trademark, font):
    W, H = im.size
    logo_width, logo_height = logo.size
    draw = ImageDraw.Draw(im)
    text_width, text_height = draw.textbbox((0, 0), trademark, font=font)[2:]
    spacing = 10  # Increase spacing to give room for the logo
    
    # Resize the logo to a smaller size (e.g., 15% of the image width)
    logo_size = int(W * 0.2)  # 20% of the background image width
    logo = logo.resize((logo_size, int(logo.size[1] * logo_size / logo.size[0])), Image.Resampling.LANCZOS)
    logo_width, logo_height = logo.size
    
    # Center the logo horizontally and place it near the bottom with extra space for the trademark
    x_position = (W - logo_width) // 2
    y_position = H - logo_height - text_height - spacing  # Place it above the trademark

    # Ensure logo has an alpha channel for transparency handling
    logo = logo.convert("RGBA")
    im.paste(logo, (x_position, y_position), logo)  # Use logo as the mask for transparency
    return im

# Main function to orchestrate the process
def main():
    input_dir = "in/raw"
    output_dir = "out"
    cap_font_path = "utils/BebasNeue.otf"
    tm_font_path = "utils/BebasNeue.otf"
    logo_path = "shelby.png"
    W, H = 1080, 1080

    im_paths = get_im_paths(input_dir)

    if not im_paths:
        print(f"No image files found in {input_dir}. Exiting...")
        return

    author_name = input("Enter author's name (e.g., Aristotle): ").strip()
    num_quotes = int(input("How many quotes would you like to fetch? ").strip())
    quotes = get_quotes_from_api(author_name, num_quotes)

    if not quotes:
        print(f"No quotes found for author '{author_name}'. Exiting...")
        return

    quotes = [' '.join(quote.split()[:20]) for quote in quotes]  # Limit quotes to 20 words
    generate_all_combinations = input("Generate all combinations? (y/n): ").strip().lower() == 'y'
    add_logo = input("Include logo? (y/n): ").strip().lower() == 'y'
    add_trademark = input("Include trademark? (y/n): ").strip().lower() == 'y'

    for i, selected_quote in enumerate(quotes):
        if generate_all_combinations:
            im_count = 0
            for im_path in im_paths:
                print(f"Overlaying {im_path} with quote: {selected_quote}")
                im = Image.open(im_path).resize((W, H))
                im = apply_tint(im, (200, 200, 200))  # Apply the tint

                draw = ImageDraw.Draw(im)
                cap_font = ImageFont.truetype(cap_font_path, 115)

                # Place the quote
                place_quote(im, selected_quote, cap_font)

                # Place trademark if necessary
                if add_trademark:
                    trademark = "YOUR_TRADEMARK"
                    tm_font = ImageFont.truetype(tm_font_path, 52)
                    place_trademark(im, trademark, tm_font)

                # Place logo if necessary
                if add_logo and logo_path:
                    try:
                        logo = Image.open(logo_path).convert("RGBA")
                        logo = resize_logo(logo, W // 5, W)  # Resize logo to max 1/5th of image width
                        im = place_logo(im, logo, trademark, tm_font)
                    except FileNotFoundError:
                        print(f"Logo file not found at {logo_path}. Skipping logo placement.")
                    except Exception as e:
                        print(f"Error placing logo: {e}")

                os.makedirs(output_dir, exist_ok=True)
                file_name = f"{im_count}_{selected_quote[:10].replace(' ', '_')}.png"
                im.save(os.path.join(output_dir, file_name), format='PNG', quality=95)
                print(f"Output image saved as: {os.path.join(output_dir, file_name)}")
                im_count += 1
        else:
            im_path = random.choice(im_paths)
            print(f"Overlaying {im_path} with quote: {selected_quote}")
            im = Image.open(im_path).resize((W, H))
            im = apply_tint(im, (200, 200, 200))  # Apply the tint

            draw = ImageDraw.Draw(im)
            cap_font = ImageFont.truetype(cap_font_path, 115)

            # Place the quote
            place_quote(im, selected_quote, cap_font)

            # Place trademark if necessary
            if add_trademark:
                trademark = "YOUR_TRADEMARK"
                tm_font = ImageFont.truetype(tm_font_path, 52)
                place_trademark(im, trademark, tm_font)

            # Place logo if necessary
            if add_logo and logo_path:
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo = resize_logo(logo, W // 5, W)  # Resize logo to max 1/5th of image width
                    im = place_logo(im, logo, trademark, tm_font)
                except FileNotFoundError:
                    print(f"Logo file not found at {logo_path}. Skipping logo placement.")
                except Exception as e:
                    print(f"Error placing logo: {e}")

            os.makedirs(output_dir, exist_ok=True)
            file_name = f"{i}_{selected_quote[:10].replace(' ', '_')}.png"
            im.save(os.path.join(output_dir, file_name), format='PNG', quality=95)
            print(f"Output image saved as: {os.path.join(output_dir, file_name)}")

if __name__ == "__main__":
    main()
