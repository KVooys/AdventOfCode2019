"""
--- Day 8: Space Image Format ---

The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars rovers, and so they are curious if you would spend a brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of rebooting! It's just waiting for someone to enter a BIOS password. The Elf responsible for the rover takes a picture of the password (your puzzle input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding; instead, they're encoded in a special Space Image Format. None of the Elves seem to remember why this is the case. They send you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the image left-to-right, then move downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit corresponds to the top-left pixel of the first layer, the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit, which corresponds to the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012

The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
"""
import pprint
from itertools import cycle
from collections import defaultdict
from PIL import Image

# part 1: Create a function that simulates the image as a bunch of lists, each list representing a single layer

def create_image(width, height, data):
    x_cycle = cycle(range(width))
    y_cycle = cycle(range(height))
    current_x = 0
    current_y = 0
    current_layer = 0
    layers = defaultdict(list)
    for pixel in str(data):
        current_x = next(x_cycle)
        if current_x == 0:
            current_y = next(y_cycle)
            if current_y == 0:
                current_layer += 1
        layers[current_layer].append(pixel)
    # pprint.pprint(layers)
    return layers


def validate(layers):
    min_zeroes = 10000000
    min_zeroes_layer = ""
    # find layer with fewewst zeroes
    for k, v in layers.items():
        zeroes = v.count('0')
        if zeroes < min_zeroes:
            min_zeroes = zeroes
            min_zeroes_layer = k
    # then multiply the 1 and 2 count of that layer

    return layers[min_zeroes_layer].count('1') * layers[min_zeroes_layer].count('2')


assert validate(create_image(3,2,123456789012)) == 1

with open("input/day8.txt") as input_file:
    inp = input_file.readline().strip()

print(validate(create_image(25, 6, inp)))

"""
--- Part Two ---

Now you're ready to decode the image. The image is rendered by stacking the layers and aligning the pixels with the same positions in each layer. The digits indicate the color of the corresponding pixel: 0 is black, 1 is white, and 2 is transparent.

The layers are rendered with the first layer in front and the last layer in back. So, if a given position has a transparent pixel in the first and second layers, a black pixel in the third layer, and a white pixel in the fourth layer, the final image would have a black pixel at that position.

For example, given an image 2 pixels wide and 2 pixels tall, the image data 0222112222120000 corresponds to the following image layers:

Layer 1: 02
         22

Layer 2: 11
         22

Layer 3: 22
         12

Layer 4: 00
         00

Then, the full image can be found by determining the top visible pixel in each position:

    The top-left pixel is black because the top layer is 0.
    The top-right pixel is white because the top layer is 2 (transparent), but the second layer is 1.
    The bottom-left pixel is white because the top two layers are 2, but the third layer is 1.
    The bottom-right pixel is black because the only visible pixel in that position is 0 (from layer 4).

So, the final image looks like this:

01
10

What message is produced after decoding your image?

"""
# I've decided to go all out and actually draw the image. Totally unnecessary, but fun to do.



def draw_image(width, height, layers):
    img = Image.new("RGBA",(width,height))
    img.save("day8drawing.png", "png")

    # Now we are going to apply the layers starting with the bottom one.
    for layer in range(max(layers.keys()), 0, -1):

        x_cycle = cycle(range(width))
        y_cycle = cycle(range(height))
        current_x = 0
        current_y = 0
        for pixel in layers[layer]:
            current_x = next(x_cycle)
            if current_x == 0:
                current_y = next(y_cycle)
            # black
            if pixel == "0":
                img.putpixel((current_x, current_y), (0,0,0,255))
            # white
            elif pixel == "1":
                img.putpixel((current_x, current_y), (255,255,255,255))
            elif pixel == "2":
                # I'll just ignore transparent pixels as they will be dealt with in a higher layer
                pass
    img.save("day8drawing.png", "png")



image = create_image(25, 6, inp)
draw_image(25, 6, image)

# img = create_image(3,2,123456789012)
# pprint.pprint(img)
# draw_image(3,2,img)

