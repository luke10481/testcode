<template>
  <div class="requests-container">
    <h2>Requests Data</h2>

    <div class="table-container">
      <table class="requests-table">
        <thead>
        <tr>
          <th>URL</th>
          <th>Request Data</th>
          <th>Picture</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in requests" :key="index">
          <td class="url-cell">
            <a :href="item.url" target="_blank">{{ item.url }}</a>
          </td>
          <td class="data-cell">
            <pre>{{ formatJson(item.request_data) }}</pre>
          </td>
          <td class="image-cell">
            <div
                class="thumbnail"
                @click="showFullImage(item.picture_filepath)"
            >
              <img
                  :src="getImageUrl(item.picture_filepath)"
                  :alt="'Image for ' + item.url"
                  @error="handleImageError"
              />
            </div>
          </td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- 图片模态框 -->
    <div v-if="selectedImage" class="modal" @click.self="selectedImage = null">
      <div class="modal-content">
        <button class="close-btn" @click="selectedImage = null">×</button>
        <img :src="getImageUrl(selectedImage)" class="full-image" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface RequestItem {
  url: string
  request_data: string
  picture_filepath: string
}

const requests = ref<RequestItem[]>([])
const selectedImage = ref<string | null>(null)

// 获取数据
const fetchRequests = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/requests')
    requests.value = await response.json()
  } catch (error) {
    console.error('Failed to fetch requests:', error)
  }
}

// 格式化JSON数据
const formatJson = (data: string): string => {
  try {
    return JSON.stringify(JSON.parse(data), null, 2)
  } catch {
    return data
  }
}

// 获取图片URL
const getImageUrl = (filepath: string | null): string => {
  if (!filepath) return ''
  return `http://localhost:8000/api/image/${filepath}`
}

// 显示完整图片
const showFullImage = (filepath: string) => {
  selectedImage.value = filepath
}

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgZmlsbD0iI2VlZSIvPjx0ZXh0IHg9IjUwIiB5PSI1MCIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5Ij5JbWFnZTwvdGV4dD48L3N2Zz4='
}

onMounted(() => {
  fetchRequests()
})
</script>

<!-- 样式保持不变 -->
<style scoped>
/* 添加或修改以下样式 */
.requests-container {
  padding: 20px;
}

.table-container {
  overflow-x: auto;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.requests-table th,
.requests-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
}

.requests-table th {
  background-color: #f5f5f5;
  font-weight: 600;
}

.url-cell {
  max-width: 200px;
  word-break: break-all;
}

.data-cell pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 13px;
  max-width: 300px;
  max-height: 100px;
  overflow-y: auto;
}

/* 修改这里：缩小缩略图 */
.image-cell {
  width: auto;
}

.thumbnail {
  width: 1.5em; /* 使用相对单位 */
  height: 1.5em;
  min-width: 40px; /* 最小尺寸 */
  min-height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  overflow: hidden;
}

.thumbnail img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.thumbnail:hover img {
  transform: scale(1.05);
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.full-image {
  max-width: 100%;
  max-height: 90vh;
  object-fit: contain;
}

.close-btn {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: white;
  font-size: 30px;
  cursor: pointer;
  padding: 5px 10px;
}
</style>