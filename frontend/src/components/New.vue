<template>
  <div style="background-color: #ececec; padding: 20px">
    <a-row :gutter="16">
      <!-- 提示栏 -->
      <a-col :span="6">
        <a-card style="width: 50%; float: left" :bordered="false">
          <p>使用说明</p>
          <a-timeline>
            <a-timeline-item
              >上传需要检测的影像文件(若包含完整的连续CT图像请压缩后上传)</a-timeline-item
            >
            <a-timeline-item>上传成功后,系统自动进行分析</a-timeline-item>
            <a-timeline-item>显示分析结果及对应的可视化</a-timeline-item>
          </a-timeline>
        </a-card>
      </a-col>
      <!-- 状态显示和上传栏 -->
      <a-col :span="12">
        <a-card
          style="width: 100%; height: 100%; float: right"
          :bordered="false"
        >
          <!-- 状态栏 -->
          <a-steps>
            <a-step :status="status.upload" title="upload">
              <a-icon slot="icon" :type="icon.upload" />
            </a-step>
            <a-step :status="status.analysis" title="analysis">
              <a-icon slot="icon" :type="icon.analysis" />
            </a-step>
            <a-step :status="status.done" title="done">
              <a-icon slot="icon" :type="icon.done" />
            </a-step>
          </a-steps>
          <a-divider></a-divider>
          <a-form>
            <a-form-item label="命名">
              <a-input :placeholder="name" v-model="name" />
            </a-form-item>
            <a-form-item label="描述">
              <a-input :placeholder="description" v-model="description" />
            </a-form-item>
            <a-form-item label="类别">
              <a-radio-group v-model="category" @change="onChange">
                <a-radio-button value="CXR"> CXR </a-radio-button>
                <a-radio-button value="CT"> CT </a-radio-button>
              </a-radio-group>
            </a-form-item>
          </a-form>
          <a-upload
            :file-list="fileList"
            :remove="handleRemove"
            :before-upload="beforeUpload"
          >
            <a-button> <a-icon type="upload" /> Select File </a-button>
          </a-upload>
          <a-button
            type="primary"
            :disabled="fileList.length === 0"
            :loading="uploading"
            style="margin-top: 16px; width: 100%"
            @click="handleUpload"
          >
            {{ uploading ? "Uploading" : "Start Upload" }}
          </a-button>
        </a-card>
      </a-col>
    </a-row>
    <a-modal
      title="结果"
      :visible="visible"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <p>{{ ModalText }}</p>
    </a-modal>
  </div>
</template>
<script>
// import reqwest from "reqwest";
import { getCookie } from "../utils/cookie.js";
export default {
  data() {
    return {
      status: { upload: "process", analysis: "wait", done: "wait" },
      icon: { upload: "loading", analysis: "line-chart", done: "check" },
      name: "Test001",
      description: "This is the first patient",
      category: "CXR",
      fileList: [],
      uploading: false,
      //弹窗
      ModalText: "分析完成, 是否前往分析记录页面查看",
      visible: false,
    };
  },
  created() {},
  methods: {
    // 类型选择
    onChange(e) {
      console.log(`checked = ${e.target.value}`);
    },
    // 文件上传
    handleRemove(file) {
      const index = this.fileList.indexOf(file);
      const newFileList = this.fileList.slice();
      newFileList.splice(index, 1);
      this.fileList = newFileList;
      this.status.upload = "process";
      this.icon.upload = "loading";
    },
    beforeUpload(file) {
      this.fileList = [...this.fileList, file];
      return false;
    },
    handleUpload() {
      var that = this;
      var formData = new FormData();
      this.fileList.forEach((file) => {
        formData.append("files[]", file);
      });
      formData.append("name", this.name);
      formData.append("description", this.description);
      formData.append("category", this.category);
      this.uploading = true;
      console.log("handleUpload", formData.get("files[]"));

      // 获取token
      let _token = getCookie("token");
      var xhr = new XMLHttpRequest();
      xhr.onerror = function () {
        alert("请求失败");
      };
      xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
          if (xhr.status == 200) {
            console.log("success", xhr.responseText);
            that.fileList = [];
            that.uploading = false;
            if (xhr.responseText == "success") {
              that.$message.success("upload successfully.");
              // 更改状态栏
              that.status.analysis = "finish";
              that.icon.analysis = "line-chart";
              that.status.done = "finish";
              that.icon.done = "check";
              //成功之后跳转到详情页面
              that.ModalText = "分析完成, 是否前往分析记录页面查看";
              that.visible = true;
            } else {
              that.$message.error(xhr.responseText);
              // 更改状态栏
              that.status.analysis = xhr.responseText;
              that.icon.analysis = "close";
            }
          } else {
            console.error("error", xhr.status);
            that.uploading = false;
            that.$message.error("upload failed.");
          }
        }
      };
      xhr.upload.onprogress = function (e) {
        console.log(e.loaded / e.total);
        if (e.loaded / e.total == 1) {
          console.log("uploading complete");
          // 更改状态栏
          that.status.upload = "finish";
          that.icon.upload = "cloud-upload";
          that.status.analysis = "process";
          that.icon.analysis = "loading";
        }
      };
      xhr.open("POST", "http://127.0.0.1:5000/upload", true);
      xhr.setRequestHeader("token", _token);
      xhr.send(formData);
    },
    //弹窗处理
    handleOk(e) {
      console.log("handleOk", e);
      this.$router.replace({
        path: "/home/record",
      });
      // 更改状态栏
      this.status.upload = "process";
      this.icon.upload = "loading";
      this.status.analysis = "wait";
      this.status.done = "wait";
    },
    handleCancel(e) {
      console.log("handleCancel", e);
      this.visible = false;
      // 更改状态栏
      this.status.upload = "process";
      this.icon.upload = "loading";
      this.status.analysis = "wait";
      this.status.done = "wait";
    },
  },
};
</script>
