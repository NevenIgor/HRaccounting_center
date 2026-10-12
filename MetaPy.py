import zipfile
import os
import shutil
from pathlib import Path
from PIL import Image
from PIL import ExifTags
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import olefile
from xml.etree import ElementTree
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


avible_types = ['docx', 'pptx', 'xlsx']


def del_doc(file_name):
    file_type = Path(file_name).suffix.lower()
    time_doc = os.stat(file_name)
    with olefile.OleFileIO(file_name, write_mode=True) as file:
        data = file.openstream('\x05SummaryInformation').read()
        file.write_stream('\x05SummaryInformation', bytes(len(data)))
    stream = None
    if file_type == '.doc':
        stream = 'Data'
    elif file_type == '.ppt':
        stream = 'Pictures'
    elif file_type == '.xls':
        stream = 'Workbook'
        os.utime(file_name, (time_doc.st_atime, time_doc.st_mtime))
        return None, None
    pngs = png_padding(file_name, stream)
    jpgs = jpeg_padding(file_name, stream)
    os.utime(file_name, (time_doc.st_atime, time_doc.st_mtime))
    return pngs, jpgs


def del_mp3(file_name):
    temp_mp3 = file_name
    time_doc = os.stat(temp_mp3)
    upd_mp3 = EasyID3(temp_mp3)
    upd_mp3.delete()
    upd_mp3.save()
    os.utime(temp_mp3, (time_doc.st_atime, time_doc.st_mtime))


def del_mp4(file_name):
    temp_mp4 = file_name
    time_doc = os.stat(temp_mp4)
    upd_mp4 = MP4(temp_mp4)
    upd_mp4.delete()
    upd_mp4.save()
    os.utime(temp_mp4, (time_doc.st_atime, time_doc.st_mtime))


def del_exif(file_name):
    temp_img = file_name
    time_doc = os.stat(temp_img)
    image = Image.open(temp_img)
    if image.mode == 'P':
        image = image.quantize(colors=256, method=2)
        image.save('tmp.png', colors=256)
    else:
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        image_without_exif.save(temp_img, optimize=True)
        os.utime(temp_img, (time_doc.st_atime, time_doc.st_mtime))


def del_docx(file_name, data_dir):
    media = list()
    doc_type = Path(file_name).suffix[1:]
    work_dir = os.getcwd()
    if doc_type not in avible_types:
        return
    temp_doc = os.path.join(work_dir, file_name)
    temp_zip = os.path.join(work_dir, 'tmp.zip')
    temp_folder = os.path.join(work_dir, 'tmp')

    time_doc = os.stat(temp_doc)
    try:
        os.rename(temp_doc, temp_zip)
    except FileExistsError:
        os.remove(temp_zip)
        os.rename(temp_doc, temp_zip)
    try:
        with zipfile.ZipFile(temp_zip, 'r') as z:
            z.extractall(temp_folder)
    except BadZipFile:
        return

    try:
        os.remove(os.path.join(temp_folder, 'docProps/app.xml'))
        os.remove(os.path.join(temp_folder, 'docProps/core.xml'))
    except FileNotFoundError:
        os.remove(temp_zip)
        shutil.make_archive(temp_zip.replace('.zip', ''), 'zip', temp_folder)
        os.rename(temp_zip, temp_doc)
        shutil.rmtree(temp_folder)
        os.utime(temp_doc, (time_doc.st_atime, time_doc.st_mtime))
        return

    shutil.copy(os.path.join(data_dir, f'Data/{doc_type}/app.xml'), os.path.join(temp_folder, 'docProps'))
    shutil.copy(os.path.join(data_dir, f'Data/{doc_type}/core.xml'), os.path.join(temp_folder, 'docProps'))

    for root, dirs, files in os.walk(temp_folder):
        for file in files:
            if Path(file).suffix.lower() == '.jpg' or Path(file).suffix.lower() == '.png' or Path(file).suffix.lower() == '.jpeg':
                del_exif(os.path.join(root, file))
                media.append(file)

    os.remove(temp_zip)
    shutil.make_archive(temp_zip.replace('.zip', ''), 'zip', temp_folder)

    os.rename(temp_zip, temp_doc)
    shutil.rmtree(temp_folder)

    os.utime(temp_doc, (time_doc.st_atime, time_doc.st_mtime))
    return media


def jpeg_padding(file_name, stream):
    files = ''
    with olefile.OleFileIO(file_name, write_mode=True) as file:
        try:
            data = file.openstream(stream).read()
        except Exception as e:
            print(e)
            return None
        st = data.find(b'\xff\xd8\xff')
        fn = data.find(b'\xff\xd9', st) + len(b'\xff\xd9')
        while st != -1:
            files += '1'
            jpg = data[st:fn]
            with open('tmp.jpg', 'wb') as f:
                f.write(jpg)
            try:
                del_exif('tmp.jpg')
                with open('tmp.jpg', 'rb') as f:
                    new_jpg = f.read()
            except Exception as e:
                print(e)
                new_jpg = jpg
            os.remove('tmp.jpg')
            idx = new_jpg.find(bytearray.fromhex('FFDA'))
            if len(new_jpg) < len(jpg):
                new_jpg = new_jpg[:idx] + bytes(len(jpg) - len(new_jpg)) + new_jpg[idx:]
                data = data[:st] + new_jpg + data[fn:]
                file.write_stream(stream, data)
            st = data.find(b'\xff\xd8\xff', st + 1)
            fn = data.find(b'\xff\xd9', st) + len(b'\xff\xd9')
    return files


def png_padding(file_name, stream):
    files = ''
    print(file_name)
    with olefile.OleFileIO(file_name, write_mode=True) as file:
        try:
            data = file.openstream(stream).read()
        except Exception as e:
            print(e)
            return None
        st = data.find(b'\x89PNG')
        fn = data.find(b'IEND\xaeB`\x82', st) + len(b'IEND\xaeB`\x82')
        while st != -1:
            files += '1'
            png = data[st:fn]
            with open('tmp.png', 'wb') as f:
                f.write(png)
            try:
                del_exif('tmp.png')
                with open('tmp.png', 'rb') as f:
                    new_png = f.read()
            except Exception as e:
                print(e)
                new_png = png
            os.remove('tmp.png')
            if len(new_png) < len(png):
                new_png += bytes(len(png) - len(new_png))
                data = data[:st] + new_png + data[fn:]
                file.write_stream(stream, data)
            st = data.find(b'\x89PNG', st + 1)
            fn = data.find(b'IEND\xaeB`\x82', st) + len(b'IEND\xaeB`\x82')
    return files


def to_zip(file_name):
    available_types = ['docx', 'pptx', 'xlsx']
    doc_type = Path(file_name).suffix[1:]
    work_dir = os.getcwd()
    if doc_type not in available_types:
        return
    temp_doc = os.path.join(work_dir, file_name)
    temp_folder = os.path.join(work_dir, 'tmp')

    time_doc = os.stat(temp_doc)
    try:
        with zipfile.ZipFile(temp_doc, 'r') as z:
            z.extractall(temp_folder)
    except Exception as e:
        print('Err:', e)
        return
    finally:
        return temp_doc, temp_folder, time_doc


def from_zip(temp_doc, temp_folder, time_doc):
    try:
        shutil.make_archive(temp_folder, 'zip', temp_folder)
        os.remove(temp_doc)
        os.rename(f'{temp_folder}.zip', temp_doc)
        shutil.rmtree(temp_folder)

        os.utime(temp_doc, (time_doc.st_atime, time_doc.st_mtime))
    except Exception as e:
        print('Err:', e)


def get_all(file_name):
    data = dict()
    temp_doc, temp_folder, time_doc = to_zip(file_name)
    for root, dirs, files in os.walk(os.path.join(temp_folder, 'docProps')):
        for file in files:
            if Path(file).suffix[1:] == 'xml':
                tree_app = ElementTree.parse(os.path.join(temp_folder, 'docProps', file))
                nodes = dict()
                for node in tree_app.iter():
                    nodes[node.tag] = node
                for elem in nodes:
                    idx = elem.find('}') + 1
                    data[elem[idx:]] = nodes[elem].text
    from_zip(temp_doc, temp_folder, time_doc)
    return data


def get_exif(file_name):
    tags = ExifTags.TAGS
    img = Image.open(file_name)
    exif = img.getexif()
    nodes = dict()
    for tag in exif:
        nodes[tags.get(tag, 'DefAttr')] = exif[tag]
    return nodes


def find(file_name, data):
    img = Image.open(file_name)
    exif = img.getexif()
    model = exif.get(272)
    if model:
        if model not in data:
            return file_name, model
    return


def get_other(filename):
    parser = createParser(filename)
    if not parser:
        return None

    with parser:
        try:
            metadata = extractMetadata(parser)
        except Exception as err:
            return None
    if not metadata:
       return None
    return metadata.exportPlaintext()


def get_metadata(filename):
    filetype = Path(filename).suffix[1:].lower()
    if filetype in ('docx', 'pptx', 'xlsx'):
        data = get_all(filename)
        res = []
        for node in data:
            res.append(f'{node}: {data[node]}')
        return res
    elif filetype == 'jpeg' or filetype == 'jpg':
        data = get_exif(filename)
        res = []
        for node in data:
            res.append(f'{node}: {data[node]}')
        return res
    else:
        return get_other(filename)


if __name__ == '__main__':
    file_name = 'Docs/1.jpg'
    print(find(file_name, ('Nikon',)))
