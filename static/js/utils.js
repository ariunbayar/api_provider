window.Utils = (function () {

    function Utils(){

    };


    Utils.prototype.toFormData = function toFormData(data) {
        let form_data = new FormData();
        for (let key in data) {
            form_data.append(key, data[key]);
        }
        return form_data;
    }

    Utils.prototype.xhr_post = function xhr_post(data, url, success_fn, error_fn) {

        let form_data = this.toFormData(data);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function() {
            if (this.readyState == 4) {

                if (this.status == 200) {
                    let data;
                    try {
                        data = JSON.parse(xhr.responseText);
                    } catch (error) {
                        data = null;
                    }

                    success_fn(data);
                } else {
                    error_fn(xhr);
                }
            }
        };
        xhr.send(form_data);

    }


    return new Utils();

})();
