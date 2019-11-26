(function() {

    function hideNotification(e) {

        let url = '/notification/mark-as-read/';
        let data = {pk: parseInt(e.target.getAttribute('data-id'))}

        window.Utils.xhr_post(data, url, function(data){
            if (data.success == true) {
                e.target.classList.add('hidden');
                setTimeout(function(){
                    e.target.style.display = 'none';
                }, 200);
            }
        });

    }

    var items = document.querySelectorAll('.notifications .notification');
    items.forEach(function(item){
        item.addEventListener('click', hideNotification);
    });

})();
