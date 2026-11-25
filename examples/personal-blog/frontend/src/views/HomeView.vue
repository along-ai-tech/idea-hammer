<template>
  <section>
    <div class="toolbar">
      <h2>最新文章</h2>
      <el-button type="primary" @click="$router.push('/admin/new')">写文章</el-button>
    </div>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" />
    <el-skeleton v-if="loading" :rows="4" animated />
    <el-empty v-else-if="!posts.length" description="还没有文章" />

    <template v-else>
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
      <div class="pager">
        <el-button :disabled="offset === 0" @click="prev">上一页</el-button>
        <el-button :disabled="!hasMore" @click="next">下一页</el-button>
      </div>
    </template>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { listPosts } from '../api/posts'
import PostCard from '../components/PostCard.vue'

const PAGE_SIZE = 5
const posts = ref([])
const offset = ref(0)
const loading = ref(false)
const error = ref('')

const hasMore = computed(() => posts.value.length === PAGE_SIZE)

async function load() {
  loading.value = true
  error.value = ''
  try {
    posts.value = await listPosts({ limit: PAGE_SIZE, offset: offset.value })
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function prev() {
  offset.value = Math.max(0, offset.value - PAGE_SIZE)
  load()
}

function next() {
  offset.value += PAGE_SIZE
  load()
}

onMounted(load)
</script>
