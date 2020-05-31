# Simple-Steganography
This is a sample python script that I modified a little from the original website found here:

https://www.thepythoncode.com/article/hide-secret-data-in-images-using-steganography-python

In the repo there are two bat files, one for encoding and one for decoding. If you want to run a command independently from the commands in the bat files, just follow the format below.

To Encode:
`python Steganography.py encode --image="/path/to/image" --message="The Message You Want To Hide"`

To Decode:
`python Steganography.py decode --image="/path/to/image"`

Some future plans I have for this repo are to allow for a full file to be embedded within an image.