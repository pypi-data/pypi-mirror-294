import os
import random
import string
from PIL import Image, ImageDraw, ImageFont
import platform

# Author info
author_info = """Made by Avinion
Telegram @akrim"""

def clear_console():
    """Clears the console based on the OS."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def generate_random_filename(extension):
    """Generates a random filename with the given extension."""
    return f"image_{random.randint(1000, 9999)}.{extension}"

def wrap_text(text, font, image_width, draw):
    """Wraps text to fit within the given image width."""
    lines = []
    words = text.split(' ')
    line = ""

    for word in words:
        # Create a line with the new word
        test_line = f"{line} {word}".strip()
        # Check the width of the test line
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        if text_width > image_width - 20:
            lines.append(line)
            line = word
        else:
            line = test_line
    lines.append(line)

    return lines

def text_to_image(text, font_size, image_path, image_format, background_color, text_color):
    """Generates an image from text with the specified font size, format, and colors."""
    try:
        # Load a font
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Create an initial image to calculate the size needed
    temp_image = Image.new('RGB', (1200, 800), background_color)
    draw = ImageDraw.Draw(temp_image)
    
    # Wrap text to fit the image width
    lines = wrap_text(text, font, temp_image.width, draw)

    # Calculate the width and height of the text block
    max_text_width = max(draw.textbbox((0, 0), line, font=font)[2] - draw.textbbox((0, 0), line, font=font)[0] for line in lines)
    text_block_height = sum(draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines) + (len(lines) - 1) * 5

    # Create a new image with enough width and height to fit the text
    image_width = max(max_text_width + 20, 1200)  # Ensure a minimum width
    image_height = max(text_block_height + 20, 800)  # Ensure a minimum height
    image = Image.new('RGB', (image_width, image_height), background_color)
    draw = ImageDraw.Draw(image)

    # Draw the text on the image
    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill=text_color)
        y += draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] + 5
    
    # Ensure the file path ends with the correct extension
    if not os.path.splitext(image_path)[1]:
        image_path = f"{image_path}.{image_format}"
    elif not image_path.lower().endswith(f'.{image_format}'):
        image_path = f"{image_path}.{image_format}"
    
    # Save the image
    try:
        image.save(image_path)
        print(f"Image saved as {image_path}")
    except Exception as e:
        print(f"Error while saving the image: {e}")

def main():
    """Main function to run the interactive script."""
    print(author_info)

    # Choose language
    language = input("Choose language/Выберите язык (E/R): ").strip().lower()
    if language == 'e':
        lang_select = "Choose color: \n1. Black \n2. White"
        lang_black = "Black"
        lang_white = "White"
    else:
        lang_select = "Выберите цвет: \n1. Черный \n2. Белый"
        lang_black = "Черный"
        lang_white = "Белый"

    while True:
        # File path input
        file_path = input("Введите путь к текстовому файлу (с пробелами и без): ").strip()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            continue
        except UnicodeDecodeError:
            print(f"Error reading the file. Ensure it's encoded in UTF-8: {file_path}")
            continue

        # Color selection
        print(lang_select)
        color_choice = input("Выберите цвет (1/2): ").strip()
        if color_choice == '1':
            background_color = 'black'
            text_color = 'white'
        elif color_choice == '2':
            background_color = 'white'
            text_color = 'black'
        else:
            print("Invalid color choice.")
            continue

        # Image format input
        image_format = input("Введите формат изображения (например, png, jpg): ").strip().lower()

        # Save path input
        save_path = input("Введите путь для сохранения изображения (с пробелами и без): ").strip()
        if not save_path:
            save_path = generate_random_filename(image_format)
        elif os.path.isdir(save_path):
            save_path = os.path.join(save_path, generate_random_filename(image_format))
        elif not os.path.splitext(save_path)[1]:
            save_path = f"{save_path}.{image_format}"
        elif not save_path.lower().endswith(f'.{image_format}'):
            save_path = f"{save_path}.{image_format}"

        # Save the image
        text_to_image(text, font_size=36, image_path=save_path, image_format=image_format, 
                      background_color=background_color, text_color=text_color)

        # Continue or exit
        choice = input("Продолжить работу? (Y/N): ").strip().lower()
        if choice == 'y':
            clear_console()
        elif choice == 'n':
            break
        else:
            print("Invalid choice. Exiting.")
            break

def textipic():
    """Main function to run the interactive script."""
    main()

if __name__ == "__main__":
    textipic()
