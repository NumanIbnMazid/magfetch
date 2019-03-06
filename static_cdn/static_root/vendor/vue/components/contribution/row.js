// {% load static %}

Vue.component('row', {
    template: `
            <tr>
                <td>{{ counter }}</td>
                <td>
                    <span class="thumb-sm avatar pull-left">
                        <img src="/static/images/raw/avatar/avatar.jpg">
                    </span>
                    {{ user }}
                </td>
                <td>{{ title }}</td>
                <td>{{ category }}</td>
                <td>{{ file_type }}</td>
                <td>{{ is_commented }}</td>
                <td>{{ is_selected }}</td>
                <td><button @click="showModal">View File</button></td>
            </tr>
        `,
    props: ['counter', 'user', 'title', 'category', 'file_type', 'file', 'is_commented', 'is_selected', 'id'],
    methods: {
        showModal: function () {
            this.$bus.$emit('showModal', this.title, this.category, this.file_type, this.file, this.is_commented, this.is_selected, this.id);
        }
    }
});