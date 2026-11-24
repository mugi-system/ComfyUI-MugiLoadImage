import hashlib
import os

import numpy as np
import torch
from PIL import Image, ImageOps, ImageSequence

import folder_paths
import node_helpers


class MugiLoadImage:
    """Standard LoadImage + a memory of the originally chosen filename.

    The plain LoadImage widget gets rewritten to a clipspace temp file as
    soon as the mask editor saves, so the original filename is lost.
    This node keeps a second widget, ``original_filename``, which the
    frontend script (js/mugi_load_image.js) fills in whenever a real
    (non-clipspace) file is chosen. The Python side just passes it
    through as a STRING output (extension stripped).
    """

    @classmethod
    def INPUT_TYPES(cls):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir)
                 if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
                "original_filename": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("IMAGE", "MASK", "filename")
    FUNCTION = "load_image"
    CATEGORY = "mugi"

    def load_image(self, image, original_filename=""):
        image_path = folder_paths.get_annotated_filepath(image)
        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None
        excluded_formats = {"MPO"}

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)
            if i.mode == "I":
                i = i.point(lambda x: x * (1 / 255))
            image_rgb = i.convert("RGB")
            if w is None or h is None:
                w, h = image_rgb.size
            if image_rgb.size[0] != w or image_rgb.size[1] != h:
                continue
            image_arr = np.array(image_rgb).astype(np.float32) / 255.0
            image_t = torch.from_numpy(image_arr)[None, :]
            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image_t)
            output_masks.append(mask.unsqueeze(0))
            if img.format in excluded_formats:
                break

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (output_image, output_mask, self._stem(original_filename or image))

    @staticmethod
    def _stem(name):
        name = (name or "").strip()
        for suffix in (" [input]", " [output]", " [temp]"):
            if name.endswith(suffix):
                name = name[: -len(suffix)]
        base = os.path.basename(name.replace("\\", "/"))
        return os.path.splitext(base)[0]

    @classmethod
    def IS_CHANGED(cls, image, original_filename=""):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, "rb") as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(cls, image, original_filename=""):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True


NODE_CLASS_MAPPINGS = {
    "MugiLoadImage": MugiLoadImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MugiLoadImage": "Load Image (mugi / keeps filename)",
}

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
