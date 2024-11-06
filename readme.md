# Griptape AI Image Generation Pipeline  
## Overview  
This repository contains a Python script that utilizes the Griptape library to create an image generation pipeline. The pipeline takes a text prompt as input, generates an image using OpenAI's DALL-E-3 model, and saves the image to a specified output directory.  
## Requirements  
- Python 3.9+
- OpenAI API credentials (stored in a .env file)  
## Set Up  
1. Set up a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install griptape python-dotenv pillow
   ```
## Pipeline Components
- Create Prompt Task: Creates a text prompt for image generation based on a given topic and style.
- Generate Image Task: Uses OpenAI's DALL-E-3 model to generate an image from the prompt.
- Convert Image Task: Converts the generated image from base64 to a JPEG file.
- Display Image Task: Displays the generated image.

## License
This code is available under the Apache 2.0 License.

## Contributing
Contributions are welcome! Please submit a pull request with your changes.

## Acknowledgments
This code utilizes the Griptape library and OpenAI's DALL-E-3 model. Special thanks to the developers and maintainers of these projects.