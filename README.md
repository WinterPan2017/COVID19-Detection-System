<!--
 * @Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
 * @Author: Winter
 * @Email: 837950571@qq.com
 * @Date: 2021-05-30 09:35:49
 * @LastEditTime: 2021-06-03 14:40:11
-->
# 新冠肺炎辅助检测系统
## 简介
新冠肺炎疫情爆发以来在全球已感染超 1 亿人，给人类社会带来巨大的危害。由于其传染性强，快速筛查新冠肺炎感染者并及时隔离治疗，对控制疫情传播尤为重要。为助力新冠肺炎快速诊断，设计实现了基于医学图像的新冠肺炎辅助检测系统。系统能够检测 CXR 和 CT 影像是否表现为感染新冠肺炎或社区获得性肺炎，并对诊断为感染新冠肺炎的影像的疑似病灶区域进行自动标注。系统的核心检测算法表现优异，在测试集上 CXR 诊断、CT 切片级诊断、CT 病例级诊断的准确度为 98.1%、99.6%、76.7%，CT 病灶分割的 DSC 系数为 0.623。其中 CT 病例级检测方案在 IEEE ICASSP 2021 Signal Processing Grand Challenge (SPGC) on COVID-19 Diagnosis 比赛中获得第十名的成绩。

系统采用B/S架构, 前端基于Vue.js和Ant Design, 后端基于flask, 算法开发基于Pytorch.

## 检测流程
![image](https://github.com/WinterPan2017/COVID19-Detection-System/blob/master/images/detection.gif?raw=true)
## 核心算法
### CXR检测
### CT检测
#### case-level
![image](https://github.com/WinterPan2017/COVID19-Detection-System/blob/master/images/CT-d.png?raw=true)
#### slice-level
![image](https://github.com/WinterPan2017/COVID19-Detection-System/blob/master/images/ct-sd.png?raw=true)
### CT病灶分割
![image](https://github.com/WinterPan2017/COVID19-Detection-System/blob/master/images/ct-seg.png?raw=true)
### CXR Grad-CAM
![image](https://github.com/WinterPan2017/COVID19-Detection-System/blob/master/images/cxr-cam.png?raw=true)
## 使用方式
1. 安装Python环境, 安装依赖
2. 安装node.js环境并安装对应依赖
3. 运行脚本 start.sh

