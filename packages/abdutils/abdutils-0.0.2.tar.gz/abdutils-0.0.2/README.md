# abdutils

## abdutils: Simplifying Python File/Image Operations  (Others Coming Soon)

Are you tired of dealing with complex Python libraries and struggling with unclear learning examples? We've been there too, which is why we created `abdutils`.

## What is abdutils?

`abdutils` is a Python utility module that aims to simplify common file and folder operations, making Python programming more efficient and intuitive. We understand that Python libraries can sometimes feel overly complicated, and learning from existing examples can be challenging. That's why we're building `abdutils` to provide a straightforward and user-friendly solution.

## Why Choose abdutils?

- **Simplicity**: We believe in keeping things simple. `abdutils` offers easy-to-use functions for various file-related tasks, eliminating the need to reinvent the wheel when working with files and directories.

- **Clarity**: Our code and documentation are designed with clarity in mind. We want you to understand how everything works, making your Python development experience smoother.

- **Open to Suggestions**: We value your input! If you have suggestions, ideas, or improvements to make `abdutils` even better, please don't hesitate to [open an issue](https://github.com/abdkhanstd/abdutils/issues) or submit a [pull request](https://github.com/abdkhanstd/abdutils/pulls).

## Getting Started

To get started with `abdutils`, you can install it easily using `pip`. Here's how:

```bash
pip install --upgrade git+https://github.com/abdkhanstd/abdutils.git

```
## Purpose

- **Ease of Programming:** `abdutils` strives to streamline Python programming by providing a collection of utility functions, which currently encompass fundamental file and directory operations.

- **Enhanced File Handling:** It provides tools to perform file creation, reading, and writing tasks effortlessly.

- **Time-Saving:** By using `abdutils`, you can save time on routine file operations, allowing you to focus on the core aspects of your projects.

Whether you're a beginner or an experienced developer, `abdutils` is here to make your Python coding experience smoother and more enjoyable.

## Installation

You can install `abdutils` directly from its GitHub repository using pip:

```bash
pip install --upgrade git+https://github.com/abdkhanstd/abdutils.git

```

To verify the installation of a Python package installed via `pip` and to provide installation instructions in a GitHub README file, follow these steps:

## Verifying Installation

1. Open your terminal or command prompt.

2. Run the following command to verify if the package "abdutils" has been installed successfully:

   ```
   pip show abdutils
   ```

   This command will display information about the installed package, including its version, location, and other details. If the package is installed correctly, you'll see its information. If it's not installed, you'll receive an error message.

## Installation (Build from repository)

To install the `abdutils` package, you can use `pip`. Run the following command in your terminal or command prompt:

   ```bash
   pip install git+https://github.com/abdkhanstd/abdutils.git
   ```

   This will install the latest version of the package directly from the GitHub repository.

   If you prefer to install manually, you can follow these steps:

   1. Clone the GitHub repository:

      ```bash
      git clone https://github.com/abdkhanstd/abdutils.git
      ```

   2. Change your current directory to the cloned repository:

      ```bash
      cd abdutils
      ```

   3. Install the package using `pip`:

      ```bash
      pip install .
      ```


## Table of Contents
- [CreateFolder](#createfolder)
- [RenameFileFolder](#renamefilefolder)
- [Copy](#copy)
- [Move](#move)
- [Delete](#delete)
- [ReadFile](#readfile)
- [WriteFile](#writefile)
- [ReadImage](#readimage-function)
- [SaveImage](#saveimage-function)
- [ConvertToGrayscale](#converttograyscale-function)
- [ConvertToRGB](#converttorgb-function)
- [CropImage](#cropimage-function)
- [GetImageSize](#getimagesize-function)
- [ResizeImage](#resizeimage-function)
- [GaussianBlurImage](#gaussianblurimage-function)
- [ConvertImageToGrayscale](#convertimagetograyscale-function)
- [SharpenImage](#sharpenimage-function)
- [DetectEdgesInImage](#detectedgesinimage-function)
- [ConvolveImage](#convolveimage-function)
- [ApplyFilter](#applyfilter-function)
- [ShowImage](#showimage-function)
- [CV2PIL](#cv2pil-function)
- [PIL2CV2](#pil2cv2-function)
- [GetSystemUsage](#GetSystemUsage)
- [GetConsoleHeight](#GetConsoleHeight)
- [ClearScreen](#ClearScreen)
- [ExitHandler](#ExitHandler)
- [SelectGPU](#SelectGPU)
- [LookForKeys](#LookForKeys)



## CreateFolder

The `CreateFolder` function allows you to create folders with various modes.

### Function Signature

```python
CreateFolder(path, mode="a", verbose=True)
```

- `path` (str): The path to the folder to be created.
- `mode` (str): The mode for folder creation ('f', 'o', 'c', or 'a'). Defaults to 'a' (ask_user).
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

#### Examples

##### Example 1: Create a folder using the default "ask_user" mode with verbose messages

```python
import abdutils as abd

abd.CreateFolder("my_folder", verbose=True)
# Expected Output: Info: The folder 'my_folder' already exists. Deleting and recreating.
```

##### Example 2: Create a folder recursively with a long path without verbose messages

```python
import abdutils as abd

abd.CreateFolder("parent/child/grandchild", verbose=False)
# No output if the folder doesn't exist; Info message if the folder already exists.
```

##### Example 3: Force create a folder, displaying a message

```python
import abdutils as abd

abd.CreateFolder("folder_to_force_create", mode="f", verbose=True)
# Expected Output: Info: The folder 'folder_to_force_create' already exists. Deleting and recreating.
```

##### Example 4: Overwrite a folder, displaying a message

```python
import abdutils as abd

abd.CreateFolder("folder_to_overwrite", mode="o", verbose=True)
# Expected Output: Info: The folder 'folder_to_overwrite' already exists. Overwriting.
```

##### Example 5: Create a folder if it doesn't exist, displaying a message

```python
import abdutils as abd

abd.CreateFolder("folder_to_create_if_not_exist", mode="c", verbose=True)
# Expected Output: Info: The folder 'folder_to_create_if_not_exist' already exists. Skipping creation.
```

##### Example 6: Ask the user whether to delete and recreate a folder, displaying a message

```python
import abdutils as abd

# Creating a folder first
abd.CreateFolder("folder_to_ask_user")

#recreating the folder
abd.CreateFolder("folder_to_ask_user", mode="a", verbose=True)
# User will be prompted for input.
```



## Copy

The `Copy` function allows you to copy files based on a source pattern to a destination folder or filename.

### Function Signature

```python
Copy(src_pattern=None, dest_path=None, verbose=True)
```

- `src_pattern` (str): The source file pattern. Supports regular expressions like '/path/to/files/*.txt'.
- `dest_path` (str): The destination path including both folder and filename.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

#### Examples

##### Example 1: Copy a file to a destination folder with verbose messages

```python
import abdutils as abd

abd.Copy("source_file.txt", "destination_folder/destination_file.txt", verbose=True)
# Expected Output: Copied 'source_file.txt' to 'destination_folder/destination_file.txt'.
```

##### Example 2: Copy files matching a pattern to a destination folder

```python
import abdutils as abd

abd.Copy("files_to_copy/*.txt", "destination_folder/", verbose=True)
# Expected Output: Multiple 'Copied' messages for each file copied.
```

##### Example 3: Copy files matching a pattern to a specified filename

```python
import abdutils as abd

abd.Copy("files_to_copy/*.txt", "destination_folder/specific_file.txt", verbose=True)
# Expected Output: Copied each matched file to 'destination_folder/specific_file.txt'.
```

##### Example 4: Copy files matching a pattern to a non-existent destination folder

```python
import abdutils as abd

abd.Copy("files_to_copy/*.txt", "non_existent_folder/", verbose=True)
# Expected Output: Created 'non_existent_folder/' and copied matched files to it.
```

##### Example 5: Copy files matching a pattern to a non-existent destination folder without verbose messages

```python
import abdutils as abd

abd.Copy("files_to_copy/*.txt", "non_existent_folder/", verbose=False)
# No output if the folder doesn't exist; Files are copied silently.
```

## Move

The `Move` function allows you to move (cut and paste) files based on a source pattern to a destination path.

### Function Signature

```python
Move(src_pattern=None, dest_path=None, verbose=True)
```

- `src_pattern` (str): The source file pattern.
- `dest_path` (str): The destination path.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

#### Examples

##### Example 1: Move a file to a destination folder with verbose messages

```python
import abdutils as abd

abd.Move("source_file.txt", "destination_folder/destination_file.txt", verbose=True)
# Expected Output: Moved 'source_file.txt' to 'destination_folder/destination_file.txt'.
```

##### Example 2: Move files matching a pattern to a destination folder

```python
import abdutils as abd

abd.Move("files_to_move/*.txt", "destination_folder/", verbose=True)
# Expected Output: Multiple 'Moved' messages for each file moved.
```

##### Example 3: Move files matching a pattern to a specified filename

```python
import abdutils as abd

abd.Move("files_to_move/*.txt", "destination_folder/specific_file.txt", verbose=True)
# Expected Output: Moved each matched file to 'destination_folder/specific_file.txt'.
```

##### Example 4: Move files matching a pattern to a non-existent destination folder

```python
import abdutils as abd

abd.Move("files_to_move/*.txt", "non_existent_folder/", verbose=True)
# Expected Output: Created 'non_existent_folder/' and moved matched files to it.
```

##### Example 5: Move files matching a pattern to a non-existent destination folder without verbose messages

```python
import abdutils as abd

abd.Move("files_to_move/*.txt", "non_existent_folder/", verbose=False)
# No output if the folder doesn't exist; Files are moved silently.
```

## Delete

The `Delete` function allows you to delete files or folders based on the given path. It supports wildcard patterns.

### Function Signature

```python
Delete(path=None, verbose=True)
```

- `path` (str): The path to the file or folder to be deleted. Supports wildcard patterns.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

#### Examples

##### Example 1: Delete a single file

```python
import abdutils as abd

# Delete a specific file with verbose messages
abd.Delete("file_to_delete.txt", verbose=True)
```

##### Example 2: Delete a folder and its contents

```python
import abdutils as abd

# Delete a folder and its contents with verbose messages
abd.Delete("folder_to_delete/", verbose=True)
```

##### Example 3: Delete files using wildcard pattern

```python
import abdutils as abd

# Delete all .txt files in the current directory with verbose messages
abd.Delete("*.txt", verbose=True)
```

##### Example 4: Delete files using a nested folder path

```python
import abdutils as abd

# Delete all .jpg files in a nested folder with verbose messages
abd.Delete("parent_folder/nested_folder/*.jpg", verbose=True)
```

##### Example 5: Deleting non-existent files

```python
import abdutils as abd

# Attempt to delete non-existent files with verbose messages
abd.Delete("non_existent_file.txt", verbose=True)
# Expected Output: No files/folders found matching the pattern 'non_existent_file.txt'.
```

##### Example 6: Deleting a symlink

```python
import abdutils as abd

# Attempt to delete a symlink with verbose messages
abd.Delete("symlink_to_file.txt", verbose=True)
# Expected Output: Deleted 'symlink_to_file.txt' (unsupported path type).
```

These examples demonstrate how to use the `Delete` function to delete files and folders based on the provided path and support for wildcard patterns.

## Rename

The `Rename` function allows you to rename a file or folder based on the given source path and new name.

### Function Signature

```python
Rename(src_path=None, new_name=None, verbose=True)
```

- `src_path` (str): The source path of the file or folder to be renamed.
- `new_name` (str): The new name for the file or folder.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

#### Examples

##### Example 1: Rename a file with a new name

```python
import abdutils as abd

abd.Rename("old_filename.txt", "new_filename.txt", verbose=True)
# Expected Output: Renamed 'old_filename.txt' to 'new_filename.txt'.
```

##### Example 2: Rename a folder with a new name

```python
import abdutils as abd

abd.Rename("old_folder", "new_folder", verbose=True)
# Expected Output: Renamed 'old_folder' to 'new_folder'.
```

##### Example 3: Rename a file or folder that does not exist

```python
import abdutils as abd

abd.Rename("non_existent_file.txt", "new_name.txt", verbose=True)
# Expected Output: [Error] [Errno 2] No such file or directory: 'non_existent_file.txt'.
```

##### Example 4: Rename a file or folder with verbose messages turned off

```python
import abdutils as abd

abd.Rename("existing_file.txt", "new_name.txt", verbose=False)
# No output if successful; Error message if the source path does not exist.
```

## ReadFile

The `ReadFile` function allows you to read a file line by line and return one line at a time with each function call.

### Function Signature

```python
ReadFile(file_path)
```

- `file_path` (str): The path to the file to be read.

#### Examples

##### Example 1: Read a file line by line

```python
import abdutils as abd

line1 = abd.ReadFile("sample.txt")
print(line1)
# Expected Output: Contents of the first line in 'sample.txt'
```

##### Example 2: Read multiple lines

```python
import abdutils as abd

line1 = abd.ReadFile("sample.txt")
line2 = abd.ReadFile("sample.txt")
print(line1)
print(line2)
# Expected Output: Contents of the first and second lines in 'sample.txt'
```

##### Example 3: Import and use `ReadFile`

```python
from abdutils import ReadFile

line1 = ReadFile("imported_file.txt")
print(line1)
# Expected Output: Contents of the first line in 'imported_file.txt'
```

##### Example 4: Read Lines in a Loop (while)

```python
import abdutils as abd

file_path = "sample.txt"
line = abd.ReadFile(file_path)

while line is not None:
    print(line)
    line = abd.ReadFile(file_path)
# Reads and prints all lines of 'abdutils.py' using a while loop.
```

## WriteFile

The `WriteFile` function enables you to write lines to a file in either append or write mode.

### Function Signature

```python
WriteFile(file_path, line)
```

- `file_path` (str): The path to the file to be written.
- `line` (str): The line to be written to the file.

#### Examples

##### Example 1: Write a line to a file

```python
import abdutils as abd

abd.WriteFile("my.txt", "Hello, World!")
# The line "Hello, World!" is written to 'my.txt'
```

##### Example 2: Write multiple lines to a file

```python
import abdutils as abd

lines_to_write = ["Line 1", "Line 2", "Line 3"]
abd.WriteFile("my.txt", lines_to_write)
# The lines "Line 1", "Line 2", and "Line 3" are appended to 'my.txt'
```

##### Example 3: Import and use `WriteFile`

```python
from abdutils import WriteFile

WriteFile("imported_file.txt", "This is an imported file.")
# The line "This is an imported file." is written to 'imported_file.txt'
```

##### Example 4: Write Lines in a Loop (for)

```python
import abdutils as abd

lines_to_write = ["Line 1", "Line 2", "Line 3"]
for line in lines_to_write:
    abd.WriteFile("looped_file.txt", line, mode="a")
# Overwrites the file 'looped_file.txt' with each line.

```

##### Example 5: Write Lines in a Loop (while)

```python
import abdutils as abd

line_to_write = "Looped line"
counter = 0
while counter < 3:
    abd.WriteFile("looped_file.txt", line_to_write, 'a')
    counter += 1
# Writes "Looped line" to 'looped_file.txt' three times in append mode.
```



# ReadImage Function

The `ReadImage` function is a Python utility for reading images from specified file paths. This function offers flexibility by allowing you to specify the desired image loading mode and method. It can load images using either the Pillow (PIL) library or OpenCV (cv2) library, depending on the method specified. Additionally, it performs checks on the image mode and handles various error scenarios gracefully.

## Function Signature

```python
from abdutils import *
def ReadImage(image_path, mode='RGB', method='auto'):
```

## Parameters

- `image_path` (str): The path to the image file.
- `mode` (str): The desired mode for loading the image ('RGB', 'L', etc.). Defaults to 'RGB'.
- `method` (str): The method to use for loading the image ('auto', 'PIL', or 'CV2'). Defaults to 'auto'.

## Returns

- `PIL.Image.Image` or `numpy.ndarray`: The loaded image.

## Error Handling

The function includes error handling for various scenarios, such as invalid modes, unsupported methods, permission errors, and file not found errors. It gracefully handles these errors and provides informative error messages.

### Examples

#### Example 1: Load an RGB image using default settings

```python
from abdutils import *

image = ReadImage("example.jpg")
```

In this example, the function loads an RGB image ("example.jpg") using the default settings, which use the Pillow library for image loading.

#### Example 2: Load a grayscale image using OpenCV (cv2)

```python
from abdutils import *

grayscale_image = ReadImage("example.png", mode='L', method='CV2')
```

This example loads a grayscale image ("example.png") using OpenCV (cv2) for image loading. The method is explicitly set to 'CV2'.

#### Example 3: Handle an unsupported image format

```python
from abdutils import *

unsupported_image = ReadImage("example.gif")
```

In this case, the function attempts to load an unsupported image format ("example.gif"). Since it's a GIF format and the method is set to 'auto', the function will use Pillow for loading.

#### Example 4: Handle a file not found error

```python
from abdutils import *

non_existent_image = ReadImage("non_existent.jpg")
```

This example demonstrates handling a file not found error. The function attempts to load an image ("non_existent.jpg") that doesn't exist in the specified path and will handle the error gracefully.

#### Example 5: Handle a permission error

```python
from abdutils import *

image_with_permission_error = ReadImage("protected.jpg")
```

In this example, the function attempts to open an image ("protected.jpg") but encounters a permission error due to restricted access. The function handles the permission error gracefully.

These examples showcase the versatility of the `ReadImage` function, including loading images in different modes and handling various error scenarios. Customize the file paths and parameters according to your specific image loading requirements.


## SaveImage Function

The `SaveImage` function is a Python utility for saving images to a specified file path. This function provides flexibility in choosing the method for saving the image and handles various error scenarios gracefully.

### Function Signature

```python
def SaveImage(image, save_path, method='auto'):
```

### Parameters

- `image`: The image to be saved (PIL.Image.Image or numpy.ndarray).
- `save_path`: The path where the image should be saved.
- `method` (str): The method to use for saving the image ('auto', 'PIL', or 'CV2'). Defaults to 'auto'.

### Returns

- `True` if the image is saved successfully; `False` if there is an error.

### Error Handling

The function includes error handling for various scenarios, such as unsupported image types, permission errors, and other exceptions. It gracefully handles these errors and provides informative error messages.

### Examples

#### Example 1: Save a PIL image using default settings

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Save the image using default 'auto' method
result = abd.SaveImage(image, "output.jpg")
if result:
    print("Image saved successfully.")
else:
    print("Failed to save the image.")
```

In this example, the function saves a PIL image using the default 'auto' method, which detects the image type.

#### Example 2: Save a numpy array (cv2 image) using explicit 'CV2' method

```python
import abdutils as abd

# Load an image using cv2
image = abd.ReadImage("input.png")

# Save the image using 'CV2' method
result = abd.SaveImage(image, "output.png", method='CV2')
if result:
    print("Image saved successfully.")
else:
    print("Failed to save the image.")
```

This example demonstrates saving a cv2 image using the 'CV2' method explicitly.

## ConvertToGrayscale Function

The `ConvertToGrayscale` function is a Python utility for converting images to grayscale. This function allows you to specify the method for conversion and supports both PIL and cv2 image types.

### Function Signature

```python
def ConvertToGrayscale(image, method='auto'):
```

### Parameters

- `image`: The input image (PIL.Image.Image or numpy.ndarray).
- `method` (str): The method to use for conversion ('auto', 'PIL', or 'CV2'). Defaults to 'auto'.

### Returns

- Grayscale image (PIL.Image.Image or numpy.ndarray).

### Error Handling

The function includes error handling for various scenarios, such as unsupported image types or formats, and provides informative error messages.

### Examples

#### Example 1: Convert an image to grayscale using the default 'auto' method

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Convert the image to grayscale using the default 'auto' method
grayscale_image = abd.ConvertToGrayscale(image)

# Display or further process the grayscale image
```

In this example, the function converts an image to grayscale using the default 'auto' method, which automatically detects the image type.

#### Example 2: Convert an image to grayscale using the 'CV2' method

```python
import abdutils as abd

# Load an image using cv2
image = abd.ReadImage("input.png")

# Convert the image to grayscale using the 'CV2' method
grayscale_image = abd.ConvertToGrayscale(image, method='CV2')

# Display or further process the grayscale image
```

This example explicitly converts a cv2 image to grayscale using the 'CV2' method.

## ConvertToRGB Function

The `ConvertToRGB` function is a Python utility that allows you to convert an image to the RGB color mode. This function supports both PIL (Pillow) and cv2 (OpenCV) image types and provides flexibility in choosing the conversion method.

### Function Signature

```python
def ConvertToRGB(image, method='auto'):
```

### Parameters

- `image`: The input image (PIL.Image.Image or numpy.ndarray).
- `method` (str): The method to use for conversion ('auto', 'PIL', or 'CV2'). Defaults to 'auto'.

### Returns

- RGB image (PIL.Image.Image or numpy.ndarray).

### Error Handling

The function includes error handling for various scenarios, such as unsupported image types, modes, or formats, and provides informative error messages.

### Examples

#### Example 1: Convert an image to RGB color mode using the default 'auto' method

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Convert the image to RGB color mode using the default 'auto' method
rgb_image = abd.ConvertToRGB(image)

# Display or further process the RGB image
```

In this example, the function converts an image to RGB color mode using the default 'auto' method, which automatically detects the image type and mode.

#### Example 2: Convert a cv2 image to RGB using the 'CV2' method

```python
import abdutils as abd

# Load an image 
image = abd.ReadImage("input.png")

# Convert the image to RGB color mode using the 'CV2' method
rgb_image = abd.ConvertToRGB(image, method='CV2')

# Display or further process the RGB image
```

This example explicitly converts an  image to RGB using the 'CV2' method.

## CropImage Function

The `CropImage` function is a Python utility for cropping a region of interest (ROI) from an image. It accepts a PIL (Pillow) image and a list of coordinates to define the cropping area.

### Function Signature

```python
def CropImage(image, coordinates):
```

### Parameters

- `image`: The input image (PIL.Image.Image).
- `coordinates` (list): A list containing the left, top, right, and bottom coordinates.

### Returns

- Cropped image (PIL.Image.Image).

### Error Handling

The function includes error handling for cases where the input image or coordinates are invalid, and it provides informative error messages.

### Example

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Define the coordinates for cropping [left, top, right, bottom]
crop_coordinates = [0, 0, 50, 50]

# Crop a region of interest from the image
cropped_image = abd.CropImage(image, crop_coordinates)

# Display or further process the cropped image
```

In this example, the function crops a region of interest from the input image based on the specified coordinates.

## GetImageSize Function

The `GetImageSize` function is a Python utility that allows you to retrieve the size (width and height) of an image. This function supports both PIL (Pillow) and cv2 (OpenCV) image types and provides flexibility in choosing the method for reading the image size.

### Function Signature

```python
def GetImageSize(image, method='auto'):
```

### Parameters

- `image`: The input image (PIL.Image.Image or numpy.ndarray).
- `method` (str): The method to use for reading the image ('auto', 'PIL' for Pillow, 'CV2' for OpenCV).
                      Defaults to 'auto'.

### Returns

- A tuple containing the width and height of the image.

### Error Handling

The function includes error handling for various scenarios, such as unsupported image types or methods, and provides informative error messages.

### Examples

#### Example 1: Get the size of an image using the default 'auto' method

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Get the size of the image using the default 'auto' method
width, height = abd.GetImageSize(image)

# Display or further process the image size
```

In this example, the function retrieves the size of an image using the default 'auto' method, which automatically detects the image type.

#### Example 2: Get the size of a cv2 image using the 'CV2' method

```python

import abdutils as abd

# Load an image using cv2
image = abd.ReadImage("input.png")

# Get the size of the cv2 image using the 'CV2' method
width, height = abd.GetImageSize(image, method='CV2')

# Display or further process the image size
```

This example explicitly retrieves the size of a cv2 image using the 'CV2' method.

## ResizeImage Function

The `ResizeImage` function is a Python utility that allows you to resize an image to the specified size while preserving the aspect ratio. This function utilizes the Pillow (PIL) library to perform the resizing.

### Function Signature

```python
def ResizeImage(image, size, verbose=True):
```

### Parameters

- `image`: The input image (PIL.Image.Image).
- `size` (tuple): The target size (width, height).
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- The resized image (PIL.Image.Image).

### Error Handling

The function includes error handling for scenarios where the input image is not a PIL Image object or the size parameter is not a valid tuple of two integers.

### Examples

#### Example 1: Resize an image to a specific size

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Resize the image to the specified size while preserving the aspect ratio
resized_image = abd.ResizeImage(image, (300, 200))

# Display or further process the resized image
```

In this example, the function resizes the input image to a width of 300 pixels and a height of 200 pixels while preserving the aspect ratio.

#### Example 2: Resize an image without displaying verbose messages

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Resize the image to the specified size without displaying verbose messages
resized_image = abd.ResizeImage(image, (640, 480), verbose=False)

# Display or further process the resized image
```

This example resizes the image to a width of 640 pixels and a height of 480 pixels without displaying verbose messages.

## GaussianBlurImage Function

The `GaussianBlurImage` function is a Python utility for applying Gaussian blur to an image. This function utilizes the Pillow (PIL) library to perform the blurring operation.

### Function Signature

```python
def GaussianBlurImage(image, sigma=1.0, verbose=True):
```

### Parameters

- `image`: The input image (PIL.Image.Image).
- `sigma` (float): The standard deviation of the Gaussian kernel.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- The blurred image (PIL.Image.Image).

### Error Handling

The function includes error handling for scenarios where the input image is not a PIL Image object or the sigma parameter is not a positive number.

### Example

```python

import abdutils as abd

# Load an image
image = abd.ReadImage("input.jpg")

# Apply Gaussian blur to the image with a specified sigma value
blurred_image = abd.GaussianBlurImage(image, sigma=2.0)

# Display or further process the blurred image
```

In this example, the function applies Gaussian blur to the input image with a sigma value of 2.0.

## ConvertImageToGrayscale Function

The `ConvertImageToGrayscale` function is a Python utility that allows you to convert a color image to grayscale. This function utilizes the Pillow (PIL) library to perform the conversion.

### Function Signature

```python
def ConvertImageToGrayscale(image, verbose=True):
```

### Parameters

- `image`: The input image (PIL.Image.Image).
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- The grayscale image (PIL.Image.Image).

### Error Handling

The function includes error handling for scenarios where the input image is not a PIL Image object.

### Example

```python

import abdutils as abd

# Load a color image
image = Image.open("color_image.jpg")

# Convert the color image to grayscale
grayscale_image = abd.ConvertImageToGrayscale(image)

# Display or further process the grayscale image
```

In this example, the function converts a color image to grayscale.

## SharpenImage Function

The `SharpenImage` function is a Python utility for sharpening an image. This function utilizes the Pillow (PIL) library to perform the sharpening operation.

### Function Signature

```python
def SharpenImage(image, factor=2.0, verbose=True):
```

### Parameters

- `image`: The input image (PIL.Image.Image).
- `factor` (float): The sharpening factor.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- The sharpened image (PIL.Image.Image).

### Error Handling

The function includes error handling for scenarios where the input image is not a PIL Image object or the factor parameter is not a positive number.

### Example

```python

import abdutils as abd

# Load an image
image = Image.open("input_image.jpg")

# Sharpen the image with a specified factor
sharpened_image = abd.SharpenImage(image, factor=1.5)

# Display or further process the sharpened image
```

In this example, the function sharpens the input image with a factor of 1.5.

Feel free to customize the file paths, parameters, and examples according to your specific image processing needs.

# DetectEdgesInImage Function

The `DetectEdgesInImage` function is a Python utility for detecting edges in an image using various edge detection methods. It provides flexibility in choosing the edge detection method and offers customizable threshold values for the Canny edge detection method. This function supports both Pillow (PIL) and NumPy image types.

## Function Signature

```python
def DetectEdgesInImage(image, method='canny', threshold1=100, threshold2=200, verbose=True):
```

### Parameters

- `image` (PIL.Image.Image or numpy.ndarray): The input image.
- `method` (str): The edge detection method to use ('canny', 'sobel', 'laplacian', 'prewitt', or 'scharr'). Defaults to 'canny'.
- `threshold1` (int): The first threshold for the hysteresis procedure (only for the 'canny' method). Defaults to 100.
- `threshold2` (int): The second threshold for the hysteresis procedure (only for the 'canny' method). Defaults to 200.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- `PIL.Image.Image`: The edge-detected image.

### Error Handling

The function includes error handling for various scenarios, such as checking if the input image is a valid PIL Image object and validating threshold values for the Canny method. It gracefully handles these errors and provides informative error messages.

### Examples

#### Example 1: Detect edges using the default Canny method

```python
import abdutils as abd

# Read an image
image = abd.ReadImage("input.jpg")

# Detect edges using the default Canny method
edge_image = abd.DetectEdgesInImage(image)

# Show the edge-detected image
abd.ShowImage(edge_image)

# Display or further process the edge-detected image
```

In this example, the function detects edges in an image using the default Canny edge detection method and displays the edge-detected image using `abd.ShowImage`.

#### Example 2: Detect edges using the Sobel method

```python
import abdutils as abd

# Read an image
image = abd.ReadImage("input.jpg")

# Detect edges using the Sobel method
edge_image = abd.DetectEdgesInImage(image, method='sobel')

# Show the edge-detected image
abd.ShowImage(edge_image)

# Display or further process the edge-detected image
```

This example explicitly uses the Sobel edge detection method to detect edges in an image and displays the edge-detected image using `abd.ShowImage`.

#### Example 3: Detect edges using custom Canny thresholds and without verbose messages

```python
import abdutils as abd

# Read an image
image = abd.ReadImage("input.jpg")

# Detect edges using custom Canny thresholds and disable verbose messages
edge_image = abd.DetectEdgesInImage(image, threshold1=50, threshold2=150, verbose=False)

# Show the edge-detected image
abd.ShowImage(edge_image)

# Display or further process the edge-detected image
```

In this example, the function uses custom threshold values for the Canny method, disables verbose messages during edge detection, and displays the edge-detected image using `abd.ShowImage`.

#### Example 4: Handle an unsupported edge detection method

```python
import abdutils as abd

# Read an image
image = abd.ReadImage("input.jpg")

# Attempt to detect edges using an unsupported method
edge_image = abd.DetectEdgesInImage(image, method='unsupported_method')

# Error message will be displayed, and edge_image will be None
```

This example demonstrates handling an unsupported edge detection method, which will result in an error message.

#### Example 5: Handle errors gracefully

```python
import abdutils as abd

# Read an invalid image (not a PIL Image object)
image = "invalid_image.jpg"

# Attempt to detect edges
edge_image = abd.DetectEdgesInImage(image)

# Error message will be displayed, and edge_image will be None
```

In this case, the function attempts to detect edges in an invalid image (not a PIL Image object) and handles the error gracefully.

These examples demonstrate the versatility of the `DetectEdgesInImage` function, including choosing different edge detection methods, customizing threshold values, and displaying the edge-detected image using `abd.ShowImage`. Customize the file paths and parameters according to your specific edge detection requirements.


You can adjust or expand upon the documentation as needed to provide more details or examples.


# ConvolveImage Function

The `ConvolveImage` function is a Python utility for applying convolution to an image using a given kernel. This function supports both Pillow (PIL) and NumPy image types, allowing you to perform convolution operations on images.

## Function Signature

```python
def ConvolveImage(image, kernel, verbose=True):
```

### Parameters

- `image` (PIL.Image.Image): The input image.
- `kernel` (numpy.ndarray): The convolution kernel.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- `PIL.Image.Image`: The convolved image.

### Error Handling

The function includes error handling for various scenarios, such as checking if the input image is a valid PIL Image object and verifying the kernel's data type and shape. It gracefully handles these errors and provides informative error messages.

### Examples

#### Example 1: Convolve an image using a custom kernel

```python
import abdutils as abd
import numpy as np

# Read an image
image = abd.ReadImage("input.jpg")

# Define a custom convolution kernel
custom_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# Apply convolution to the image using the custom kernel
convolved_image = abd.ConvolveImage(image, custom_kernel)

# Show the convolved image
abd.ShowImage(convolved_image)

# Display or further process the convolved image
```

In this example, the function applies convolution to an image using a custom kernel and displays the convolved image using `abd.ShowImage`.

#### Example 2: Convolve an image without displaying verbose messages

```python
import abdutils as abd
import numpy as np

# Read an image
image = abd.ReadImage("input.jpg")

# Define a custom convolution kernel
custom_kernel = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]])

# Apply convolution to the image without verbose messages
convolved_image = abd.ConvolveImage(image, custom_kernel, verbose=False)

# Show the convolved image
abd.ShowImage(convolved_image)

# Display or further process the convolved image
```

This example applies convolution to an image using a custom kernel but disables verbose messages during the convolution process.

# ApplyFilter Function

The `ApplyFilter` function is a Python utility for applying a convolution filter to an image using a custom kernel. This function supports both Pillow (PIL) and NumPy image types, allowing you to apply custom filters to images.

## Function Signature

```python
def ApplyFilter(image, kernel):
```

### Parameters

- `image` (PIL.Image.Image or numpy.ndarray): The input image to apply the filter to.
- `kernel` (numpy.ndarray): The custom convolution kernel.

### Returns

- `PIL.Image.Image` or `numpy.ndarray`: The filtered image.

### Error Handling

The function includes error handling for various scenarios, such as checking if the input image is a valid PIL Image object or a NumPy array (cv2 image). It gracefully handles these errors and provides informative error messages.

### Examples

#### Example 1: Apply a custom filter to an image

```python
import abdutils as abd
import numpy as np

# Read an image
image = abd.ReadImage("input.jpg")

# Define a custom convolution kernel for the filter
custom_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

# Apply the custom filter to the image
filtered_image = abd.ApplyFilter(image, custom_kernel)

# Show the filtered image
abd.ShowImage(filtered_image)

# Display or further process the filtered image
```

In this example, the function applies a custom filter to an image using a custom convolution kernel and displays the filtered image using `abd.ShowImage`.

#### Example 2: Apply a filter to a NumPy array (cv2 image)

```python
import abdutils as abd
import numpy as np

# Read an image using cv2 (NumPy array)
image = abd.ReadImage("input.png")

# Define a custom convolution kernel for the filter
custom_kernel = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])

# Apply the custom filter to the image (NumPy array)
filtered_image = abd.ApplyFilter(image, custom_kernel)

# Show the filtered image
abd.ShowImage(filtered_image)

# Display or further process the filtered image
```

This example demonstrates applying a custom filter to a NumPy array (cv2 image) and displaying the filtered image using `abd.ShowImage`.

These examples showcase the functionality of the `ConvolveImage` and `ApplyFilter` functions, allowing you to perform convolution operations and apply custom filters to images with ease. Customize the kernel and image paths as needed for your specific image processing tasks.


You can customize or expand upon this documentation as necessary to provide more details or examples for your functions.

# ShowImage Function

The `ShowImage` function is a Python utility for displaying an image using Matplotlib. This function is useful for visualizing images during image processing tasks.

## Function Signature

```python
def ShowImage(image, title="Image", verbose=True):
```

### Parameters

- `image` (PIL.Image.Image): The input image.
- `title` (str): The title of the displayed image.
- `verbose` (bool): Whether to display verbose messages. Defaults to True.

### Returns

- None

### Error Handling

The function includes error handling to ensure that the input `image` is a valid PIL Image object. If the input is not a PIL Image, it raises an error.

### Example

```python
import abdutils as abd

# Read an image
image = abd.ReadImage("input.jpg")

# Display the image with a custom title
abd.ShowImage(image, title="My Image")

# Continue with image processing or analysis
```

In this example, the `ShowImage` function is used to display an image with a custom title. The image can be loaded using the `abd.ReadImage` function or obtained from any other source.

# CV2PIL Function

The `CV2PIL` function is a Python utility for converting an OpenCV image (in BGR format) to a PIL Image (in RGB format). This conversion is useful when working with both OpenCV and PIL for image processing tasks.

## Function Signature

```python
def CV2PIL(cv2_image):
```

### Parameters

- `cv2_image` (numpy.ndarray): The OpenCV image (BGR format).

### Returns

- PIL.Image.Image or None: The PIL Image if the conversion is successful; otherwise, it returns None.

### Example

```python
import abdutils as abd

# Load an image using OpenCV (cv2)
cv2_image = abd.ReadImage("input.jpg")

# Convert the OpenCV image to a PIL Image
pil_image = abd.CV2PIL(cv2_image)

# Perform PIL-based image processing on pil_image
```

In this example, the `CV2PIL` function is used to convert an OpenCV image to a PIL Image, enabling further image processing using PIL.

# PIL2CV2 Function

The `PIL2CV2` function is a Python utility for converting a PIL Image (in RGB format) to an OpenCV image (in BGR format). This conversion is useful when working with both PIL and OpenCV for image processing tasks.

## Function Signature

```python
def PIL2CV2(pil_image):
```

### Parameters

- `pil_image` (PIL.Image.Image): The PIL Image (RGB format).

### Returns

- numpy.ndarray or None: The OpenCV image if the conversion is successful; otherwise, it returns None.

### Example

```python
import abdutils as abd

# Load an image using PIL
pil_image = abd.ReadImage("input.jpg")

# Convert the PIL Image to an OpenCV image
cv2_image = abd.PIL2CV2(pil_image)

# Perform OpenCV-based image processing on cv2_image
```

In this example, the `PIL2CV2` function is used to convert a PIL Image to an OpenCV image, enabling further image processing using OpenCV.

These utility functions (`ShowImage`, `CV2PIL`, and `PIL2CV2`) provide essential functionality for displaying images and performing conversions between common image formats, making them valuable tools for image processing and analysis tasks.

# GetSystemUsage
This function retrieves the current system's CPU, GPU, and Disk usage statistics.
#### Function Signature
```python
def GetSystemUsage():
```
#### Example Usage
```python
import abdutils as abd

cpu, gpu_usages, gpu_memory, disk = abd.GetSystemUsage()
print(f"CPU Usage: {cpu}%, Disk Usage: {disk}%")
for i, usage in enumerate(gpu_usages):
    print(f"GPU {i} Usage: {usage}%")
for i, memory in enumerate(gpu_memory):
    print(f"GPU {i} Memory Usage: {memory}%")
```
## GetConsoleHeight
This function returns the height of the console in lines.
#### Function Signature
```python
def GetConsoleHeight():
```
#### Example Usage
```python
import abdutils as abd
height = abd.GetConsoleHeight()
print(f"Console Height: {height} lines")
```
# ClearScreen
Clears the console screen.
#### Function Signature
```python
def ClearScreen():
```
*No input parameters*
#### Example Usage
```python
import abdutils as abd

abd.ClearScreen()
```
# LookForKeys
The `LookForKeys` function is designed to handle proper program exit, ensuring the freeing of GPU resources. It sets up signal handlers to capture Ctrl+C and Ctrl+Z signals.

#### Function Signature
```python
def LookForKeys():
```
*No input parameters*

#### Example Usage
```python
import abdutils as abd

abd.LookForKeys()

# Your program logic here...
```

*Note:* This function should be called at the beginning of your program to ensure the proper setup of signal handlers for graceful termination and resource management.

# SelectGPU
The `SelectGPU` function automatically selects a GPU that is available and has the most free memory. This is particularly useful for optimizing GPU resource allocation in environments with multiple GPUs.

#### Function Signature
```python
def SelectGPU():
```
*No input parameters*

#### Example Usage
```python
import abdutils as abd

selected_gpu = abd.SelectGPU()
if selected_gpu:
    print(f"Automatically selected GPU: {selected_gpu.name}")
```

*Note:* This function is ideal for scenarios where optimal GPU utilization is crucial, such as in machine learning or data processing tasks that are GPU-intensive. It simplifies the process of selecting the most appropriate GPU based on current memory availability.


# ShowUsage
The `ShowUsage` function displays real-time system usage statistics, including CPU, GPU, and Disk usage. It's typically implemented to run in a separate thread, continuously updating these statistics on the console.

#### Function Signature
```python
def ShowUsage():
    # Function body...
```
*No input parameters*

#### Example Usage
```python
import abdutils as abd

# Start displaying system usage in a separate thread
abd.ShowUsage()

# Rest of your program...
```

*Note:* This function is useful for monitoring the performance of your system in real-time, especially during resource-intensive operations.
