from dotenv import load_dotenv

# Griptape
from griptape.structures import Pipeline
from griptape.tasks import (
    PromptTask,
    PromptImageGenerationTask,
    CodeExecutionTask,
)
from griptape.artifacts import TextArtifact
from griptape.drivers import OpenAiImageGenerationDriver
from griptape.engines import PromptImageGenerationEngine
import os
import base64
import json
from io import BytesIO
from PIL import Image

load_dotenv()  # Load your environment

# Variables
output_dir = "images"

# Create the driver
image_driver = OpenAiImageGenerationDriver(model="dall-e-3", api_type="open_ai", image_size="1024x1024")

# Create the engine
image_engine = PromptImageGenerationEngine(image_generation_driver=image_driver)

# Create a function to convert b64 to jpg NOT CURRENTLY USED!
def b64_json_to_image(task: CodeExecutionTask) -> TextArtifact:
    """Converts a base64 encoded image within a JSON object to an image file."""

    data = json.loads(f'images/{task.input.value}')
    image_data = base64.b64decode(data['image'])  # Assuming 'image' key holds the base64 string
    filename = f'{task.input.value}.jpg'
    with open(filename, 'wb') as f:
        f.write(image_data)
    # return TextArtifact(filename)
    image = Image.open(BytesIO(image_data))
    return image

# Create a function to convert b64 to jpg
def b64_to_image(task: CodeExecutionTask) -> TextArtifact:
    """Converts a base64 encoded image within a JSON object to an image file."""
    #images/b38074ecf0b74103950777503debe016
    # filepath = f'images/{task.input.value}'
    # with open(filepath, 'rb') as file:
    #     b64_data = file.read()
    output_dir = task.context["output_dir"]
    imgdata = base64.b64decode(task.parent_outputs['Generate Image Task'].base64)
    filename = f"{output_dir}/{task.parent_outputs['Generate Image Task'].id}.jpg"
    with open(filename, 'wb') as f:
        f.write(imgdata)
    return TextArtifact(filename)

# Create a function to display an image
def display_image(task: CodeExecutionTask) -> TextArtifact:
    import os
    from PIL import Image

    # Get the filename
    filename = task.parents_output_text

    # # Get the output_dir
    # output_dir = task.context["output_dir"]

    # # Get the path of the image
    # image_path = os.path.join(output_dir, filename)

    # Open the image
    image = Image.open(filename)
    image.show()

    return TextArtifact(filename)


# Create the pipeline object
pipeline = Pipeline()

# Create tasks
create_prompt_task = PromptTask(
    """
    Create a prompt for an Image Generation pipeline for the following topic: 
    {{ args[0] }}
    in the style of {{ style }}.
    """,
    context={"style": "a polaroid photograph from the 1970s"},
    id="Create Prompt Task",
)

generate_image_task = PromptImageGenerationTask(
    "{{ parent_output }}",
    image_generation_engine=image_engine,
    #output_dir=output_dir,
    id="Generate Image Task",
)

convert_image_task = CodeExecutionTask(
    "{{ parent_output }}",
    on_run=b64_to_image,
    context={"output_dir": output_dir},
    id="Convert Image Task",
)

display_image_task = CodeExecutionTask(
    "{{ parent.output.name }}",
    context={"output_dir": output_dir},
    on_run=display_image,
    id="Display Image Task",
)

# Add tasks to pipeline
pipeline.add_tasks(create_prompt_task, generate_image_task, convert_image_task, display_image_task)

# Run the pipeline
pipeline.run("a cow")