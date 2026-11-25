<template>
  <section>
    <div class="toolbar">
      <h2>文章管理</h2>
      <el-button type="primary" @click="$router.push('/admin/new')">写文章</el-button>
    </div>

    <el-alert
      title="v0 无登录：管理端仅用于本机演示，勿直接暴露公网。"
      type="warning"
      :closable="false"
      show-icon
    />

    <el-table
      v-loading="loading"
      :data="posts"
      empty-text="还没有文章"
      style="margin-top: 16px"
    >
      <el-table-column prop="title" label="标题" />
      <el-table-column label="置顶" width="90">
        <template #default="{ row }">
          <el-tag v-if="row.is_pinned" type="danger" size="small">置顶</el-tag>
          <span v-else>-</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/admin/posts/${row.id}/edit`)">
            编辑
          </el-button>
          <el-button size="small" data-test="pin-post" @click="pin(row)">
            {{ row.is_pinned ? '取消置顶' : '置顶' }}
          </el-button>
          <el-button size="small" type="danger" data-test="delete-post" @click="remove(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" />
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { deletePost, listPosts, togglePin } from '../api/posts'

const posts = ref([])
const loading = ref(false)
const error = ref('')

async function load() {
  loading.value = true
  error.value = ''
  try {
    posts.value = await listPosts({ limit: 100, offset: 0 })
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function pin(row) {
  try {
    const updated = await togglePin(row.id)
    row.is_pinned = updated.is_pinned
    ElMessage.success(updated.is_pinned ? '已置顶' : '已取消置顶')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

async function remove(row) {
  try {
    await deletePost(row.id)
    posts.value = posts.value.filter((item) => item.id !== row.id)
    ElMessage.success('已删除')
  } catch (e) {
    ElMessage.error(e.message)
  }
}

onMounted(load)
</script>
