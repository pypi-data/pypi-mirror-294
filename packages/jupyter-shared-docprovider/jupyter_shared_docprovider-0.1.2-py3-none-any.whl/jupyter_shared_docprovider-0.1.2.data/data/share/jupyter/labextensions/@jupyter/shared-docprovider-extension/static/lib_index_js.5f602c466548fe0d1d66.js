"use strict";
(self["webpackChunk_jupyter_shared_docprovider_extension"] = self["webpackChunk_jupyter_shared_docprovider_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/filebrowser.js":
/*!****************************!*\
  !*** ./lib/filebrowser.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   drive: () => (/* binding */ drive),
/* harmony export */   sharedFileBrowser: () => (/* binding */ sharedFileBrowser),
/* harmony export */   yfile: () => (/* binding */ yfile),
/* harmony export */   ynotebook: () => (/* binding */ ynotebook)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyter/ydoc */ "webpack/sharing/consume/default/@jupyter/ydoc");
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyter/shared-drive */ "webpack/sharing/consume/default/@jupyter/shared-drive");
/* harmony import */ var _jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyter/shared-docprovider */ "webpack/sharing/consume/default/@jupyter/shared-docprovider/@jupyter/shared-docprovider");
/* harmony import */ var _jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

//import { listIcon, fileIcon, refreshIcon } from '@jupyterlab/ui-components';








/**
 * The shared drive provider.
 */
const drive = {
    id: '@jupyter/docprovider-extension:drive',
    description: 'The default collaborative drive provider',
    provides: _jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__.ISharedDrive,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IDefaultFileBrowser, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [_jupyter_shared_drive__WEBPACK_IMPORTED_MODULE_7__.IGlobalAwareness],
    activate: (app, defaultFileBrowser, translator, globalAwareness) => {
        const trans = translator.load('jupyter-shared-drive');
        const drive = new _jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__.SharedDrive(app.serviceManager.user, defaultFileBrowser, trans, globalAwareness, 'Shared');
        return drive;
    }
};
/**
 * Plugin to register the shared model factory for the content type 'file'.
 */
const yfile = {
    id: '@jupyter/docprovider-extension:yfile',
    description: "Plugin to register the shared model factory for the content type 'file'",
    autoStart: true,
    requires: [_jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__.ISharedDrive],
    optional: [],
    activate: (app, drive) => {
        const yFileFactory = () => {
            return new _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_6__.YFile();
        };
        drive.sharedModelFactory.registerDocumentFactory('file', yFileFactory);
    }
};
/**
 * Plugin to register the shared model factory for the content type 'notebook'.
 */
const ynotebook = {
    id: '@jupyter/docprovider-extension:ynotebook',
    description: "Plugin to register the shared model factory for the content type 'notebook'",
    autoStart: true,
    requires: [_jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__.ISharedDrive],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: (app, drive, settingRegistry) => {
        let disableDocumentWideUndoRedo = true;
        // Fetch settings if possible.
        if (settingRegistry) {
            settingRegistry
                .load('@jupyterlab/notebook-extension:tracker')
                .then(settings => {
                const updateSettings = (settings) => {
                    var _a;
                    const enableDocWideUndo = settings === null || settings === void 0 ? void 0 : settings.get('experimentalEnableDocumentWideUndoRedo').composite;
                    disableDocumentWideUndoRedo = (_a = !enableDocWideUndo) !== null && _a !== void 0 ? _a : true;
                };
                updateSettings(settings);
                settings.changed.connect((settings) => updateSettings(settings));
            });
        }
        const yNotebookFactory = () => {
            return new _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_6__.YNotebook({
                disableDocumentWideUndoRedo
            });
        };
        drive.sharedModelFactory.registerDocumentFactory('notebook', yNotebookFactory);
    }
};
/**
 * The shared file browser factory provider.
 */
const sharedFileBrowser = {
    id: 'jupyterlab-shared-contents:sharedFileBrowser',
    description: 'The shared file browser factory provider',
    autoStart: true,
    requires: [_jupyter_shared_docprovider__WEBPACK_IMPORTED_MODULE_8__.ISharedDrive, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.IRouter,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.JupyterFrontEnd.ITreeResolver,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator
    ],
    activate: async (app, drive, fileBrowserFactory, router, tree, labShell, translator) => {
        const { createFileBrowser } = fileBrowserFactory;
        //const trans = (translator ?? nullTranslator).load('jupyterlab-shared-contents');
        app.serviceManager.contents.addDrive(drive);
        const widget = createFileBrowser('jp-shared-contents-browser', {
            driveName: drive.name,
            // We don't want to restore old state, we don't have a drive handle ready
            restore: false
        });
        //widget.title.caption = trans.__('Shared Contents');
        widget.title.caption = 'Shared Contents';
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.listIcon;
        //const importButton = new ToolbarButton({
        //  icon: fileIcon,
        //  onClick: async () => {
        //    let path = prompt('Please enter the path of the file to import:');
        //    if (path !== null) {
        //      await drive.importFile(path);
        //    }
        //  },
        //  tooltip: 'Import File'
        //});
        const refreshButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.refreshIcon,
            onClick: async () => {
                widget.model.refresh();
            },
            tooltip: 'Refresh File Browser'
        });
        widget.toolbar.insertItem(0, 'refresh', refreshButton);
        //widget.toolbar.insertItem(1, 'import', importButton);
        app.shell.add(widget, 'left');
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
/* harmony import */ var _filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./filebrowser */ "./lib/filebrowser.js");
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
    _filebrowser__WEBPACK_IMPORTED_MODULE_0__.drive,
    _filebrowser__WEBPACK_IMPORTED_MODULE_0__.yfile,
    _filebrowser__WEBPACK_IMPORTED_MODULE_0__.ynotebook,
    _filebrowser__WEBPACK_IMPORTED_MODULE_0__.sharedFileBrowser
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.5f602c466548fe0d1d66.js.map