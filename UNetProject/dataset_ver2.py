import logging
import numpy as np
import torch
from PIL import Image
from os import listdir
from os.path import splitext, isfile, join
from pathlib import Path
from torch.utils.data import Dataset
from torchvision import transforms


class MyDataset(Dataset):
    def __init__(self, images_dir: str, mask_dir: str, scale: float = 1.0):
        self.images_dir = Path(images_dir)
        self.mask_dir = Path(mask_dir)
        assert 0 < scale <= 1, 'Scale must be between 0 and 1'
        self.scale = scale

        self.ids = [splitext(file)[0] for file in listdir(images_dir) if
                    isfile(join(images_dir, file)) and not file.startswith('.')]
        if not self.ids:
            raise RuntimeError(f'No input file found in {images_dir}, make sure you put your images there')

        logging.info(f'Creating dataset with {len(self.ids)} examples')
        self.mask_values = [False, True]

    def __len__(self):
        return len(self.ids)

    @staticmethod
    def preprocess(mask_values, pil_img, scale, is_mask):
        w, h = pil_img.size
        newW, newH = int(scale * w), int(scale * h)
        assert newW > 0 and newH > 0, 'Scale is too small, resized images would have no pixel'
        pil_img = pil_img.resize((newW, newH), resample=Image.NEAREST if is_mask else Image.BICUBIC)
        img = np.asarray(pil_img)

        if is_mask:
            mask = np.zeros((newH, newW), dtype=np.int64)
            for i, v in enumerate(mask_values):
                if img.ndim == 2:
                    mask[img == v] = i
                else:
                    mask[(img == v).all(-1)] = i

            return mask

        else:
            if img.ndim == 2:
                img = img[np.newaxis, ...]
            else:
                img = img.transpose((2, 0, 1))

            if (img > 1).any():
                img = img / 255.0

            return img

    def preprocess_mask(self, mask_values, pil_mask, scale):
        w, h = pil_mask.size
        newW, newH = int(scale * w), int(scale * h)
        assert newW > 0 and newH > 0, 'Scale is too small, resized masks would have no pixel'
        pil_mask = pil_mask.resize((newW, newH), resample=Image.NEAREST)
        mask = np.asarray(pil_mask)

        new_mask = np.zeros((newH, newW), dtype=np.int64)
        for i, v in enumerate(mask_values):
            if mask.ndim == 2:
                new_mask[mask == v] = i
            else:
                new_mask[(mask == v).all(-1)] = i

        return new_mask

    def apply_transforms(self, img, mask):
        # Define image transformation operations
        transform = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),  # Random horizontal flip
            transforms.RandomVerticalFlip(p=0.5),  # Random vertical flip
            transforms.RandomResizedCrop((695, 695), scale=(0.5, 1), ratio=(0.5, 2))
            # Add other transformation operations as needed...
        ])

        # Convert PIL Image to PyTorch Tensor
        img_tensor = torch.as_tensor(np.asarray(img)).float().contiguous()
        mask_tensor = torch.as_tensor(self.preprocess_mask(self.mask_values, mask, self.scale)).long().contiguous()

        # Apply image augmentation to both image and mask
        augmented_img = transform(img_tensor)

        # Ensure the mask is not transformed spatially (e.g., resizing)
        # You can add other operations specific to mask processing if needed
        augmented_mask = mask_tensor

        return augmented_img, augmented_mask

    def __getitem__(self, idx):
        name = self.ids[idx]
        mask_file = list(self.mask_dir.glob(name + '.*'))
        img_file = list(self.images_dir.glob(name + '.*'))

        assert len(img_file) == 1, f'Either no image or multiple images found for the ID {name}: {img_file}'
        assert len(mask_file) == 1, f'Either no masks or multiple masks found for the ID {name}: {mask_file}'
        mask = Image.open(mask_file[0])
        img = Image.open(img_file[0])

        assert img.size == mask.size, \
            f'Image and masks {name} should be the same size, but are {img.size} and {mask.size}'

        # Image preprocessing
        img = self.preprocess(self.mask_values, img, self.scale, is_mask=False)
        mask = self.preprocess(self.mask_values, mask, self.scale, is_mask=True)

        # Apply additional transforms
        img, mask = self.apply_transforms(img, mask)

        return {
            'image': img,
            'mask': mask
        }


if __name__ == '__main__':
    dir_img = './data/imgs/'
    dir_mask = './data/masks/'

    dataset = MyDataset(dir_img, dir_mask)
