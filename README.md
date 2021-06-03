<!--
 * @Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
 * @Author: Winter
 * @Email: 837950571@qq.com
 * @Date: 2021-05-30 09:35:49
 * @LastEditTime: 2021-06-03 14:30:27
-->
# 新冠肺炎辅助检测系统
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

