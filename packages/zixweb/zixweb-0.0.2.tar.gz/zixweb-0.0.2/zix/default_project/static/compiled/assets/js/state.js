
class State {
    constructor(appName, cookieExpDays=365) {
        this._var = {};
        this._cb = {};
        this._cookies = new Set();
        this._sessions = new Set();
        this._cookieExpDays = cookieExpDays;
        sessionStorage.SessionName = appName;
    }
    remove(name) {
        this._sessions.delete(name);
        this._cookies.delete(name);
        delete this._var[name];  
        sessionStorage.removeItem(name);
        this.deleteCookie(name);
        for (const cb of this.getCBs(name)) {
            cb();
        }        
        this.removeAllCBs(name);
    }
    async set(name, value, persist=0) { // 0: memory, 1: session, 2: cookie
        if (persist === 0) {
            this._var[name] = value;            
            this._sessions.delete(name);
            this._cookies.delete(name);
            sessionStorage.removeItem(name);
            this.deleteCookie(name);
        }
        else if (persist === 1) {
            delete this._var[name];
            this._sessions.add(name);
            this._cookies.delete(name);
            sessionStorage.setItem(name, value);            
            this.deleteCookie(name);
        } else if (persist === 2) {
            delete this._var[name];
            this._sessions.delete(name);
            this._cookies.add(name);
            sessionStorage.removeItem(name, value);            
            this.setCookie(name, value);
        }
        for (const cb of this.getCBs(name)) {
            cb();
        }
        return this._var[name];
    }
    get(name) {
        return this._var[name] || sessionStorage.getItem(name) || this.getCookie(name);
    }
    getCBs(name) {
        if (this._cb[name] == undefined) {
            this._cb[name] = new Array();
        }
        return this._cb[name];
    }
    addCB(name, fn) {
        var cbs = this.getCBs(name);
        cbs.push(fn);
    }
    removeCB(name, fn) {
        var cbs = this.getCBs(name);
        for (var i = 0; i < cbs.length; i++) {
            if (cbs[i] === fn) {
                cbs.splice(i, 1);
                break;
            }
        }
    }
    removeAllCBs(name) {
        delete this._cb[name];
    }
    setCookie(name, value, days=365) {
        var expires = '';
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = '; expires=' + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }
    getCookie(name) {
        var nameEQ = name + '=';
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }
    deleteCookie(name) {   
        document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    }
}