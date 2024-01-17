# pytextimage
Generate custom images with text easily.

![pytextimage.png](pytextimage.png)
<details>
<summary><i>Generated by <b>pytextimage</b></i></summary>
This image was created with this command:

```
pytextimage -b transparent -t py [path to SourceSans3-Bold] yellow -t text [path to SourceSans3-Bold] grey -t image [path to SourceSans3-Bold] blue -s pytextimage.png
```
</details>

## Installation
Install ```python3``` and ```fontconfig```. (It can work without ```fontconfig``` however it won't be able to resolve fonts so you will have to type their names exactly. Default sans-serif font won't work either.)

Run these commands:
```
git clone https://github.com/cosmicproc/pytextimage
pip3 install ./pytextimage
```
Then you can run the program with:
```
pytextimage
```

## Usage
Just run the program, and it should ask you the required specifications of your desired image.
If you want to automate or generate image with a single key press, you can also use the command line flags. 
To learn what flags are available, use the ```-h``` or ```--help``` flag.

## Use Cases
- GitHub repository social cards
- Letter profile images
- Text-based logos
