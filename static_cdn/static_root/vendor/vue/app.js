new Vue({
    el: '#app',
    data: {
        showModal: false
    },
    mounted: function () {
        this.$bus.$on('showModal', function () {
            this.showModal = true;
        }.bind(this));
    }
});