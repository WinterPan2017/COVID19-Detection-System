<template>
  <a-table :columns="columns" :data-source="data">
    <a slot="name" slot-scope="text">{{ text }}</a>
    <span slot="customTitle"><a-icon type="smile-o" /> 名称</span>
    <span slot="category" slot-scope="category">
      <a-tag
        :key="category"
        :color="
          category.toUpperCase() === 'CXR' ? 'CornflowerBlue' : 'BurlyWood '
        "
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
      <a-divider type="vertical" />
      <a-popconfirm
        title="Are you sure delete this task?"
        ok-text="Yes"
        cancel-text="No"
        @confirm="confirmDelete(record)"
      >
        <a class="ant-dropdown-lin">删除</a>
      </a-popconfirm>

      <a-divider type="vertical" />
      <a class="ant-dropdown-link" @click="download(record)"> 下载 </a>
      <a-divider type="vertical" />
      <a class="ant-dropdown-link" @click="showDetail(record)"> 详情 </a>
    </span>
  </a-table>
</template>
<script>
const columns = [
  {
    dataIndex: "name",
    key: "name",
    slots: { title: "customTitle" },
    scopedSlots: { customRender: "name" },
  },
  {
    title: "时间",
    dataIndex: "time",
    key: "time",
  },
  {
    title: "数量",
    dataIndex: "num",
    key: "num",
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

const data = [];
import reqwest from "reqwest";
import { getCookie } from "../utils/cookie.js";
export default {
  data() {
    return {
      data,
      columns,
    };
  },
  created() {
    let _token = getCookie("token");
    if (_token === undefined || _token == "") {
      this.$router.replace("/Login");
    } else {
      reqwest({
        url: "http://127.0.0.1:5000/getRecord",
        method: "get",
        headers: {
          token: _token,
        },
        data: {},
        success: (e) => {
          console.log("sucess", e);
          this.data = e;
        },
        error: () => {},
      });
    }
  },
  methods: {
    showDetail(record) {
      console.log(record);
      this.$router.replace({
        name: "Detail",
        params: {
          drecord: record.key,
        },
      });
    },
    confirmDelete(e) {
      console.log("delete", e);
      // 提交服务器
      reqwest({
        url: "http://127.0.0.1:5000/deleteRecord",
        method: "get",
        headers: {
          token: getCookie("token"),
        },
        data: { drecord: e.key },
        success: (e) => {
          console.log("sucess", e);
        },
        error: () => {},
      });
      // 更新本地
      for (let i = 0; i < this.data.length; i++) {
        if (this.data[i].key == e.key) this.data.splice(i, 1);
      }
      this.$message.success("删除成功");
    },
    // 将监听操作写在methods里面，removeEventListener取消监听内容必须跟开启监听保持一致
    backChange() {
      this.$emit("change", false);
    },
    // 下载
    download(record) {
      const xhr = new XMLHttpRequest();

      xhr.open(
        "GET",
        "http://127.0.0.1:5000/downloadRecord" +
          encodeURI("?drecord=" + record.key),
        true
      );
      xhr.setRequestHeader("token", getCookie("token"));
      xhr.responseType = "blob";
      xhr.onerror = function () {
        alert("请求失败");
      };
      xhr.onload = () => {
        if (xhr.status === 200) {
          console.log("xhr sucess", xhr);
          if (xhr.response.type == "application/json") {
            console.log(xhr.response.type != "application/json");
            return;
          }
          const a = document.createElement("a");
          const blob = new Blob([xhr.response], { type: "application/zip" });
          const url = window.URL.createObjectURL(blob);
          a.href = url;
          a.download = "1.zip";
          a.click();
          window.URL.revokeObjectURL(url);
        }
      };

      xhr.send();
      // const a = document.createElement("a");
      // a.setAttribute("href", href);
      // a.setAttribute("download", title);
      // a.click();
    },
  },
  // 挂载完成后，判断浏览器是否支持popstate
  mounted() {
    if (window.history && window.history.pushState) {
      // 往历史记录里面添加一条新的当前页面的url
      history.pushState(null, null, document.URL);
      // 给 popstate 绑定一个方法 监听页面刷新
      window.addEventListener("popstate", this.backChange, false);
    }
  },

  // 页面销毁时，取消监听。否则其他vue路由页面也会被监听
  destroyed() {
    // window.removeListener("popstate", this.backChange, false);
  },
};
</script>
