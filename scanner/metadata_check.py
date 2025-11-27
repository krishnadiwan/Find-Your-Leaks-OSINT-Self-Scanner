# File: scanner/metadata_check.py

from PIL import Image, ExifTags
import io
import piexif

def extract_metadata(uploaded_file):
    """
    Extracts clean, human-readable EXIF metadata.
    Removes binary/unreadable fields automatically.
    """
    try:
        img_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(img_bytes))
        metadata = {}

        # --- PIL EXIF ---
        exif_data = getattr(image, "_getexif", lambda: None)()
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, tag_id)
                if isinstance(value, (bytes, bytearray)):
                    continue  # skip binary data
                metadata[tag_name] = str(value)

        # --- piexif (more complete) ---
        try:
            exif_dict = piexif.load(img_bytes)
            for ifd in exif_dict:
                for tag in exif_dict[ifd]:
                    tag_name = piexif.TAGS[ifd][tag]["name"]
                    value = exif_dict[ifd][tag]
                    if isinstance(value, (bytes, bytearray)):
                        continue
                    metadata[tag_name] = str(value)
        except Exception:
            pass

        # --- Filter only readable text ---
        clean_meta = {k: v for k, v in metadata.items() if len(str(v)) < 200}

        if not clean_meta:
            return {"Info": "No EXIF metadata found in this image."}

        return clean_meta

    except Exception as e:
        return {"Error": str(e)}
