<template>
  <div style="width: 100%; height: 100%; min-height: 100%; transition: 0.3s">
    <p style="font-weight: 500; color: #0d1a26; font-size: 24px">
      Workflow for patient-level detection
    </p>
    <a-divider></a-divider>
    <a-row :gutter="16">
      <a-col :span="6">
        <pdf
          src="http://127.0.0.1:5000/getIntroduction"
          :page="1"
          style="display: inline-block; width: 100%"
        ></pdf>
      </a-col>
      <a-col :span="6">
        <pdf
          src="http://127.0.0.1:5000/getIntroduction"
          :page="2"
          style="display: inline-block; width: 100%"
        ></pdf>
      </a-col>
      <a-col :span="6">
        <pdf
          src="http://127.0.0.1:5000/getIntroduction"
          :page="3"
          style="display: inline-block; width: 100%"
        ></pdf>
      </a-col>
      <a-col :span="6">
        <pdf
          src="http://127.0.0.1:5000/getIntroduction"
          :page="4"
          style="display: inline-block; width: 100%"
        ></pdf>
      </a-col>
    </a-row>
    <p style="font-weight: 500; color: #0d1a26; font-size: 24px">
      Workflow for slice-level detection
    </p>
    <a-divider></a-divider>
    <p>comming soon ...</p>
    <p style="font-weight: 500; color: #0d1a26; font-size: 24px">
      Workflow for lesion segmentation
    </p>
    <a-divider></a-divider>
    <p>comming soon ...</p>
  </div>
</template>
<script>
import pdf from "vue-pdf";
export default {
  components: {
    pdf,
  },
  data() {
    return {};
  },
};
</script>
