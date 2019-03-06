Vue.component('modal', {
    template: '#modal-template',
    data: function () {
        return {
            title: '',
            category: '',
            file_type: '',
            file: '',
            is_commented: '',
            is_selected: '',
            id: 0
        }
    },
    mounted: function () {
        this.$bus.$on('showModal', function (title, category, file_type, file, is_commented, is_selected, id) {
            this.title = title;
            this.category = category;
            this.file_type = file_type;
            this.file = file;
            this.is_commented = is_commented;
            this.is_selected = is_selected;
            this.id = id;
        }.bind(this));
    }
});