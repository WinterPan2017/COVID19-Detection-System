'''
Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-04-15 13:41:02
LastEditTime: 2021-04-26 20:46:41
'''
from abc import abstractclassmethod, ABCMeta
import os
import cv2
import SimpleITK as sitk
import torch
import numpy as np

# import for CXR
from utils.resnet import resnet18
from utils.GradCAM import GradCam

# import for CT
import utils.densenet as models
import utils.lungseg.mask
from utils.unet import UNet


class Detector(metaclass=ABCMeta):
    """检测的基类"""
    @abstractclassmethod
    def predict(self, image):
        """进行分类"""
        pass

    @abstractclassmethod
    def annotate(self, image):
        """病灶标注"""
        pass

    @abstractclassmethod
    def detect(self, folder):
        """对外接口"""
        pass


class CXRDetector(Detector):
    def __init__(self, ):
        self.model_path = "/home/winter/Projects/cv/covid19/2dconv-x-ray/checkpoints/image0_255_DA_resnet18_folder1val_3classes.model_best.pth.tar"
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        self.model = resnet18(num_classes=3)
        checkpoint = torch.load(self.model_path)
        self.model.load_state_dict(checkpoint["state_dict"])

    def predict(self, image):
        self.model.to(device=self.device)
        self.model.eval()
        image = image.to(device=self.device)
        with torch.no_grad():
            output = self.model(image)
            _, pred = torch.max(output, 1)
            pred = pred.cpu().numpy()[0]
        return {0: "COVID-19", 1: "Normal", 2: "CAP"}[pred]

    def annotate(self, image):
        # force to use cpu
        self.model.to(torch.device("cpu"))
        for param in self.model.parameters():
            param.requires_grad = True
        grad_cam = GradCam(self.model, target_layer="layer4")
        cam = grad_cam.generate_cam(image, None)
        cam = cam * 255
        cam = cam.astype(np.uint8)
        cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        cam = cv2.cvtColor(cam, cv2.COLOR_RGB2BGR)
        image = image.numpy()[0]
        image = np.transpose(np.stack((image[0], image[0], image[0])),
                             (1, 2, 0))
        return (cam * 0.3 + image * 0.7).astype(np.uint8)

    def detect(self, folder):
        # 只允许单张
        assert len(os.listdir(folder)) == 1
        filepath = os.path.join(folder, os.listdir(folder)[0])
        # 读取文件
        _, suffix = os.path.splitext(filepath)
        suffix = suffix.lower()
        assert len(suffix) > 1

        rawimage = None
        if suffix in [".png", ".jpeg", ".jpg"]:
            rawimage = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        elif suffix in [".dcm", ".gz"]:
            rawimage = SimpleITK.GetArrayFromImage(
                SimpleITK.ReadImage(filepath))
        else:
            raise Exception(
                f"read image failed with unsupported format {suffix}")
        assert len(rawimage.shape) == 2

        # 对应的预处理
        image = cv2.resize(rawimage, (299, 299))
        image = (image - image.min()) / (image.max() - image.min()) * 255
        image = image.astype(np.uint8)
        image = torch.from_numpy(image[np.newaxis, np.newaxis, :, :]).type(
            torch.FloatTensor)
        # 检测得到分类结果
        diagnosis = self.predict(image)

        annotationimage = None
        # 阳性获取CAM
        if diagnosis != "Normal":
            annotationimage = self.annotate(image)
            annotationimage = cv2.resize(annotationimage, rawimage.shape)

        return diagnosis, rawimage, annotationimage


class CTDetector(Detector):
    def __init__(self, ):
        self.device = torch.device("cpu")
        if torch.cuda.is_available():
            self.device = torch.device("cuda")

    def predict2d(self, image):
        device = self.device
        checkpoints_path = "./utils/densenet121_5000_3CTxmask.pth"
        checkpoints = torch.load(checkpoints_path)
        model = models.__dict__[checkpoints["arch"]](num_classes=3)
        model.load_state_dict(checkpoints["state_dict"])
        model.eval()
        model.to(device=device)
        with torch.no_grad():
            image = torch.from_numpy(image).type(torch.FloatTensor)
            image = image.to(device=device)
            output = model(image)
            _, pred = torch.max(output, 1)
            return pred.cpu().numpy().item()

    def predict3d(self, image):
        # resample
        imgs = image
        device = self.device
        checkpoints_path = "./utils/densenet121_5000_3CTxmask.pth"
        topk = 3
        checkpoints = torch.load(checkpoints_path)
        model = models.__dict__[checkpoints["arch"]](num_classes=3)
        model.load_state_dict(checkpoints["state_dict"])
        model.eval()
        model.to(device=device)

        results = []
        with torch.no_grad():
            output = []
            i = 0
            b = 20
            while i + b < imgs.shape[0]:
                img = imgs[i:i + b].astype(np.float32)
                img = torch.from_numpy(img).type(torch.FloatTensor)
                img = img.to(device=device)
                o = model(img)
                o = o.cpu()
                output.append(o)
                i += b
            if imgs.shape[0] - i > 0:
                img = imgs[i:imgs.shape[0]].astype(np.float32)
                img = torch.from_numpy(img).type(torch.FloatTensor)
                img = img.to(device=device)
                o = model(img)
                o = o.cpu()
                output.append(o)
            output = torch.cat(output, 0)

            # fusion block for patient level predict
            output_softmax = torch.nn.functional.softmax(output, dim=1)
            scores = torch.zeros(3)
            scores[0] = output_softmax[:, 0].mean()
            values, _ = output_softmax.topk(k=topk, dim=0)
            scores[1] = values.mean(dim=0)[1]
            scores[2] = values.mean(dim=0)[2]
            _, pred = scores.max(0)

        return pred.item()

    def predict(self, image):
        shape = sitk.GetArrayFromImage(image).shape
        # 单张
        if shape[0] == 1:
            mask = utils.lungseg.mask.apply(image)
            image = sitk.GetArrayFromImage(image)
            mask[mask != 0] = 1
            MAX_BOUND = 700
            MIN_BOUND = -1200
            image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
            image[image > 1] = 1
            image[image < 0] = 0
            image[mask == 0] = 0
            image = np.stack([image[0], image[0],
                              image[0]])[np.newaxis, :, :, :]
            diagnosis = self.predict2d(image)
        # 多张
        else:
            resample_slices = self.resample(image)
            preprocessed_slices = self.preprocess(resample_slices)
            diagnosis = self.predict3d(preprocessed_slices)
        return {0: "Normal", 1: "COVID-19", 2: "CAP"}[diagnosis]

    def resample(self, image, targetSliceThickness=2):
        """
            Resample to the same thickness
            Return:
                    resampled_slices, SimpleITK.SimpleITK.Image
        """
        original_spacing = image.GetSpacing()
        if original_spacing[2] == targetSliceThickness:
            return image

        original_size = image.GetSize()

        resample = sitk.ResampleImageFilter()
        resample.SetInterpolator(sitk.sitkLinear)
        resample.SetDefaultPixelValue(0)

        new_spacing = [original_spacing[0], original_spacing[1], 2]
        resample.SetOutputSpacing(new_spacing)
        resample.SetOutputOrigin(image.GetOrigin())
        resample.SetOutputDirection(image.GetDirection())

        size = [
            int(
                np.round(original_size[0] *
                         (original_spacing[0] / new_spacing[0]))),
            int(
                np.round(original_size[1] *
                         (original_spacing[1] / new_spacing[1]))),
            int(
                np.round(original_size[2] *
                         (original_spacing[2] / new_spacing[2]))),
        ]
        resample.SetSize(size)
        image = resample.Execute(image)
        return image

    def preprocess(self, slices, lung_area_threshold=5000):
        """
            Obtain the results of lung segmentation, slice select, and preprocess
            return:
                    preprocessed_slices, numpy.ndiarray, shape (N, 3, 512, 512)
        """
        masks = utils.lungseg.mask.apply(slices,
                                         batch_size=10,
                                         force_cpu=False)
        slices = sitk.GetArrayFromImage(slices)
        new_slices = []
        for i in range(slices.shape[0]):
            mask = masks[i]
            if mask.sum() <= lung_area_threshold:
                continue
            mask[mask != 0] = 1
            s = slices[i]
            MAX_BOUND = 700
            MIN_BOUND = -1200
            s = (s - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
            s[s > 1] = 1
            s[s < 0] = 0
            s[mask == 0] = 0
            new_slices.append(np.stack([s, s, s]))
        new_slices = np.stack(new_slices)
        return new_slices

    def annotate(self, image):
        original_image = ((image - image.min()) / (image.max() - image.min()) *
                          255).astype(np.uint8)
        image = np.clip(image, -1250, 250)
        image = ((image + 1250) / 1500 * 255).astype(np.uint8)
        device = self.device
        checkpoint = torch.load(
            "./utils/unet_dataaugmentation.model_best.pth.tar")
        model = UNet(1, 1, bilinear=True)
        model.load_state_dict(checkpoint["state_dict"])
        model.eval()
        model.to(device=device)
        with torch.no_grad():
            image = torch.from_numpy(image[np.newaxis, np.newaxis, :, :]).type(
                torch.FloatTensor).to(device=device)
            pred = model(image)
            pred = torch.sigmoid(pred)
            pred = (pred > 0.5).float().cpu().detach().numpy().astype(
                np.uint8)[0][0]
            contours, _ = cv2.findContours(pred, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
            image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
            print(pred.sum())
            cv2.drawContours(image, contours, -1, (0, 0, 255), 1)
            image[:, :, 2][pred == 1] = 150
        return image

    def detect(self, folder):
        sitkimage = None
        # 单个文件
        if len(os.listdir(folder)) == 1:
            filepath = os.path.join(folder, os.listdir(folder)[0])
            # 读取文件
            _, suffix = os.path.splitext(filepath)
            suffix = suffix.lower()
            assert len(suffix) > 1
            if suffix in [".dcm", ".gz"]:
                sitkimage = sitk.ReadImage(filepath)
            else:
                raise Exception(
                    f"read image failed with unsupported format {suffix}")
        # 多个连续文件构成3dCT
        else:
            reader = sitk.ImageSeriesReader()
            dicom_names = reader.GetGDCMSeriesFileNames(folder)
            reader.SetFileNames(dicom_names)
            sitkimage = reader.Execute()

        if len(sitk.GetArrayFromImage(sitkimage).shape) == 2:
            sitkimage = sitk.GetImageFromArray(
                sitk.GetArrayFromImage(sitkimage)[np.newaxis, :, :])
        # 已获取文件 rawimage (N, W, H)
        print("ct ", sitk.GetArrayFromImage(sitkimage).shape)
        diagnosis = self.predict(sitkimage)

        image = sitk.GetArrayFromImage(sitkimage)
        # 获取每个切片的诊断
        slices = []
        for i in range(image.shape[0]):
            slice_diagnosis = self.predict(
                sitk.GetImageFromArray(image[i:i + 1]))
            # 处理到0-255便于查看
            rawimage = ((image[i] - image[i].min()) /
                        (image[i].max() - image[i].min()) * 255).astype(
                            np.uint8)
            annotationimage = None
            print(i, slice_diagnosis)
            if slice_diagnosis != "Normal":
                annotationimage = self.annotate(image[i])
                if slice_diagnosis != diagnosis:
                    slice_diagnosis = diagnosis
            slices.append([slice_diagnosis, rawimage, annotationimage])
        return diagnosis, slices


if __name__ == "__main__":
    # d = CXRDetector().detect("./images/temp")
    import time
    start = time.time()
    d = CTDetector().detect(
        "/home/winter/Projects/cv/covid19/dataset/SPGC-Test/SPGC-Test1/T1-001")
    print(time.time() - start)
