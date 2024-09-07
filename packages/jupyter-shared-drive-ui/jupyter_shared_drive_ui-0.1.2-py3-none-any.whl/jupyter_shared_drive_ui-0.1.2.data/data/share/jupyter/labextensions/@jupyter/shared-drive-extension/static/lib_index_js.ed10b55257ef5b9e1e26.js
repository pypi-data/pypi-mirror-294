"use strict";
(self["webpackChunk_jupyter_shared_drive_extension"] = self["webpackChunk_jupyter_shared_drive_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/collaboration.js":
/*!******************************!*\
  !*** ./lib/collaboration.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   menuBarPlugin: () => (/* binding */ menuBarPlugin),
/* harmony export */   rtcGlobalAwarenessPlugin: () => (/* binding */ rtcGlobalAwarenessPlugin),
/* harmony export */   userEditorCursors: () => (/* binding */ userEditorCursors),
/* harmony export */   userMenuPlugin: () => (/* binding */ userMenuPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyter/shared-drive */ "webpack/sharing/consume/default/@jupyter/shared-drive/@jupyter/shared-drive");
/* harmony import */ var _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var y_protocols_awareness__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! y-protocols/awareness */ "../../node_modules/y-protocols/awareness.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module shared-drive-extension
 */


//import { WebrtcAwarenessProvider } from '@jupyter/docprovider';
//import { URLExt } from '@jupyterlab/coreutils';
//import { ServerConnection } from '@jupyterlab/services';

//import { ITranslator, nullTranslator } from '@jupyterlab/translation';




/**
 * Jupyter plugin providing the IUserMenu.
 */
const userMenuPlugin = {
    id: '@jupyter/shared-drive-extension:userMenu',
    description: 'Provide connected user menu.',
    requires: [],
    provides: _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.IUserMenu,
    activate: (app) => {
        const { commands } = app;
        const { user } = app.serviceManager;
        return new _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.UserMenu({ commands, user });
    }
};
/**
 * Jupyter plugin adding the IUserMenu to the menu bar if collaborative flag enabled.
 */
const menuBarPlugin = {
    id: '@jupyter/shared-drive-extension:user-menu-bar',
    description: 'Add user menu to the interface.',
    autoStart: true,
    requires: [_jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.IUserMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IToolbarWidgetRegistry],
    activate: async (app, menu, toolbarRegistry) => {
        const { user } = app.serviceManager;
        const menuBar = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.MenuBar({
            forceItemsPosition: {
                forceX: false,
                forceY: false
            },
            renderer: new _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.RendererUserMenu(user)
        });
        menuBar.id = 'jp-UserMenu';
        user.userChanged.connect(() => menuBar.update());
        menuBar.addMenu(menu);
        toolbarRegistry.addFactory('TopBar', 'user-menu', () => menuBar);
    }
};
/**
 * Jupyter plugin creating a global awareness for RTC.
 */
const rtcGlobalAwarenessPlugin = {
    id: '@jupyter/shared-drive-extension:rtcGlobalAwareness',
    description: 'Add global awareness to share working document of users.',
    requires: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_2__.IStateDB],
    provides: _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.IGlobalAwareness,
    activate: (app, state) => {
        var _a;
        const { user } = app.serviceManager;
        const ydoc = new yjs__WEBPACK_IMPORTED_MODULE_5__.Doc();
        const awareness = new y_protocols_awareness__WEBPACK_IMPORTED_MODULE_6__.Awareness(ydoc);
        awareness.setLocalState({ username: (_a = user.identity) === null || _a === void 0 ? void 0 : _a.name, contents: [] });
        //const server = ServerConnection.makeSettings();
        //const url = URLExt.join(server.wsUrl, 'api/collaboration/room');
        //new WebrtcAwarenessProvider({
        //  url: url,
        //  roomID: 'JupyterLab:globalAwareness',
        //  awareness: awareness,
        //  user: user
        //});
        //state.changed.connect(async () => {
        //  const data: any = await state.toJSON();
        //  const current: string = data['layout-restorer:data']?.main?.current || '';
        //  if (current.match(/^\w+:RTC:/)) {
        //    awareness.setLocalStateField('current', current);
        //  } else {
        //    awareness.setLocalStateField('current', null);
        //  }
        //});
        return awareness;
    }
};
const userEditorCursors = {
    id: '@jupyter/share-drive-extension:userEditorCursors',
    description: 'Add CodeMirror extension to display remote user cursors and selections.',
    autoStart: true,
    requires: [_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__.IEditorExtensionRegistry],
    activate: (app, extensions) => {
        extensions.addExtension({
            name: 'remote-user-cursors',
            factory(options) {
                const { awareness, ysource: ytext } = options.model.sharedModel;
                return _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__.EditorExtensionRegistry.createImmutableExtension((0,_jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_4__.remoteUserCursors)({ awareness, ytext }));
            }
        });
    }
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _collaboration__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./collaboration */ "./lib/collaboration.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module shared-drive-extension
 */

/**
 * Export the plugins as default.
 */
const plugins = [
    _collaboration__WEBPACK_IMPORTED_MODULE_0__.userMenuPlugin,
    _collaboration__WEBPACK_IMPORTED_MODULE_0__.menuBarPlugin,
    _collaboration__WEBPACK_IMPORTED_MODULE_0__.rtcGlobalAwarenessPlugin,
    _collaboration__WEBPACK_IMPORTED_MODULE_0__.userEditorCursors
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.ed10b55257ef5b9e1e26.js.map