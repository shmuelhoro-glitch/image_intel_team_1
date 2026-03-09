from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os
from function import dms_to_decimal
"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def has_gps(data: dict):

    if  34853 in data:
        return True
    else:
        return False
















def latitude(data: dict):
     ref=data.get(1)
     dms_to=data.get(2)
     if ref is None or dms_to is None:
         return None
     return dms_to_decimal(dms_to,ref)

















def longitude(data: dict):
    ref = data.get(3)
    dms_to = data.get(4)
    if ref is None or dms_to is None:
        return None
    return dms_to_decimal(dms_to, ref)












def datatime(data: dict):
    try:
        return data["DateTime"].replace(":", "-", 2)
    except KeyError:
        return None













def camera_make(data: dict):
    try:
        return data["Make"].strip("\x00")
    except KeyError:
        return None














def camera_model(data: dict):
    try:
        return data["Model"].strip("\x00")
    except KeyError:
        return None














def extract_metadata(image_path):
    path = Path(image_path)
    if path.suffix.lower() == ".jpg":
        with Image.open(image_path)as img:
            all_exif=img.getexif()

            exif = {}

            for tag_id, value in all_exif.items():
                new_tag_id=TAGS.get(tag_id,tag_id)
                exif[new_tag_id]=value
            return exif



    return None

















    # """
    # שולף EXIF מתמונה בודדת.
    #
    # Args:
    #     image_path: נתיב לקובץ תמונה
    #
    # Returns:
    #     dict עם: filename, datetime, latitude, longitude,
    #           camera_make, camera_model, has_gps
    # """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    listi=[]
    for fill in folder_path:
       dicti=extract_metadata(fill)
       listi.append(dicti)














