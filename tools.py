import os, shutil 
import requests

sep = os.path.sep
ope = os.path.exists
opj = os.path.join

def PathOrUrl(inpt):
    # If path return True else it is assumed a url
    if ope(inpt):
        return True
    try:
        requests.get(inpt)
    except:
        raise TypeError('Boolean Required!')
    return False

def Download(url):
    pic = os.path.join("temp", "img.png")
    try: 
        response = requests.get(url, stream=True)
        response.raise_for_status() 
 
        os.makedirs(os.path.dirname(pic), exist_ok=True)
 
        with open(pic, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return pic
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to download image: {e}")


def Rename(name):
    if not name:
        name = 'Sample'

    for i in os.listdir():
        if name + '.gif' == i:
            name += '1'
    
    return name

def Clean():
    try:
        shutil.rmtree('temp')
    except:
        pass

def Log(text, switch):
    if switch:
        print(text)
