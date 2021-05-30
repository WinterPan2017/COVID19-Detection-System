"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
Object.defineProperty(exports, "RouteMenu", {
  enumerable: true,
  get: function get() {
    return _RouteMenu["default"];
  }
});
Object.defineProperty(exports, "SiderMenuWrapper", {
  enumerable: true,
  get: function get() {
    return _SiderMenu["default"];
  }
});
Object.defineProperty(exports, "SiderMenu", {
  enumerable: true,
  get: function get() {
    return _SiderMenu.SiderMenu;
  }
});
Object.defineProperty(exports, "SiderMenuProps", {
  enumerable: true,
  get: function get() {
    return _SiderMenu.SiderMenuProps;
  }
});
Object.defineProperty(exports, "PageHeaderWrapper", {
  enumerable: true,
  get: function get() {
    return _PageHeaderWrapper["default"];
  }
});
Object.defineProperty(exports, "GlobalFooter", {
  enumerable: true,
  get: function get() {
    return _GlobalFooter["default"];
  }
});
Object.defineProperty(exports, "VueFragment", {
  enumerable: true,
  get: function get() {
    return _Fragment["default"];
  }
});

var _RouteMenu = _interopRequireDefault(require("./RouteMenu"));

var _SiderMenu = _interopRequireWildcard(require("./SiderMenu"));

var _PageHeaderWrapper = _interopRequireDefault(require("./PageHeaderWrapper"));

var _GlobalFooter = _interopRequireDefault(require("./GlobalFooter"));

var _Fragment = _interopRequireDefault(require("./Fragment"));

function _getRequireWildcardCache() { if (typeof WeakMap !== "function") return null; var cache = new WeakMap(); _getRequireWildcardCache = function _getRequireWildcardCache() { return cache; }; return cache; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } if (obj === null || typeof obj !== "object" && typeof obj !== "function") { return { "default": obj }; } var cache = _getRequireWildcardCache(); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj["default"] = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { "default": obj }; }