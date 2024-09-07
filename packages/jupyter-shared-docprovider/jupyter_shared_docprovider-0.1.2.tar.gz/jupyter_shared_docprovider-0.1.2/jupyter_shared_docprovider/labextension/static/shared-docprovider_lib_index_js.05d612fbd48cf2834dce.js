"use strict";
(self["webpackChunk_jupyter_shared_docprovider_extension"] = self["webpackChunk_jupyter_shared_docprovider_extension"] || []).push([["shared-docprovider_lib_index_js"],{

/***/ "../shared-docprovider/lib/drive.js":
/*!******************************************!*\
  !*** ../shared-docprovider/lib/drive.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   SharedDrive: () => (/* binding */ SharedDrive)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! y-webrtc */ "webpack/sharing/consume/default/y-webrtc/y-webrtc");
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(y_webrtc__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! yjs */ "webpack/sharing/consume/default/yjs");
/* harmony import */ var yjs__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(yjs__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _provider__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./provider */ "../shared-docprovider/lib/provider.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





//import { ServerConnection } from './serverconnection';


const signalingServers = JSON.parse(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getOption('signalingServers'));
const MODEL = {
    name: '',
    path: '',
    type: '',
    writable: true,
    created: '',
    last_modified: '',
    mimetype: '',
    content: '',
    format: null
};
/**
 * A collaborative implementation for an `IDrive`, talking to other peers using WebRTC.
 */
class SharedDrive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(user, defaultFileBrowser, translator, globalAwareness, name) {
        this._onSync = (synced) => {
            var _a;
            if (synced.synced) {
                this._ready.resolve();
                (_a = this._fileSystemProvider) === null || _a === void 0 ? void 0 : _a.off('synced', this._onSync);
            }
        };
        this._onCreate = (options, sharedModel) => {
            if (typeof options.format !== 'string') {
                return;
            }
            const file = this._fileSystemContent.get(options.path);
            if (file === undefined) {
                return;
            }
            const key = `${options.format}:${options.contentType}:${options.path}`;
            const provider = new _provider__WEBPACK_IMPORTED_MODULE_6__.WebrtcProvider({
                url: '',
                path: options.path,
                format: options.format,
                contentType: options.contentType,
                model: sharedModel,
                user: this._user,
                translator: this._trans,
                signalingServers: this._signalingServers
            });
            this._fileProviders.set(key, provider);
            sharedModel.disposed.connect(() => {
                const provider = this._fileProviders.get(key);
                if (provider) {
                    provider.dispose();
                    this._fileProviders.delete(key);
                }
            });
        };
        this._fileChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._isDisposed = false;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._signalingServers = [];
        this._user = user;
        //this._defaultFileBrowser = defaultFileBrowser;
        this._trans = translator;
        this._globalAwareness = globalAwareness;
        //this._username = this._globalAwareness?.getLocalState()?.user.identity.name;
        //this._username = this._globalAwareness?.getLocalState()?.username;
        this._fileProviders = new Map();
        this.sharedModelFactory = new SharedModelFactory(this._onCreate);
        this.serverSettings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.ServerConnection.makeSettings();
        signalingServers.forEach((url) => {
            if (url.startsWith('ws://') || url.startsWith('wss://') || url.startsWith('http://') || url.startsWith('https://')) {
                // It's an absolute URL, keep it as-is.
                this._signalingServers.push(url);
            }
            else {
                // It's a Jupyter server relative URL, build the absolute URL.
                this._signalingServers.push(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(this.serverSettings.wsUrl, url));
            }
        });
        this.name = name;
        this._fileSystemYdoc = new yjs__WEBPACK_IMPORTED_MODULE_2__.Doc();
        this._fileSystemContent = this._fileSystemYdoc.getMap('content');
        this._fileSystemProvider = new y_webrtc__WEBPACK_IMPORTED_MODULE_1__.WebrtcProvider('fileSystem', this._fileSystemYdoc, {
            signaling: this._signalingServers,
            awareness: this._globalAwareness || undefined
        });
        this._fileSystemProvider.on('synced', this._onSync);
    }
    getDownloadUrl(path) {
        return new Promise(resolve => {
            resolve('');
        });
    }
    delete(path) {
        return new Promise(resolve => {
            resolve();
        });
    }
    restoreCheckpoint(path, checkpointID) {
        return new Promise(resolve => {
            resolve();
        });
    }
    deleteCheckpoint(path, checkpointID) {
        return new Promise(resolve => {
            resolve();
        });
    }
    //async importFile(path: string) {
    //  const model = await this._defaultFileBrowser.model.manager.services.contents.get(path, {content: true});
    //  const ymap = new Y.Map();
    //  const ytext = new Y.Text();
    //  this._fileSystemContent.set(model.name, ymap);
    //  ymap.set('init', new Y.Map());
    //  ymap.set('content', ytext);
    //  ytext.insert(0, model.content);
    //}
    async newUntitled(options = {}) {
        if (options.type === 'directory') {
            throw new Error('Cannot create directory');
        }
        let ext;
        if (options.type === 'notebook') {
            ext = 'ipynb';
        }
        else {
            ext = 'txt';
        }
        let idx = 0;
        let newName = '';
        const fileSystemContent = this._fileSystemContent.toJSON();
        while (newName === '') {
            const _newName = `untitled${idx}.${ext}`;
            if (_newName in fileSystemContent) {
                idx += 1;
            }
            else {
                newName = _newName;
            }
        }
        const model = {
            name: newName,
            path: newName,
            type: 'file',
            writable: true,
            created: '',
            last_modified: '',
            mimetype: '',
            content: null,
            format: null
        };
        const ymap = new yjs__WEBPACK_IMPORTED_MODULE_2__.Map();
        this._fileSystemContent.set(newName, ymap);
        this._fileChanged.emit({
            type: 'new',
            oldValue: null,
            newValue: model
        });
        return model;
    }
    async rename(path, newPath) {
        const fileSystemContent = this._fileSystemContent.toJSON();
        if (path in fileSystemContent) {
            this._fileSystemContent.delete(path);
        }
        if (!(newPath in fileSystemContent)) {
            const ymap = new yjs__WEBPACK_IMPORTED_MODULE_2__.Map();
            this._fileSystemContent.set(newPath, ymap);
        }
        const model = {
            name: newPath,
            path: newPath,
            type: 'file',
            writable: true,
            created: '',
            last_modified: '',
            mimetype: '',
            content: null,
            format: null
        };
        return model;
    }
    copy(path, toDir) {
        return new Promise(resolve => {
            resolve(MODEL);
        });
    }
    createCheckpoint(path) {
        const model = {
            id: '',
            last_modified: ''
        };
        return new Promise(resolve => {
            resolve(model);
        });
    }
    listCheckpoints(path) {
        return new Promise(resolve => {
            resolve([]);
        });
    }
    /**
     * A signal emitted when a file operation takes place.
     */
    get fileChanged() {
        return this._fileChanged;
    }
    /**
     * Test whether the manager has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the manager.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._fileProviders.forEach(p => p.dispose());
        this._fileProviders.clear();
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    async get(localPath, options) {
        let model;
        await this._ready;
        if (options && options.format && options.type) {
            // it's a file
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._fileProviders.get(key);
            if (provider) {
                //await provider.ready;
                model = {
                    name: localPath,
                    path: localPath,
                    type: 'file',
                    writable: true,
                    created: '',
                    last_modified: '',
                    mimetype: '',
                    content: null,
                    format: null
                };
                return new Promise(resolve => {
                    resolve(model);
                });
            }
        }
        // it's a directory
        const content = [];
        if (localPath === '') {
            // root directory
            this._fileSystemContent.forEach((value, key) => {
                content.push({
                    name: key,
                    path: key,
                    type: 'file',
                    writable: true,
                    created: '',
                    last_modified: '',
                    mimetype: '',
                    content: null,
                    format: null
                });
            });
            model = {
                name: '',
                path: '',
                type: 'directory',
                writable: false,
                created: '',
                last_modified: '',
                mimetype: '',
                content,
                format: null
            };
        }
        else {
            model = {
                name: localPath,
                path: localPath,
                type: 'file',
                writable: true,
                created: '',
                last_modified: '',
                mimetype: '',
                content: null,
                format: null
            };
        }
        return new Promise(resolve => {
            resolve(model);
        });
    }
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    async save(localPath, options = {}) {
        // Check that there is a provider - it won't e.g. if the document model is not collaborative.
        if (options.format && options.type) {
            const key = `${options.format}:${options.type}:${localPath}`;
            const provider = this._fileProviders.get(key);
            if (provider) {
                // Save is done from the backend
                const fetchOptions = {
                    type: options.type,
                    format: options.format,
                    content: false
                };
                return this.get(localPath, fetchOptions);
            }
        }
        return new Promise(resolve => {
            resolve(MODEL);
        });
        //return super.save(localPath, options);
    }
}
/**
 * Yjs sharedModel factory for real-time collaboration.
 */
class SharedModelFactory {
    /**
     * Shared model factory constructor
     *
     * @param _onCreate Callback on new document model creation
     */
    constructor(_onCreate) {
        this._onCreate = _onCreate;
        this._documentFactories = new Map();
    }
    /**
     * Register a SharedDocumentFactory.
     *
     * @param type Document type
     * @param factory Document factory
     */
    registerDocumentFactory(type, factory) {
        if (this._documentFactories.has(type)) {
            throw new Error(`The content type ${type} already exists`);
        }
        this._documentFactories.set(type, factory);
    }
    /**
     * Create a new `ISharedDocument` instance.
     *
     * It should return `undefined` if the factory is not able to create a `ISharedDocument`.
     */
    createNew(options) {
        if (typeof options.format !== 'string') {
            console.warn(`Only defined format are supported; got ${options.format}.`);
            return;
        }
        if (this._documentFactories.has(options.contentType)) {
            const factory = this._documentFactories.get(options.contentType);
            const sharedModel = factory(options);
            this._onCreate(options, sharedModel);
            return sharedModel;
        }
        return;
    }
}


/***/ }),

/***/ "../shared-docprovider/lib/index.js":
/*!******************************************!*\
  !*** ../shared-docprovider/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ISharedDrive: () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.ISharedDrive),
/* harmony export */   SharedDrive: () => (/* reexport safe */ _drive__WEBPACK_IMPORTED_MODULE_0__.SharedDrive),
/* harmony export */   WebrtcProvider: () => (/* reexport safe */ _provider__WEBPACK_IMPORTED_MODULE_1__.WebrtcProvider)
/* harmony export */ });
/* harmony import */ var _drive__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./drive */ "../shared-docprovider/lib/drive.js");
/* harmony import */ var _provider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./provider */ "../shared-docprovider/lib/provider.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../shared-docprovider/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module shared-docprovider
 */





/***/ }),

/***/ "../shared-docprovider/lib/provider.js":
/*!*********************************************!*\
  !*** ../shared-docprovider/lib/provider.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   WebrtcProvider: () => (/* binding */ WebrtcProvider)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! y-webrtc */ "webpack/sharing/consume/default/y-webrtc/y-webrtc");
/* harmony import */ var y_webrtc__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(y_webrtc__WEBPACK_IMPORTED_MODULE_2__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
class WebrtcProvider {
    /**
     * Construct a new WebSocketProvider
     *
     * @param options The instantiation options for a WebSocketProvider
     */
    constructor(options) {
        //private _onConnectionClosed = (event: any): void => {
        //  if (event.code === 1003) {
        //    console.error('Document provider closed:', event.reason);
        //    showErrorMessage(this._trans.__('Document session error'), event.reason, [
        //      Dialog.okButton()
        //    ]);
        //    // Dispose shared model immediately. Better break the document model,
        //    // than overriding data on disk.
        //    this._sharedModel.dispose();
        //  }
        //};
        this._onSync = (synced) => {
            if (synced.synced) {
                this._ready.resolve();
                //this._yWebrtcProvider?.off('status', this._onSync);
            }
        };
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this._isDisposed = false;
        this._path = options.path;
        this._contentType = options.contentType;
        this._format = options.format;
        this._sharedModel = options.model;
        this._awareness = options.model.awareness;
        this._yWebrtcProvider = null;
        //this._trans = options.translator;
        this._signalingServers = options.signalingServers;
        const user = options.user;
        user.ready
            .then(() => {
            this._onUserChanged(user);
        })
            .catch(e => console.error(e));
        user.userChanged.connect(this._onUserChanged, this);
        this._connect().catch(e => console.warn(e));
    }
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        //this._yWebrtcProvider?.off('connection-close', this._onConnectionClosed);
        //this._yWebrtcProvider?.off('status', this._onSync);
        (_a = this._yWebrtcProvider) === null || _a === void 0 ? void 0 : _a.destroy();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
    }
    async _connect() {
        this._yWebrtcProvider = new y_webrtc__WEBPACK_IMPORTED_MODULE_2__.WebrtcProvider(`${this._format}:${this._contentType}:${this._path}}`, this._sharedModel.ydoc, {
            signaling: this._signalingServers,
            awareness: this._awareness
        });
        this._yWebrtcProvider.on('synced', this._onSync);
        //this._yWebrtcProvider.on('connection-close', this._onConnectionClosed);
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}


/***/ }),

/***/ "../shared-docprovider/lib/tokens.js":
/*!*******************************************!*\
  !*** ../shared-docprovider/lib/tokens.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ISharedDrive: () => (/* binding */ ISharedDrive)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The collaborative drive.
 */
const ISharedDrive = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyter/shared-drive-extension:ISharedDrive');


/***/ })

}]);
//# sourceMappingURL=shared-docprovider_lib_index_js.05d612fbd48cf2834dce.js.map