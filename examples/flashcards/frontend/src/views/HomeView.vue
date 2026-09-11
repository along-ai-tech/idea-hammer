<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '@/api'

const healthStatus = ref<string>('checking...')
const healthError = ref<string | null>(null)

onMounted(async () => {
  try {
    const { data } = await api.get<{ status: string }>('/health')
    healthStatus.value = data.status === 'ok' ? '✅ 后端连通' : `异常: ${data.status}`
  } catch (e: unknown) {
    healthError.value = e instanceof Error ? e.message : 'unknown'
    healthStatus.value = '❌ 后端不可达'
  }
})
</script>

<template>
  <el-card>
    <template #header>
      <h2>IdeaHammer 演示项目</h2>
    </template>
    <p>本地闪卡应用 — Phase 1 骨架已就绪。</p>
    <p>
      <strong>后端健康检查：</strong>
      <span>{{ healthStatus }}</span>
      <span v-if="healthError" style="color: red; margin-left: 8px;">({{ healthError }})</span>
    </p>
    <el-divider />
    <h3>下一步</h3>
    <el-link type="primary" href="/cards">→ 进入卡片管理</el-link>
  </el-card>
</template>
