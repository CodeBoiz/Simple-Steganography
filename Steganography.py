#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Most of the core functionality of this python script is taken from this python article
   https://www.thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python

   Also watch this Computerphile video for a more indepth analysis of the topic
   https://www.youtube.com/watch?v=TWEXCYQKyDc
"""

# import modules
import cv2
import numpy as np
import os

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image, secret_data):
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[+] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[+] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def decode(image):
    print("[+] Decoding...")
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

if __name__ == "__main__":

    # import parse args
    import argparse

    # Parse arguments
    parser = argparse.ArgumentParser('Encode or Decode an image,')

    parser.add_argument("command", metavar="<command>", help="'encode' or 'decode'")
    parser.add_argument('--image', required=False, metavar="/path/to/image",
                        help="Path to image")
    parser.add_argument('--message', required=False, metavar="Message",
                        help="String that you want to be embeded within the image")

    args = parser.parse_args()

    # sort if you want to encode or decode an image
    if args.command == 'encode':
        input_image = cv2.imread(args.image)
        
        output_image = "encoded_image.PNG"
        secret_data = args.message
        # encode the data into the image
        encoded_image = encode(image=input_image, secret_data=secret_data)
        print("[+] Writing Output Image")
        # save the output image (encoded image)
        cv2.imwrite(output_image, encoded_image)
        print("[*] Done")

    if args.command == 'decode':
        output_image = cv2.imread(args.image)
        # decode the secret data from the image
        decoded_data = decode(output_image)
        print("[+] Decoded data:", decoded_data)
        print("[*] Done")