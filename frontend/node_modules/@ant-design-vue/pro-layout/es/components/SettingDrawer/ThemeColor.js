import _mergeJSXProps from "babel-helper-vue-jsx-merge-props";

function _objectWithoutProperties(source, excluded) { if (source == null) return {}; var target = _objectWithoutPropertiesLoose(source, excluded); var key, i; if (Object.getOwnPropertySymbols) { var sourceSymbolKeys = Object.getOwnPropertySymbols(source); for (i = 0; i < sourceSymbolKeys.length; i++) { key = sourceSymbolKeys[i]; if (excluded.indexOf(key) >= 0) continue; if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue; target[key] = source[key]; } } return target; }

function _objectWithoutPropertiesLoose(source, excluded) { if (source == null) return {}; var target = {}; var sourceKeys = Object.keys(source); var key, i; for (i = 0; i < sourceKeys.length; i++) { key = sourceKeys[i]; if (excluded.indexOf(key) >= 0) continue; target[key] = source[key]; } return target; }

import './ThemeColor.less';
import PropTypes from 'ant-design-vue/es/_util/vue-types';
import { genThemeToString } from '../../utils/util';
import 'ant-design-vue/es/tooltip/style';
import Tooltip from 'ant-design-vue/es/tooltip';
import 'ant-design-vue/es/icon/style';
import Icon from 'ant-design-vue/es/icon';
var baseClassName = 'theme-color';
export var TagProps = {
  color: PropTypes.string,
  check: PropTypes.bool
};
var Tag = {
  props: TagProps,
  functional: true,
  render: function render(h, content) {
    var _content$props = content.props,
        color = _content$props.color,
        check = _content$props.check,
        data = content.data,
        rest = _objectWithoutProperties(content, ["props", "data"]);

    return h("div", _mergeJSXProps([data, {
      style: {
        backgroundColor: color
      }
    }]), [check ? h(Icon, {
      attrs: {
        type: "check"
      }
    }) : null]);
  }
};
export var ThemeColorProps = {
  colors: PropTypes.array,
  title: PropTypes.string,
  value: PropTypes.string,
  i18nRender: PropTypes.oneOfType([PropTypes.func, PropTypes.bool]).def(false)
};
var ThemeColor = {
  props: ThemeColorProps,
  inject: ['locale'],
  render: function render(h) {
    var _this = this;

    var title = this.title,
        value = this.value,
        _this$colors = this.colors,
        colors = _this$colors === void 0 ? [] : _this$colors;
    var i18n = this.$props.i18nRender || this.locale;

    var handleChange = function handleChange(key) {
      _this.$emit('change', key);
    };

    return h("div", {
      "class": baseClassName,
      ref: 'ref'
    }, [h("h3", {
      "class": "".concat(baseClassName, "-title")
    }, [title]), h("div", {
      "class": "".concat(baseClassName, "-content")
    }, [colors.map(function (item) {
      var themeKey = genThemeToString(item.key);
      var check = value === item.key || genThemeToString(value) === item.key;
      return h(Tooltip, {
        key: item.color,
        attrs: {
          title: themeKey ? i18n("app.setting.themecolor.".concat(themeKey)) : item.key
        }
      }, [h(Tag, {
        "class": "".concat(baseClassName, "-block"),
        attrs: {
          color: item.color,
          check: check
        },
        on: {
          "click": function click() {
            return handleChange(item.key);
          }
        }
      })]);
    })])]);
  }
};
export default ThemeColor;