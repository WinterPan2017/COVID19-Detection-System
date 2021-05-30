"""
Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-03-04 09:54:36
LastEditTime: 2021-03-04 09:54:36
"""
# import torchvision.transforms as transforms
import torch
# import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import numpy as np
import torch
import cv2


class CamExtractor:
    """
        Extracts cam features from the model
    """

    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None

    def save_gradient(self, grad):
        self.gradients = grad

    def forward_pass(self, x):
        """
            Does a full forward pass on the model
        """
        conv_output = None
        for module_pos, module in self.model._modules.items():
            x = module(x)  # Forward
            if module_pos == self.target_layer:
                x.register_hook(self.save_gradient)
                conv_output = x  # Save the convolution output on that layer
                # x = x.view(x.size(0), x.size(1))
            if module_pos == "avgpool":
                x = x.view(x.size(0), x.size(1))
        return conv_output, x


class GradCam:
    """
        Produces class activation map
    """

    def __init__(self, model, target_layer):
        self.model = model
        self.model.eval()
        # Define extractor
        self.extractor = CamExtractor(self.model, target_layer)

    def generate_cam(self, input_image, target_class=None):
        # Full forward pass
        # conv_output is the output of convolutions at specified layer
        # model_output is the final output of the model (1, 1000)
        conv_output, model_output = self.extractor.forward_pass(input_image)
        if target_class is None:
            target_class = np.argmax(model_output.data.numpy())
        # Target for backprop
        one_hot_output = torch.FloatTensor(1, model_output.size()[-1]).zero_()
        one_hot_output[0][target_class] = 1
        # Zero grads
        self.model.zero_grad()
        # Backward pass with specified target
        model_output.backward(gradient=one_hot_output, retain_graph=True)
        # Get hooked gradients
        guided_gradients = self.extractor.gradients.data.numpy()[0]
        # Get convolution outputs
        target = conv_output.data.numpy()[0]
        # Get weights from gradients
        weights = np.mean(
            guided_gradients, axis=(1, 2)
        )  # Take averages for each gradient
        # Create empty numpy array for cam
        cam = np.ones(target.shape[1:], dtype=np.float32)
        # Multiply each weight with its conv output and then, sum
        for i, w in enumerate(weights):
            cam += w * target[i, :, :]
        cam = np.maximum(cam, 0)
        cam = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))  # Normalize between 0-1
        cam = np.uint8(cam * 255)  # Scale between 0-255 to visualize
        cam = (
            np.uint8(
                Image.fromarray(cam).resize(
                    (input_image.shape[2], input_image.shape[3]), Image.ANTIALIAS
                )
            )
            / 255
        )
        # ^ I am extremely unhappy with this line. Originally resizing was done in cv2 which
        # supports resizing numpy matrices with antialiasing, however,
        # when I moved the repository to PIL, this option was out of the window.
        # So, in order to use resizing with ANTIALIAS feature of PIL,
        # I briefly convert matrix to PIL image and then back.
        # If there is a more beautiful way, do not hesitate to send a PR.

        # You can also use the code below instead of the code line above, suggested by @ ptschandl
        # from scipy.ndimage.interpolation import zoom
        # cam = zoom(cam, np.array(input_image[0].shape[1:])/np.array(cam.shape))
        return cam


if __name__ == "__main__":
    from models import resnet18
    from dataset import COVID19ChestXRay

    print("=> loading checkpoint")
    checkpoint = torch.load(
        "/home/winter/Projects/cv/covid19/2dconv-x-ray/checkpoints/image0_255_DA_resnet18_folder1val_3classes.model_best.pth.tar"
    )
    model = resnet18(num_classes=3)
    model.load_state_dict(checkpoint["state_dict"])

    for param in model.parameters():
        param.requires_grad = True

    for module_pos, module in model._modules.items():
        print(module_pos)

    train_dataset = COVID19ChestXRay(
        "/home/winter/Projects/cv/x-ray/COVID-19_Radiography_Database/COVID-19_Radiography_Dataset",
        "./train.csv",
        "Valid",
    )

    model.eval()
    for img, label in train_dataset:
        if label != 2:
            continue
        grad_cam = GradCam(model, target_layer="layer4")
        # Generate cam mask
        cam = grad_cam.generate_cam(torch.unsqueeze(img, 0), None)
        plt.subplot(1, 3, 1)
        # plt.title(label)
        plt.imshow(img.data.numpy()[0], cmap=plt.cm.gray)
        plt.axis("off")
        plt.subplot(1, 3, 2)
        cam = cam * 255
        cam = cam.astype(np.uint8)
        cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        cam = cv2.cvtColor(cam, cv2.COLOR_RGB2BGR)
        plt.imshow(cam, cmap=plt.cm.gray)
        plt.axis("off")
        plt.subplot(1, 3, 3)
        img = img.numpy()
        img = np.transpose(np.stack((img[0], img[0], img[0])), (1, 2, 0))
        img = (cam * 0.3 + img * 0.7).astype(np.uint8)
        plt.imshow(img, cmap=plt.cm.gray)
        plt.axis("off")
        plt.show()

        # break

