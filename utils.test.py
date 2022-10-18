import utils
from PIL import Image

def fill_image_test():
    image:Image.Image = Image.open("./sample/sample2.png")
    image.show()

    for diff in [0,2,5,10,20]:
        print("diff:",diff)
        output_image = utils.fill_image(
            image=image,
            x=1000,
            y=1000,
            r=100,
            g=150,
            b=255,
            diff=diff
        )
        output_image.show()

dst:Image.Image = Image.open("sample/sample1.png")
before:Image.Image=Image.open("sample/sample2.png")
after:Image.Image=Image.open("sample/sample2_partially_filled.png")
replaced = utils.replace_changed_region(dst,before,after)
replaced.show()