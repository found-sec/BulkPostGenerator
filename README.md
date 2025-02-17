<div align="center">

# Bulk Post Generator

### Create posts in bulk within seconds, ensuring neatness and organization.
<img src="https://github.com/user-attachments/assets/91e69de7-fdb3-4053-bf8a-6bad54373bdb" width="300"/>
</div>

## Features

- Overlay random quotes on images.
- Customizable text styles.
- Add logos or trademarks to images.
- Automatically saves the generated posts to an `out/` folder.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/found-sec/BulkPostGenerator.git
   cd BulkPostGenerator
   ```
2. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
    
# API Ninjas Image Quote Generator

This Python script overlays quotes fetched from the API Ninjas API onto images. It provides customization options such as adding a logo, trademark text, and applying a color tint to the images.


- **Fetch Quotes**: Retrieves quotes from the API Ninjas API for a specified author.
- **Image Handling**: Resizes images and overlays quotes with text wrapping.
- **Quote Overlay**: Places the fetched quote at the center of the image.
- **Customization**: Option to add a logo and trademark text to the images.
- **Batch Processing**: Generate multiple image-quote combinations or use a random image for each quote.
- **Image Tint**: Apply a custom color tint to the images.
- **Output**: Saves processed images in the `out` folder.

1. Run the script:
    ```bash
    python api_ninjas_specific.py
    ```

2. Follow the prompts:
    - Enter the author's name.
    - Specify how many quotes to fetch.
    - Choose whether to generate all combinations or random selections.

# Forismatic Image Quote Generator

This Python script overlays quotes fetched from the Forismatic API onto images. It provides customization options such as adding a logo, trademark text, and applying a color tint to the images.

## Features

- **Fetch Quotes**: Retrieves random quotes from the Forismatic API.
- **Image Handling**: Resizes images and overlays quotes with text wrapping.
- **Quote Overlay**: Places the fetched quote at the center of the image.
- **Customization**: Option to add a logo and trademark text to the images.
- **Batch Processing**: Generate multiple image-quote combinations or use a random image for each quote.
- **Image Tint**: Apply a custom color tint to the images.
- **Output**: Saves processed images in the `out` folder.

## Usage

1. Run the script:
    ```bash
    python forismatic_random.py
    ```

2. Follow the prompts:
    - Specify the number of quotes to generate.
    - Choose whether to generate all combinations or random selections of quotes.
    - Decide whether to include a trademark/logo on the images.

# Image Quote Generator from File

This Python script overlays quotes from a file onto images. It provides options for customizing the images with logos, trademark text, and color tint effects.

## Features

- **Load Quotes**: Reads quotes from a text file (`quotes.txt`).
- **Image Handling**: Resizes images and overlays quotes with text wrapping.
- **Quote Overlay**: Places the quote at the center of the image.
- **Customization**: Option to add a logo and trademark text to the images.
- **Batch Processing**: Generate combinations of images and quotes or randomly select one quote for each image.
- **Image Tint**: Apply a custom color tint to the images.
- **Output**: Saves processed images in the `out` folder.

## Usage

1. Run the script:
    ```bash
    python post_generator.py
    ```

2. Follow the prompts:
    - Specify whether to generate all combinations of images and quotes or select one quote per image.
    - Decide whether to include a trademark/logo on the images.

3. Ensure your quotes are saved in the `quotes.txt` file in the `in` folder and images are located in the `in/raw` folder.

4. Processed images will be saved in the `out` folder.



## Customization

- You can modify the script to change the tint color applied to images by editing the `apply_tint()` function.


## Notes

- Ensure that the `in/raw` directory contains the image files you want to use.
- Processed images will be saved in the `out` directory.
- utils/BebasNeue.otf is the font being used in the posts, it can be changed with any font file.
- -YOUR_TRADEMARK can be replaced with eg your social handles.
- shelby.png can be replaced with your desired logo.

## License
This project uses the MIT license.
