from PIL import Image
import requests
from io import BytesIO
import os, shutil, urllib
import random

# Settings =============================
number_of_shops = 100
number_of_places = 30
images_per_shop = 5
extension = '.jpg'

dimentions = {
    'thumbnail': (140, 140),
    'menu_image': (140,100),
    'description_image': (280,200)
}

folder_names = {
    'main_folder': 'photos',
    'icons_folder': 'icons',
    'places_folder': 'places',

}
filenames = {
    'shop': 'shop',
    'thumbnail': 'thumbnail',
    'menu_image': 'menu',
    'description_image': 'descr'

}






main_path = folder_names['main_folder']
icons_path = os.path.join( folder_names['main_folder'],'icons_folder')
places_path = os.path.join( folder_names['main_folder'],'places_folder')


# Resetting
if os.path.exists(folder_names['main_folder']):
    shutil.rmtree(folder_names['main_folder'])



if not os.path.exists(main_path):
    os.makedirs(main_path)

if not os.path.exists(icons_path):
    os.makedirs(icons_path)

if not os.path.exists(places_path):
    os.makedirs(places_path)



def get_image(url):
    with urllib.request.urlopen(url) as url:

        return url.read()

def make_url(dim, idx):
    if idx == 'random':
        url = "https://picsum.photos/{0}/{1}/?{2}".format(dim[0], dim[1], idx)
    else:
        url = "https://picsum.photos/{0}/{1}/?image={2}".format(dim[0], dim[1], idx)
    return url

def make_name(name, idx = None):
    if idx:
        return '{0}_{1}'.format(filenames[name], idx)
    else:
        return  '{0}'.format(filenames[name])



def preview(img):
    with open('temp.jpg', 'wb') as f:
        f.write(img)

    img = Image.open('temp.jpg')
    img.show()



for idx in range(0,number_of_shops):
    shop_folder_path = os.path.join(places_path, make_name('shop', idx))
    if not os.path.exists(shop_folder_path):
        os.makedirs(shop_folder_path)


    # Dimensions
    t_dim = dimentions['thumbnail']
    m_dim = dimentions['menu_image']
    d_dim = dimentions['description_image']

    thumbnail = os.path.join(shop_folder_path, make_name('thumbnail'))
    img = get_image(make_url(t_dim, 'random'))
    with open(thumbnail + extension, 'wb') as f:
        f.write(img)


    menu_image = os.path.join(shop_folder_path, make_name('menu_image'))
    img = get_image(make_url(d_dim, 'random'))
    with open(menu_image + extension, 'wb') as f:
        f.write(img)


    #
    for idx in range(0, images_per_shop):

        descr_name = os.path.join(shop_folder_path, make_name('description_image', idx))
        img = get_image(make_url(m_dim, 'random'))
        with open(descr_name + extension, 'wb') as f:
            f.write(img)
        #preview(img)








    #

