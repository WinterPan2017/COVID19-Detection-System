"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports["default"] = exports.defaultRenderLogoAntTitle = exports.defaultRenderLogo = exports.SiderMenuProps = void 0;

require("./index.less");

var _vueTypes = _interopRequireDefault(require("ant-design-vue/es/_util/vue-types"));

require("ant-design-vue/es/layout/style");

var _layout = _interopRequireDefault(require("ant-design-vue/es/layout"));

var _util = require("../../utils/util");

var _RouteMenu = _interopRequireDefault(require("../RouteMenu"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }

var Sider = _layout["default"].Sider;
var SiderMenuProps = {
  i18nRender: _vueTypes["default"].oneOfType([_vueTypes["default"].func, _vueTypes["default"].bool]).def(false),
  mode: _vueTypes["default"].string.def('inline'),
  theme: _vueTypes["default"].string.def('dark'),
  contentWidth: _vueTypes["default"].oneOf(['Fluid', 'Fixed']).def('Fluid'),
  collapsible: _vueTypes["default"].bool,
  collapsed: _vueTypes["default"].bool,
  handleCollapse: _vueTypes["default"].func,
  menus: _vueTypes["default"].array,
  siderWidth: _vueTypes["default"].number.def(256),
  isMobile: _vueTypes["default"].bool,
  layout: _vueTypes["default"].string.def('inline'),
  fixSiderbar: _vueTypes["default"].bool,
  logo: _vueTypes["default"].any,
  title: _vueTypes["default"].string.def(''),
  // render function or vnode
  menuHeaderRender: _vueTypes["default"].oneOfType([_vueTypes["default"].func, _vueTypes["default"].array, _vueTypes["default"].object, _vueTypes["default"].bool]),
  menuRender: _vueTypes["default"].oneOfType([_vueTypes["default"].func, _vueTypes["default"].array, _vueTypes["default"].object, _vueTypes["default"].bool])
};
exports.SiderMenuProps = SiderMenuProps;

var defaultRenderLogo = function defaultRenderLogo(h, logo) {
  if (typeof logo === 'string') {
    return h("img", {
      attrs: {
        src: logo,
        alt: "logo"
      }
    });
  }

  if (typeof logo === 'function') {
    return logo();
  }

  return h(logo);
};

exports.defaultRenderLogo = defaultRenderLogo;

var defaultRenderLogoAntTitle = function defaultRenderLogoAntTitle(h, props) {
  var _props$logo = props.logo,
      logo = _props$logo === void 0 ? 'https://gw.alipayobjects.com/zos/antfincdn/PmY%24TNNDBI/logo.svg' : _props$logo,
      title = props.title,
      menuHeaderRender = props.menuHeaderRender;

  if (menuHeaderRender === false) {
    return null;
  }

  var logoDom = defaultRenderLogo(h, logo);
  var titleDom = h("h1", [title]);

  if (menuHeaderRender) {
    return (0, _util.isFun)(menuHeaderRender) && menuHeaderRender(h, logoDom, props.collapsed ? null : titleDom, props) || menuHeaderRender;
  }

  return h("span", [logoDom, titleDom]);
};

exports.defaultRenderLogoAntTitle = defaultRenderLogoAntTitle;
var SiderMenu = {
  name: 'SiderMenu',
  model: {
    prop: 'collapsed',
    event: 'collapse'
  },
  props: SiderMenuProps,
  render: function render(h) {
    var collapsible = this.collapsible,
        collapsed = this.collapsed,
        siderWidth = this.siderWidth,
        fixSiderbar = this.fixSiderbar,
        mode = this.mode,
        theme = this.theme,
        menus = this.menus,
        logo = this.logo,
        title = this.title,
        _this$onMenuHeaderCli = this.onMenuHeaderClick,
        onMenuHeaderClick = _this$onMenuHeaderCli === void 0 ? function () {
      return null;
    } : _this$onMenuHeaderCli,
        i18nRender = this.i18nRender,
        menuHeaderRender = this.menuHeaderRender,
        menuRender = this.menuRender;
    var siderCls = ['ant-pro-sider-menu-sider'];
    if (fixSiderbar) siderCls.push('fix-sider-bar');
    if (theme === 'light') siderCls.push('light'); //
    // const handleCollapse = (collapsed, type) => {
    //   this.$emit('collapse', collapsed)
    // }

    var headerDom = defaultRenderLogoAntTitle(h, {
      logo: logo,
      title: title,
      menuHeaderRender: menuHeaderRender,
      collapsed: collapsed
    });
    return h(Sider, {
      "class": siderCls,
      attrs: {
        breakpoint: 'lg',
        trigger: null,
        width: siderWidth,
        theme: theme,
        collapsible: collapsible,
        collapsed: collapsed
      }
    }, [headerDom && h("div", {
      "class": "ant-pro-sider-menu-logo",
      on: {
        "click": onMenuHeaderClick
      },
      attrs: {
        id: "logo"
      }
    }, [h("router-link", {
      attrs: {
        to: {
          path: '/'
        }
      }
    }, [headerDom])]), menuRender && ((0, _util.isFun)(menuRender) && menuRender(h, this.$props) || menuRender) || h(_RouteMenu["default"], {
      attrs: {
        collapsed: collapsed,
        menus: menus,
        mode: mode,
        theme: theme,
        i18nRender: i18nRender
      }
    })]);
  }
};
var _default = SiderMenu;
exports["default"] = _default;