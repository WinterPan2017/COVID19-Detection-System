<template>
  <div id="userLayout" :class="['user-layout-wrapper']">
    <div class="container">
      <div class="user-layout-lang">
        <div class="select-lang-trigger" />
      </div>
      <div class="user-layout-content">
        <div class="top">
          <div class="header">
            <a>
              <img
                src="~@/assets/logo.png"
                class="logo"
                alt="logo"
                style="height: 90px"
              />
              <span class="title">COVID-19 医学影像辅助诊断系统</span>
            </a>
          </div>
          <div class="desc">基于深度学习的新型冠状病毒医学影像辅助诊断系统</div>
        </div>

        <div class="main">
          <a-form
            id="formLogin"
            class="user-layout-login"
            ref="formLogin"
            :form="form"
            @submit="handleSubmit"
          >
            <a-tabs
              :activeKey="customActiveKey"
              :tabBarStyle="{ textAlign: 'center', borderBottom: 'unset' }"
            >
              <a-tab-pane key="tab1" tab="credentials">
                <a-alert
                  v-if="isLoginError"
                  type="error"
                  showIcon
                  style="margin-bottom: 24px"
                  message="user.login.message-invalid-credentials"
                />
                <a-form-item>
                  <a-input
                    size="large"
                    type="text"
                    placeholder="帐号: admin"
                    v-decorator="['username']"
                  >
                    <a-icon
                      slot="prefix"
                      type="user"
                      :style="{ color: 'rgba(0,0,0,.25)' }"
                    />
                  </a-input>
                </a-form-item>

                <a-form-item>
                  <a-input-password
                    size="large"
                    placeholder="密码: admin"
                    v-decorator="['password']"
                  >
                    <a-icon
                      slot="prefix"
                      type="lock"
                      :style="{ color: 'rgba(0,0,0,.25)' }"
                    />
                  </a-input-password>
                </a-form-item>
              </a-tab-pane>
            </a-tabs>

            <a-form-item style="margin-top: 24px">
              <a-button
                size="large"
                type="primary"
                htmlType="submit"
                class="login-button"
                :loading="state.loginBtn"
                :disabled="state.loginBtn"
              >
                登录
              </a-button>
            </a-form-item>
          </a-form>
        </div>
        <div class="footer">
          <div class="links">
            <a href="_self">帮助</a>
            <a href="_self">隐私</a>
            <a href="_self">条款</a>
          </div>
          <div class="copyright">Copyright &copy; 2021 Winter</div>
        </div>
      </div>
    </div>
    <a-modal
      title="提示"
      :visible="visible"
      @ok="modalhandle"
      @cancel="modalhandle"
    >
      <p>{{ ModalText }}</p>
    </a-modal>
  </div>
</template>

<script>
import reqwest from "reqwest";
import { setCookie, getCookie } from "../utils/cookie.js";
export default {
  // components: {
  //   TwoStepCaptcha
  // },
  data() {
    return {
      customActiveKey: "tab1",
      loginBtn: false,
      // login type: 0 email, 1 username, 2 telephone
      loginType: 0,
      isLoginError: false,
      requiredTwoStepCaptcha: false,
      stepCaptchaVisible: false,
      form: this.$form.createForm(this),
      state: {
        time: 60,
        loginBtn: false,
        // login type: 0 email, 1 username, 2 telephone
        loginType: 0,
        smsSendBtn: false,
      },
      //弹窗
      ModalText: "分析完成, 是否前往分析记录页面查看",
      visible: false,
    };
  },
  created() {
    let _token = getCookie("token");
    console.log("login token", _token);
    if (_token !== undefined && _token !== "") {
      this.$router.replace("/Home/introduction");
    }
    // reqwest({
    //   url: "http://127.0.0.1:5000/login",
    //   method: "post",
    //   headers: {
    //     token: _token,
    //   },
    //   data: { username: "123", password: "456" },
    //   success: (e) => {
    //     console.log("sucess login, token", e);
    //     setCookie("token", e.token, 120);
    //   },
    //   error: () => {
    //     console.log("login failed");
    //   },
    // });
  },
  methods: {
    handleSubmit() {
      this.form.validateFields((err, values) => {
        console.log(values.username, values.password);
        if (values.username == undefined || values.password == null) {
          this.ModalText = "请填写完整的帐号和密码";
          this.visible = true;
          return;
        }
        console.log(err, values);
        // if (!err) {
        //   console.log("Received values of form: ", values);
        //   if (values.username == "admin" && values.password == "123456")
        //     this.$router.replace("/Home/introduction");
        // }
        let _token = getCookie("token");
        reqwest({
          url: "http://127.0.0.1:5000/login",
          method: "post",
          headers: {
            token: _token,
          },
          data: { username: values.username, password: values.password },
          success: (e) => {
            console.log("sucess login, token", e);
            setCookie("token", e.token, 120);
            // this.$router.replace("/Home/introduction");
            this.$router.push({
              name: "Introduction",
              params: {
                username: values.username,
              },
            });
          },
          error: () => {
            console.log("login failed");
            this.ModalText = "帐号或密码不正确,登录失败";
            this.visible = true;
          },
        });
      });
      // this.$router.replace("/Home");
    },
    modalhandle() {
      this.ModalText = "请填写完整的帐号和密码";
      this.visible = false;
    },
    stepCaptchaSuccess() {},
    stepCaptchaCancel() {},
  },
  mounted() {
    document.body.classList.add("userLayout");
  },
  beforeDestroy() {
    document.body.classList.remove("userLayout");
  },
};
</script>

<style lang="less" scoped>
.user-layout-login {
  label {
    font-size: 14px;
  }

  .getCaptcha {
    display: block;
    width: 100%;
    height: 40px;
  }

  .forge-password {
    font-size: 14px;
  }

  button.login-button {
    padding: 0 15px;
    font-size: 16px;
    height: 40px;
    width: 100%;
  }

  .user-login-other {
    text-align: left;
    margin-top: 24px;
    line-height: 22px;

    .item-icon {
      font-size: 24px;
      color: rgba(0, 0, 0, 0.2);
      margin-left: 16px;
      vertical-align: middle;
      cursor: pointer;
      transition: color 0.3s;

      &:hover {
        color: #1890ff;
      }
    }

    .register {
      float: right;
    }
  }
}
#userLayout.user-layout-wrapper {
  height: 100%;

  .container {
    width: 100%;
    min-height: 100%;
    background: #f0f2f5 url(~@/assets/background.svg) no-repeat 50%;
    background-size: 100%;
    //padding: 50px 0 84px;
    position: relative;

    .user-layout-lang {
      width: 100%;
      height: 40px;
      line-height: 44px;
      text-align: right;

      .select-lang-trigger {
        cursor: pointer;
        padding: 12px;
        margin-right: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        vertical-align: middle;
      }
    }

    .user-layout-content {
      padding: 32px 0 24px;

      .top {
        text-align: center;

        .header {
          height: 44px;
          line-height: 44px;

          .badge {
            position: absolute;
            display: inline-block;
            line-height: 1;
            vertical-align: middle;
            margin-left: -12px;
            margin-top: -10px;
            opacity: 0.8;
          }

          .logo {
            height: 44px;
            vertical-align: top;
            margin-right: 16px;
            border-style: none;
          }

          .title {
            font-size: 33px;
            color: rgba(0, 0, 0, 0.85);
            font-family: Avenir, "Helvetica Neue", Arial, Helvetica, sans-serif;
            font-weight: 600;
            position: relative;
            top: 2px;
          }
        }
        .desc {
          font-size: 14px;
          color: rgba(0, 0, 0, 0.45);
          margin-top: 12px;
          margin-bottom: 40px;
        }
      }

      .main {
        min-width: 260px;
        width: 368px;
        margin: 0 auto;
      }

      .footer {
        // position: absolute;
        width: 100%;
        bottom: 0;
        padding: 0 16px;
        margin: 48px 0 24px;
        text-align: center;

        .links {
          margin-bottom: 8px;
          font-size: 14px;
          a {
            color: rgba(0, 0, 0, 0.45);
            transition: all 0.3s;
            &:not(:last-child) {
              margin-right: 40px;
            }
          }
        }
        .copyright {
          color: rgba(0, 0, 0, 0.45);
          font-size: 14px;
        }
      }
    }

    a {
      text-decoration: none;
    }
  }
}
</style>
