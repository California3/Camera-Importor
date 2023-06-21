import os
import rawpy
from PIL import Image, ExifTags

def raw2jpg(source, save_path):
    # get file from soruce
    raw_file = os.path.basename(source)
    # get file name
    raw_file_name = raw_file.split('.')[0]
    # get file suffix
    raw_file_suffix = raw_file.split('.')[1]
    # target
    thumbLocation = save_path + '/' + raw_file_name + ".thumb.jpg"

    with rawpy.imread(source) as raw:
        thumb = raw.extract_thumb()
        # # save image
        # imageio.imsave(target, im)
        if thumb.format == rawpy.ThumbFormat.JPEG:
            with open(thumbLocation, 'wb') as f:
                f.write(thumb.data)

        image = Image.open(thumbLocation)
        image.getexif()
        exif = image._getexif()
        # get shot time
        # shot_time = exif[36867]
        print(exif[306])
        print(raw.metadata)
    return thumbLocation


source = "res/DSC01043.ARW"
save_path = "res"
print(raw2jpg(source, save_path))