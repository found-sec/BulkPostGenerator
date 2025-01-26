import os
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
import textwrap

# Function to read quotes from a file
def get_quotes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.readlines()
        return [quote.strip() for quote in content if quote.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

# Function to apply a tint color to the image
def apply_tint(im, tint_color):
    # Convert image to 'RGB' mode if not already
    if im.mode != 'RGB':
        im = im.convert('RGB')
    # Create a new image with the tint color and apply the multiply blend
    tinted_im = ImageChops.multiply(im, Image.new('RGB', im.size, tint_color))
    # Adjust brightness for the final effect
    tinted_im = ImageEnhance.Brightness(tinted_im).enhance(0.6)
    return tinted_im

# Function to place a logo at the bottom of the image
def place_logo(bkg, logo, trademark, font):
    bkg_width, bkg_height = bkg.size
    logo_width, logo_height = logo.size
    draw = ImageDraw.Draw(bkg)
    text_width, text_height = draw.textbbox((0, 0), trademark, font=font)[2:]
    spacing = 2
    x_position = int((bkg_width - logo_width) / 2)
    
    # Position the logo just above the trademark text
    y_position = bkg_height - logo_height - text_height - spacing - 10  # 10 pixels gap from text
    
    # Ensure the logo has an alpha channel
    if logo.mode != "RGBA":
        logo = logo.convert("RGBA")
    
    # Extract the alpha channel for transparency
    mask = logo.split()[3]  # Use the alpha channel as the mask
    
    bkg.paste(logo, (x_position, y_position), mask)
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

# Function to check if a file path is an image
def is_img(file_name):
    try:
        Image.open(file_name)
        return True
    except IOError:
        return False

# Function to get paths of image files from a directory
def get_im_paths(dir_path):
    return [os.path.join(dir_path, file) for file in os.listdir(dir_path) if is_img(os.path.join(dir_path, file))]

# Function to build and save the image
def build_image(im_path, quote, im_count='', logoify=True, trademarkify=True):
    W = H = 1080
    im = Image.open(im_path).resize((W, H))
    im = apply_tint(im, (200, 200, 200))
    draw = ImageDraw.Draw(im)

    cap_font = ImageFont.truetype("utils/BebasNeue.otf", 115)
    place_quote(im, quote, cap_font)

    # Add trademark/logo if requested
    if trademarkify:
        trademark = "YOUR_TRADEMARK"
        tm_font = ImageFont.truetype("utils/BebasNeue.otf", 52)
        place_trademark(im, trademark, tm_font)
    
    if logoify:
        try:
            logo = Image.open("shelby.png")  # Replace with actual path to logo file

            # Resize the logo to fit within 20% of the image width or height
            max_logo_width = W * 0.2
            max_logo_height = H * 0.2

            logo_width, logo_height = logo.size

            # Calculate the aspect ratio
            aspect_ratio = logo_width / logo_height
            if logo_width > logo_height:
                if logo_width > max_logo_width:
                    logo_width = max_logo_width
                    logo_height = logo_width / aspect_ratio
            else:
                if logo_height > max_logo_height:
                    logo_height = max_logo_height
                    logo_width = logo_height * aspect_ratio

            # Resize the logo to the new dimensions
            logo = logo.resize((int(logo_width), int(logo_height)))

            place_logo(im, logo, trademark, tm_font)
        except Exception as e:
            print(f"Error loading logo: {e}")

    # Ensure output directory exists
    if not os.path.exists("out"):
        os.makedirs("out")

    # Save the image with a unique filename
    im.save(f'out/{im_count}_{quote[:10]}.png')
    print(f"Output image saved as: out/{im_count}_{quote[:10]}.png")

# Main function to orchestrate the process
def main():
    dir_path = "in/raw"
    im_paths = get_im_paths(dir_path)
    quotes = get_quotes("in/quotes.txt")  # Adjust the path to your quotes file

    if not im_paths:
        print(f"No image files found in {dir_path}. Exiting...")
        return

    generate_all_combinations = input("Generate all combinations? (y/n): ").strip().lower() == 'y'
    
    # User input for including trademark and logo
    include_trademark = input("Include trademark? (y/n): ").strip().lower() == 'y'
    include_logo = input("Include logo? (y/n): ").strip().lower() == 'y'

    if generate_all_combinations:
        im_count = 0
        for im_path in im_paths:
            for quote in quotes:
                print(f"Overlaying {im_path} with quote: {quote}...")
                build_image(im_path, quote, im_count, include_logo, include_trademark)
            im_count += 1
    else:
        for i, im_path in enumerate(im_paths):
            if i < len(quotes):
                print(f"Overlaying {im_path} with quote: {quotes[i]}...")
                build_image(im_path, quotes[i], '', include_logo, include_trademark)
            else:
                print(f"Skipping {im_path} as there are no more quotes available")

if __name__ == "__main__":
    main()
