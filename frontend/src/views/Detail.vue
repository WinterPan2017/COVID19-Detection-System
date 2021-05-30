<template>
  <div style="background-color: #ececec; padding: 20px; height: 100%">
    <a-row :gutter="16">
      <a-card style="width: 100%; height: 100%; float: right" :bordered="true">
        <a-descriptions title="检测记录" layout="horizontal">
          <a-descriptions-item label="命名">
            {{ info.name }}
          </a-descriptions-item>
          <a-descriptions-item label="创建时间">
            {{ info.time }}
          </a-descriptions-item>
          <a-descriptions-item label="影像数量">
            {{ info.num }}
          </a-descriptions-item>
          <a-descriptions-item label="描述">
            {{ info.description }}
          </a-descriptions-item>
          <a-descriptions-item label="类型">
            <a-tag
              :key="info.category"
              :color="info.category === 'CXR' ? 'CornflowerBlue' : 'BurlyWood '"
            >
              {{ info.category }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="诊断">
            <a-tag
              style="margin-left: 10px"
              :color="
                info.diagnosis === 'COVID-19'
                  ? 'red'
                  : info.diagnosis === 'CAP'
                  ? 'yellow'
                  : 'green '
              "
            >
              {{ info.diagnosis }}
            </a-tag>
          </a-descriptions-item>
        </a-descriptions>
        <a-divider type="horizontal" />

        <a-descriptions title="分析详情" />
        <a-table :columns="columns" :data-source="data">
          <span slot="category" slot-scope="category">
            <a-tag
              :key="category"
              :color="category === 'CXR' ? 'CornflowerBlue' : 'BurlyWood '"
            >
              {{ category.toUpperCase() }}
            </a-tag>
          </span>
          <span slot="diagnosis" slot-scope="diagnosis">
            <a-tag
              :key="diagnosis"
              :color="
                diagnosis === 'COVID-19'
                  ? 'red'
                  : diagnosis === 'CAP'
                  ? 'yellow'
                  : 'green'
              "
            >
              {{ diagnosis.toUpperCase() }}
            </a-tag>
          </span>
          <span slot="action" slot-scope="record">
            <a-button
              type="primary"
              icon="file-image"
              size="large"
              @click="showImages(record)"
            >
              显示
            </a-button>
          </span>
        </a-table>
        <a-row :gutter="16">
          <!-- 原始图片 -->
          <a-col :span="8">
            <a-card hoverable style="width: 90%; margin: auto" title="原始图像">
              <img
                slot="cover"
                alt="选取对应文件即可显示"
                :src="rawImageOnShow"
              />
            </a-card>
          </a-col>
          <!-- 分割可视化图片 -->
          <a-col :span="8">
            <a-card
              hoverable
              style="width: 90%; margin: auto"
              title="疑似感染区域标注"
            >
              <img
                slot="cover"
                alt="选取对应文件即可显示"
                :src="annotationImageOnShow"
              />
            </a-card>
          </a-col>
          <!-- 分析 -->
          <a-col :span="8">
            <a-card hoverable style="width: 90%; margin: auto" title="分析">
            </a-card>
          </a-col>
        </a-row>
      </a-card>
    </a-row>
  </div>
</template>
<script>
const columns = [
  {
    title: "文件名",
    dataIndex: "filename",
    key: "filename",
  },

  {
    title: "类型",
    dataIndex: "category",
    key: "category",
    scopedSlots: { customRender: "category" },
  },
  {
    title: "诊断",
    key: "diagnosis",
    dataIndex: "diagnosis",
    scopedSlots: { customRender: "diagnosis" },
  },
  {
    title: "操作",
    key: "action",
    scopedSlots: { customRender: "action" },
  },
];
import reqwest from "reqwest";
import { getCookie } from "../utils/cookie.js";
export default {
  data() {
    return {
      drecord: this.$route.params.drecord,
      rawImageOnShow: "../assets/CT.png",
      annotationImageOnShow: "../assets/CT.png",
      info: {
        name: "name",
        description: "description",
        time: "time",
        num: 1,
        diagnosis: "COVID-19",
      },
      data: [
        {
          category: "CT",
          description: "this is a test for Normal",
          diagnosis: "Normal",
          key: 1,
          name: "ct test1",
          num: 1,
          time: "2021-04-15 12:45:40",
        },
      ],
      columns,
    };
  },
  created() {
    // 检查是否登录
    let _token = getCookie("token");
    if (_token === undefined || _token == "") {
      this.$router.replace("/Login");
    } else {
      this.drecord = this.$route.params.drecord;
      // 检查是否获取到drecordid
      if (this.drecord == undefined) {
        this.$router.replace("/Home/Record");
      } else {
        // 请求文件列表
        reqwest({
          url: "http://127.0.0.1:5000/getRecordDetail",
          method: "get",
          headers: {
            token: getCookie("token"),
          },
          data: { drecord: this.drecord },
          success: (e) => {
            console.log("sucess", e);
            this.data = e.arecords;
            this.info = e.info;
          },
          error: () => {},
        });
      }
    }
  },
  methods: {
    // 切换显示图像
    showImages(record) {
      reqwest({
        url: "http://127.0.0.1:5000/getImage",
        method: "get",
        responseType: "arraybuffer",
        data: { arecordid: record.arecordid, israw: true },
        success: (e) => {
          this.rawImageOnShow = "data:image/png;base64," + e.response;
        },
        error: () => {},
      });
      reqwest({
        url: "http://127.0.0.1:5000/getImage",
        method: "get",
        responseType: "arraybuffer",
        data: { arecordid: record.arecordid, israw: false },
        success: (e) => {
          this.annotationImageOnShow = "data:image/png;base64," + e.response;
        },
        error: () => {},
      });
    },
  },
};
</script>

<style scoped>
.space-align-container {
  display: flex;
  /* align-item: flex-start; */
  flex-wrap: wrap;
  /* width: 100%;
  height: 100%; */
}
.space-align-block {
  margin: 8px 4px;
  border: 1px solid #40a9ff;
  padding: 4px;
  flex: none;
  width: 100%;
  height: 100%;
}
.space-align-block .mock-block {
  display: inline-block;
  padding: 32px 8px 16px;
  background: rgba(150, 150, 150, 0.2);
}
</style>