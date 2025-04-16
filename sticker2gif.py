import os, ai
from PIL import Image
from tools import *

class Maker:
    def __init__(self, img_path, log=False):
        self.img_path = img_path
        self.path = 'Saved_Sticker'
        
        os.makedirs(self.path, exist_ok=1)
        os.chdir(self.path)
       
        self.log = log
        Clean()
        
        os.makedirs('temp', exist_ok=True)

    def getImg(self):
        if PathOrUrl(self.img_path):
            img = self.img_path
        else:
            Log('\nDownloading...', self.log)
            img = Download(self.img_path)
        
        return Image.open(img)
            

    def cutImg(self):
        sticker = self.getImg()

        size = sticker.size

        # Using basic AI to determine mini images in each row and column
        Log('\nAI Running...', self.log)
        AI = ai.Brain(sticker)
        columns, rows = AI.run()
        Log('\nRows: {}, Columns: {}'.format(rows, columns), self.log)

        # Getting the fixed size of each mini image
        x, y = round(size[0] / columns), round(size[1] / rows)

        # Setting up cordinates
        cd = (0, 0, x, y)

        Log('\nCutting process...', self.log)
        n = 0
        for _ in range(rows):

            for _ in range(columns):

                # Cropping the mini image
                minSticker = sticker.crop(cd)
                
                colors = minSticker.convert('RGB').getcolors()
                if colors == None:
                    colors = [(0, (1, 0, 0))]
                
                # Detecting empty mini images and bypassing them
                if not (sum(colors[0][1]) == 0 and len(colors) == 1):
                    transparent_bg = Image.new('RGBA', (x, y), (0, 0, 0, 0))
                    Image.alpha_composite(transparent_bg, minSticker).save(f'temp/{n}.png')
                    n += 1
                
                # Cordinates of the next image in same row
                cd = (cd[0] + x, cd[1], cd[2] + x, cd[3])
            
            # Cordinates of the first image in the next row
            cd = (0, cd[1] + y, x, cd[3] + y)

    def rgba_to_gif_clean(self, frame): 
        rgba = frame.convert("RGBA")
 
        transparent_bg = Image.new("RGBA", rgba.size, (0, 0, 0, 0))
        clean = Image.alpha_composite(transparent_bg, rgba)
 
        data = clean.getdata()
        new_data = [
            (0, 0, 0, 0) if px[3] < 10 else px  # Set near-transparent pixels to black
            for px in data
        ]
        clean.putdata(new_data)
 
        gif_frame = clean.convert("P", palette=Image.ADAPTIVE, dither=Image.NONE)
 
        transparent_index = gif_frame.getpixel((0, 0))
        gif_frame.info["transparency"] = transparent_index

        return gif_frame

    def gifImg(self, name, duration):
        pics = [i for i in os.listdir('temp') if i.split('.')[0].isdecimal()]
        
        # Sorting pics ascendingly
        pics.sort(key = lambda x: int(x.split('.')[0]))

        frames = []
        for i in pics:
            frame = Image.open(opj('temp', i))
            frames.append(frame.copy())

        # Correct any incorrect input
        name = Rename(name)

        # Catch Stupid Inputs
        try:
            duri = int(duration)
            if not 0 < duri < 101:
                duri = 60
        except:
            duri = 60
        
        # Create GIF
        Log('\nCreating Gif...', self.log)
        target_size = (140, 140)
        resized_frames = [self.rgba_to_gif_clean(f.resize(target_size, Image.Resampling.LANCZOS)) for f in frames]
        resized_frames[0].save(
            name + '-2.gif',
            save_all=True,
            append_images=resized_frames[1:],
            duration=duri,
            loop=0,
            disposal=2,
            transparency=0
        )
        frames[0].save(
            name + '.gif',
            save_all=True,
            append_images=frames[1:],
            duration=duri,
            loop=0,
            transparency=0,      # Index of the transparent color (usually 0)
            disposal=2           # Ensures each frame clears before the next
        )

    def run(self):
        self.cutImg()
        
        self.gifImg(
            input('\nGIF name: '),
            input('\nDuration [from 1 to 100]: '))
        
        Clean()
        Log('\nDone!', self.log)
