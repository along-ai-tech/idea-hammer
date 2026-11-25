<template>
  <el-card class="post-card" shadow="hover" :class="{ pinned: post.is_pinned }">
    <div class="title-row">
      <el-tag v-if="post.is_pinned" type="danger" size="small">📌 置顶</el-tag>
      <router-link :to="`/posts/${post.id}`" class="post-title">{{ post.title }}</router-link>
    </div>
    <p class="excerpt">{{ excerpt(post.content) }}</p>
    <div class="meta">
      <span>{{ formatDate(post.created_at) }}</span>
      <span v-if="typeof post.up_count === 'number'">{{ reactionSummary(post.up_count, post.down_count || 0) }}</span>
    </div>
  </el-card>
</template>

<script setup>
import { formatDate, excerpt, reactionSummary } from '../utils/format'

defineProps({
  post: { type: Object, required: true },
})
</script>

<style scoped>
.post-card {
  margin-bottom: 12px;
}

.post-card.pinned {
  border-left: 4px solid #f56c6c;
}
</style>
