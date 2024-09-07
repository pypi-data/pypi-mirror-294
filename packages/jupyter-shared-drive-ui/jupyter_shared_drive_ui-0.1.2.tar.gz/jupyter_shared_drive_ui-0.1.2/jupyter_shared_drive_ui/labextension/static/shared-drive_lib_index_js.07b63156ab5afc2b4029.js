"use strict";
(self["webpackChunk_jupyter_shared_drive_extension"] = self["webpackChunk_jupyter_shared_drive_extension"] || []).push([["shared-drive_lib_index_js"],{

/***/ "../shared-drive/lib/components.js":
/*!*****************************************!*\
  !*** ../shared-drive/lib/components.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   UserIconComponent: () => (/* binding */ UserIconComponent)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * React component for the user icon.
 *
 * @returns The React component
 */
const UserIconComponent = props => {
    const { user } = props;
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "jp-UserInfo-Container" },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { title: user.display_name, className: "jp-UserInfo-Icon", style: { backgroundColor: user.color } },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, user.initials)),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("h3", null, user.display_name)));
};


/***/ }),

/***/ "../shared-drive/lib/cursors.js":
/*!**************************************!*\
  !*** ../shared-drive/lib/cursors.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   remoteUserCursors: () => (/* binding */ remoteUserCursors)
/* harmony export */ });
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @codemirror/view */ "webpack/sharing/consume/default/@codemirror/view");
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_codemirror_view__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Facet storing the Yjs document objects
 */
const editorAwarenessFacet = _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.Facet.define({
    combine(configs) {
        return configs[configs.length - 1];
    }
});
/**
 * Remote selection theme
 */
const remoteSelectionTheme = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.EditorView.baseTheme({
    '.jp-remote-cursor': {
        borderLeft: '1px solid black',
        marginLeft: '-1px'
    },
    '.jp-remote-cursor.jp-mod-primary': {
        borderLeftWidth: '2px'
    },
    '.jp-remote-selection': {
        opacity: 0.5
    },
    '.cm-tooltip': {
        border: 'none'
    },
    '.cm-tooltip .jp-remote-userInfo': {
        color: 'var(--jp-ui-inverse-font-color0)',
        padding: '0px 2px'
    }
});
// TODO fix which user needs update
const remoteSelectionsAnnotation = _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.Annotation.define();
/**
 * Wrapper around RectangleMarker to be able to set the user color for the remote cursor and selection ranges.
 */
class RemoteMarker {
    /**
     * Constructor
     *
     * @param style Specific user style to be applied on the marker element
     * @param marker {@link RectangleMarker} to wrap
     */
    constructor(style, marker) {
        this.style = style;
        this.marker = marker;
    }
    draw() {
        const elt = this.marker.draw();
        for (const [key, value] of Object.entries(this.style)) {
            // @ts-expect-error Unknown key
            elt.style[key] = value;
        }
        return elt;
    }
    eq(other) {
        return (this.marker.eq(other.marker) && _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(this.style, other.style));
    }
    update(dom, oldMarker) {
        for (const [key, value] of Object.entries(this.style)) {
            // @ts-expect-error Unknown key
            dom.style[key] = value;
        }
        return this.marker.update(dom, oldMarker.marker);
    }
}
/**
 * Extension defining a new editor layer storing the remote user cursors
 */
const remoteCursorsLayer = (0,_codemirror_view__WEBPACK_IMPORTED_MODULE_1__.layer)({
    above: true,
    markers(view) {
        const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
        const ydoc = ytext.doc;
        const cursors = [];
        awareness.getStates().forEach((state, clientID) => {
            var _a, _b, _c;
            if (clientID === awareness.doc.clientID) {
                return;
            }
            const cursors_ = state.cursors;
            for (const cursor of cursors_ !== null && cursors_ !== void 0 ? cursors_ : []) {
                if (!(cursor === null || cursor === void 0 ? void 0 : cursor.anchor) || !(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                    return;
                }
                const anchor = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createAbsolutePositionFromRelativePosition)(cursor.anchor, ydoc);
                const head = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createAbsolutePositionFromRelativePosition)(cursor.head, ydoc);
                if ((anchor === null || anchor === void 0 ? void 0 : anchor.type) !== ytext || (head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                    return;
                }
                const className = ((_a = cursor.primary) !== null && _a !== void 0 ? _a : true)
                    ? 'jp-remote-cursor jp-mod-primary'
                    : 'jp-remote-cursor';
                const cursor_ = _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.EditorSelection.cursor(head.index, head.index > anchor.index ? -1 : 1);
                for (const piece of _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.RectangleMarker.forRange(view, className, cursor_)) {
                    // Wrap the rectangle marker to set the user color
                    cursors.push(new RemoteMarker({ borderLeftColor: (_c = (_b = state.user) === null || _b === void 0 ? void 0 : _b.color) !== null && _c !== void 0 ? _c : 'black' }, piece));
                }
            }
        });
        return cursors;
    },
    update(update, layer) {
        return !!update.transactions.find(t => t.annotation(remoteSelectionsAnnotation));
    },
    class: 'jp-remote-cursors'
});
/**
 * Tooltip extension to display user display name at cursor position
 */
const userHover = (0,_codemirror_view__WEBPACK_IMPORTED_MODULE_1__.hoverTooltip)((view, pos) => {
    var _a;
    const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
    const ydoc = ytext.doc;
    for (const [clientID, state] of awareness.getStates()) {
        if (clientID === awareness.doc.clientID) {
            continue;
        }
        for (const cursor of (_a = state.cursors) !== null && _a !== void 0 ? _a : []) {
            if (!(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                continue;
            }
            const head = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createAbsolutePositionFromRelativePosition)(cursor.head, ydoc);
            if ((head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                continue;
            }
            // Use some margin around the cursor to display the user.
            if (head.index - 3 <= pos && pos <= head.index + 3) {
                return {
                    pos: head.index,
                    above: true,
                    create: () => {
                        var _a, _b, _c, _d;
                        const dom = document.createElement('div');
                        dom.classList.add('jp-remote-userInfo');
                        dom.style.backgroundColor = (_b = (_a = state.user) === null || _a === void 0 ? void 0 : _a.color) !== null && _b !== void 0 ? _b : 'darkgrey';
                        dom.textContent =
                            (_d = (_c = state.user) === null || _c === void 0 ? void 0 : _c.display_name) !== null && _d !== void 0 ? _d : 'Anonymous';
                        return { dom };
                    }
                };
            }
        }
    }
    return null;
}, {
    hideOn: (tr, tooltip) => !!tr.annotation(remoteSelectionsAnnotation),
    hoverTime: 0
});
/**
 * Extension defining a new editor layer storing the remote selections
 */
const remoteSelectionLayer = (0,_codemirror_view__WEBPACK_IMPORTED_MODULE_1__.layer)({
    above: false,
    markers(view) {
        const { awareness, ytext } = view.state.facet(editorAwarenessFacet);
        const ydoc = ytext.doc;
        const cursors = [];
        awareness.getStates().forEach((state, clientID) => {
            var _a, _b, _c;
            if (clientID === awareness.doc.clientID) {
                return;
            }
            const cursors_ = state.cursors;
            for (const cursor of cursors_ !== null && cursors_ !== void 0 ? cursors_ : []) {
                if (((_a = cursor.empty) !== null && _a !== void 0 ? _a : true) || !(cursor === null || cursor === void 0 ? void 0 : cursor.anchor) || !(cursor === null || cursor === void 0 ? void 0 : cursor.head)) {
                    return;
                }
                const anchor = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createAbsolutePositionFromRelativePosition)(cursor.anchor, ydoc);
                const head = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createAbsolutePositionFromRelativePosition)(cursor.head, ydoc);
                if ((anchor === null || anchor === void 0 ? void 0 : anchor.type) !== ytext || (head === null || head === void 0 ? void 0 : head.type) !== ytext) {
                    return;
                }
                const className = 'jp-remote-selection';
                for (const piece of _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.RectangleMarker.forRange(view, className, _codemirror_state__WEBPACK_IMPORTED_MODULE_0__.EditorSelection.range(anchor.index, head.index))) {
                    // Wrap the rectangle marker to set the user color
                    cursors.push(new RemoteMarker({ backgroundColor: (_c = (_b = state.user) === null || _b === void 0 ? void 0 : _b.color) !== null && _c !== void 0 ? _c : 'black' }, piece));
                }
            }
        });
        return cursors;
    },
    update(update, layer) {
        return !!update.transactions.find(t => t.annotation(remoteSelectionsAnnotation));
    },
    class: 'jp-remote-selections'
});
/**
 * CodeMirror extension exchanging and displaying remote user selection ranges (including cursors)
 */
const showCollaborators = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.ViewPlugin.fromClass(class {
    constructor(view) {
        this.editorAwareness = view.state.facet(editorAwarenessFacet);
        this._listener = ({ added, updated, removed }) => {
            const clients = added.concat(updated).concat(removed);
            if (clients.findIndex(id => id !== this.editorAwareness.awareness.doc.clientID) >= 0) {
                // Trick to get the remoteCursorLayers to be updated
                view.dispatch({ annotations: [remoteSelectionsAnnotation.of([])] });
            }
        };
        this.editorAwareness.awareness.on('change', this._listener);
    }
    destroy() {
        this.editorAwareness.awareness.off('change', this._listener);
    }
    /**
     * Communicate the current user cursor position to all remotes
     */
    update(update) {
        var _a;
        if (!update.docChanged && !update.selectionSet) {
            return;
        }
        const { awareness, ytext } = this.editorAwareness;
        const localAwarenessState = awareness.getLocalState();
        // set local awareness state (update cursors)
        if (localAwarenessState) {
            const hasFocus = update.view.hasFocus && update.view.dom.ownerDocument.hasFocus();
            const selection = update.state.selection;
            const cursors = new Array();
            if (hasFocus && selection) {
                for (const r of selection.ranges) {
                    const primary = r === selection.main;
                    const anchor = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createRelativePositionFromTypeIndex)(ytext, r.anchor);
                    const head = (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createRelativePositionFromTypeIndex)(ytext, r.head);
                    cursors.push({
                        anchor,
                        head,
                        primary,
                        empty: r.empty
                    });
                }
                if (!localAwarenessState.cursors || cursors.length > 0) {
                    const oldCursors = (_a = localAwarenessState.cursors) === null || _a === void 0 ? void 0 : _a.map(cursor => {
                        return {
                            ...cursor,
                            anchor: (cursor === null || cursor === void 0 ? void 0 : cursor.anchor)
                                ? (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createRelativePositionFromJSON)(cursor.anchor)
                                : null,
                            head: (cursor === null || cursor === void 0 ? void 0 : cursor.head)
                                ? (0,yjs__WEBPACK_IMPORTED_MODULE_3__.createRelativePositionFromJSON)(cursor.head)
                                : null
                        };
                    });
                    if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(cursors, oldCursors)) {
                        // Update cursors
                        awareness.setLocalStateField('cursors', cursors);
                    }
                }
            }
        }
    }
}, {
    provide: () => {
        return [
            remoteSelectionTheme,
            remoteCursorsLayer,
            remoteSelectionLayer,
            userHover,
            // As we use relative positioning of widget, the tooltip must be positioned absolutely
            // And we attach the tooltip to the body to avoid overflow rules
            (0,_codemirror_view__WEBPACK_IMPORTED_MODULE_1__.tooltips)({ position: 'absolute', parent: document.body })
        ];
    }
});
/**
 * CodeMirror extension to display remote users cursors
 *
 * @param config Editor source and awareness
 * @returns CodeMirror extension
 */
function remoteUserCursors(config) {
    return [editorAwarenessFacet.of(config), showCollaborators];
}


/***/ }),

/***/ "../shared-drive/lib/index.js":
/*!************************************!*\
  !*** ../shared-drive/lib/index.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IGlobalAwareness: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IGlobalAwareness),
/* harmony export */   IUserMenu: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IUserMenu),
/* harmony export */   RendererUserMenu: () => (/* reexport safe */ _menu__WEBPACK_IMPORTED_MODULE_2__.RendererUserMenu),
/* harmony export */   UserInfoBody: () => (/* reexport safe */ _userinfopanel__WEBPACK_IMPORTED_MODULE_3__.UserInfoBody),
/* harmony export */   UserInfoPanel: () => (/* reexport safe */ _userinfopanel__WEBPACK_IMPORTED_MODULE_3__.UserInfoPanel),
/* harmony export */   UserMenu: () => (/* reexport safe */ _menu__WEBPACK_IMPORTED_MODULE_2__.UserMenu),
/* harmony export */   remoteUserCursors: () => (/* reexport safe */ _cursors__WEBPACK_IMPORTED_MODULE_1__.remoteUserCursors)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../shared-drive/lib/tokens.js");
/* harmony import */ var _cursors__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./cursors */ "../shared-drive/lib/cursors.js");
/* harmony import */ var _menu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./menu */ "../shared-drive/lib/menu.js");
/* harmony import */ var _userinfopanel__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./userinfopanel */ "../shared-drive/lib/userinfopanel.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module shared-drive
 */






/***/ }),

/***/ "../shared-drive/lib/menu.js":
/*!***********************************!*\
  !*** ../shared-drive/lib/menu.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   RendererUserMenu: () => (/* binding */ RendererUserMenu),
/* harmony export */   UserMenu: () => (/* binding */ UserMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/virtualdom */ "webpack/sharing/consume/default/@lumino/virtualdom");
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Custom renderer for the user menu.
 */
class RendererUserMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.MenuBar.Renderer {
    /**
     * Constructor of the class RendererUserMenu.
     *
     * @argument user Current user object.
     */
    constructor(user) {
        super();
        this._user = user;
    }
    /**
     * Render the virtual element for a menu bar item.
     *
     * @param data - The data to use for rendering the item.
     *
     * @returns A virtual element representing the item.
     */
    renderItem(data) {
        const className = this.createItemClass(data);
        const dataset = this.createItemDataset(data);
        const aria = this.createItemARIA(data);
        return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.li({ className, dataset, tabindex: '0', onfocus: data.onfocus, ...aria }, this._createUserIcon(), this.renderLabel(data), this.renderIcon(data));
    }
    /**
     * Render the label element for a menu item.
     *
     * @param data - The data to use for rendering the label.
     *
     * @returns A virtual element representing the item label.
     */
    renderLabel(data) {
        const content = this.formatLabel(data);
        return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.div({ className: 'lm-MenuBar-itemLabel jp-MenuBar-label' }, content);
    }
    /**
     * Render the user icon element for a menu item.
     *
     * @returns A virtual element representing the item label.
     */
    _createUserIcon() {
        if (this._user.isReady && this._user.identity.avatar_url) {
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.div({
                className: 'lm-MenuBar-itemIcon jp-MenuBar-imageIcon'
            }, _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.img({ src: this._user.identity.avatar_url }));
        }
        else if (this._user.isReady) {
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.div({
                className: 'lm-MenuBar-itemIcon jp-MenuBar-anonymousIcon',
                style: { backgroundColor: this._user.identity.color }
            }, _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.span({}, this._user.identity.initials));
        }
        else {
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_2__.h.div({
                className: 'lm-MenuBar-itemIcon jp-MenuBar-anonymousIcon'
            }, _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.userIcon);
        }
    }
}
/**
 * This menu does not contain anything but we keep it around in case someone uses it.
 * Custom lumino Menu for the user menu.
 */
class UserMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Menu {
    constructor(options) {
        super(options);
    }
}


/***/ }),

/***/ "../shared-drive/lib/tokens.js":
/*!*************************************!*\
  !*** ../shared-drive/lib/tokens.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IGlobalAwareness: () => (/* binding */ IGlobalAwareness),
/* harmony export */   IUserMenu: () => (/* binding */ IUserMenu)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The user menu token.
 *
 * NOTE: Require this token in your extension to access the user menu
 * (top-right menu in JupyterLab's interface).
 */
const IUserMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyter/collaboration:IUserMenu');
/**
 * The global awareness token.
 */
const IGlobalAwareness = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyter/collaboration:IGlobalAwareness');


/***/ }),

/***/ "../shared-drive/lib/userinfopanel.js":
/*!********************************************!*\
  !*** ../shared-drive/lib/userinfopanel.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   UserInfoBody: () => (/* binding */ UserInfoBody),
/* harmony export */   UserInfoPanel: () => (/* binding */ UserInfoPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./components */ "../shared-drive/lib/components.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




class UserInfoPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Panel {
    constructor(user) {
        super({});
        this.addClass('jp-UserInfoPanel');
        this._profile = user;
        this._body = null;
        if (this._profile.isReady) {
            this._body = new UserInfoBody(this._profile.identity);
            this.addWidget(this._body);
            this.update();
        }
        else {
            this._profile.ready
                .then(() => {
                this._body = new UserInfoBody(this._profile.identity);
                this.addWidget(this._body);
                this.update();
            })
                .catch(e => console.error(e));
        }
    }
}
/**
 * A SettingsWidget for the user.
 */
class UserInfoBody extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /**
     * Constructs a new settings widget.
     */
    constructor(user) {
        super();
        this._user = user;
    }
    get user() {
        return this._user;
    }
    set user(user) {
        this._user = user;
        this.update();
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_2__.createElement(_components__WEBPACK_IMPORTED_MODULE_3__.UserIconComponent, { user: this._user });
    }
}


/***/ })

}]);
//# sourceMappingURL=shared-drive_lib_index_js.07b63156ab5afc2b4029.js.map