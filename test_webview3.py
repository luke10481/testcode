import webview
import threading
import time


class Api:
    def __init__(self):
        self.data = [
            {"id": 1, "url": "www.baidu.com", "request": "POST", "image": "https://via.placeholder.com/50/FF0000"},
        ]

    def get_data(self):
        """返回当前数据给前端"""
        return self.data

    def update_data(self, new_data):
        """更新数据，可以被Python端调用"""
        self.data = new_data


html = """
<!DOCTYPE html>
<div id="app">
    <table border="1">
        <tr><th>ID</th><th>URL</th><th>请求</th><th>图片</th></tr>
        <tr v-for="item in items">
            <td>{{item.id}}</td>
            <td>{{item.url}}</td>
            <td>{{item.request}}</td>
            <td><img :src="item.image" width="50"></td>
        </tr>
    </table>
</div>
<script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
<script>
const { createApp } = Vue;

createApp({
    data() {
        return {
            items: []
        }
    },
    mounted() {
        this.loadData();
        // 设置每2秒自动刷新数据
        setInterval(() => {
            this.loadData();
        }, 500);
    },
    methods: {
        async loadData() {
            if (window.pywebview && window.pywebview.api) {
                try {
                    const data = await window.pywebview.api.get_data();
                    this.items = data;
                } catch (error) {
                    console.error('加载数据失败:', error);
                }
            }
        }
    }
}).mount('#app');
</script>
"""

api = Api()
window = webview.create_window(
    '自动刷新表格',
    html=html,
    width=700,
    height=400,
    js_api=api
)


# 示例：模拟Python端更新数据
def update_from_python():
    # 等待窗口加载
    time.sleep(2)

    # 第一次更新数据
    new_data1 = [
        {"id": 1, "url": "www.google.com", "request": "GET", "image": "https://via.placeholder.com/50/00FF00"},
        {"id": 2, "url": "www.github.com", "request": "POST", "image": "https://via.placeholder.com/50/0000FF"}
    ]
    api.update_data(new_data1)
    print("Python端数据已更新（第一次）")

    # 再等几秒后进行第二次更新
    time.sleep(5)

    new_data2 = [
        {"id": 1, "url": "www.python.org", "request": "GET", "image": "https://via.placeholder.com/50/FF00FF"},
        {"id": 2, "url": "www.example.com", "request": "PUT", "image": "https://via.placeholder.com/50/FFFF00"},
        {"id": 3, "url": "www.test.com", "request": "DELETE", "image": "https://via.placeholder.com/50/00FFFF"}
    ]
    api.update_data(new_data2)
    print("Python端数据已更新（第二次）")


# 在另一个线程中运行更新函数
threading.Thread(target=update_from_python, daemon=True).start()

webview.start()