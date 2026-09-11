<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useStudyStore } from '@/stores/study'

const store = useStudyStore()
const showAnswer = ref(false)

onMounted(() => store.fetchQueue())

async function rate(quality: number) {
  await store.submitReview(quality)
  showAnswer.value = false
  store.nextCard()
}

function reveal() {
  showAnswer.value = true
}

function restart() {
  showAnswer.value = false
  store.fetchQueue()
}
</script>

<template>
  <el-card class="study-card-wrapper">
    <template #header>
      <div class="header">
        <h2>📚 学习模式</h2>
        <span class="progress">{{ store.progress }}</span>
      </div>
    </template>

    <!-- 加载中 -->
    <div v-if="store.loading" class="state-loading">
      <div class="spinner"></div>
      <p>加载复习队列...</p>
    </div>

    <!-- 错误 -->
    <el-alert
      v-else-if="store.error"
      :title="store.error"
      type="error"
      :closable="false"
    />

    <!-- 复习完毕 -->
    <div v-else-if="store.isFinished" class="state-finished">
      <el-empty description="🎉 今日复习完毕">
        <p v-if="store.queue.length === 0">没有待复习的卡片</p>
        <p v-else>所有卡片都复习完了</p>
        <template #footer>
          <el-button type="primary" @click="restart">刷新队列</el-button>
          <el-link type="primary" href="/cards" style="margin-left: 12px;">
            → 去看卡片管理
          </el-link>
        </template>
      </el-empty>
    </div>

    <!-- 复习卡片 -->
    <div v-else-if="store.currentCard" class="card-area">
      <transition name="flip" mode="out-in">
        <div v-if="!showAnswer" key="front" class="card-face front">
          <div class="card-label">正面（问题）</div>
          <div class="card-text">{{ store.currentCard.front }}</div>
          <el-button type="primary" size="large" @click="reveal">
            显示答案 →
          </el-button>
        </div>

        <div v-else key="back" class="card-face back">
          <div class="card-label">正面（问题）</div>
          <div class="card-text secondary">{{ store.currentCard.front }}</div>
          <div class="divider"></div>
          <div class="card-label">反面（答案）</div>
          <div class="card-text answer">{{ store.currentCard.back }}</div>
          <div class="rating-section">
            <div class="rating-label">你的掌握度（0 = 完全不会 / 5 = 完全掌握）：</div>
            <div class="rating-buttons">
              <el-button-group>
                <el-button type="danger" @click="rate(0)">0</el-button>
                <el-button type="danger" @click="rate(1)">1</el-button>
                <el-button type="danger" @click="rate(2)">2</el-button>
                <el-button type="success" @click="rate(3)">3</el-button>
                <el-button type="success" @click="rate(4)">4</el-button>
                <el-button type="success" @click="rate(5)">5</el-button>
              </el-button-group>
            </div>
            <div class="rating-hint">
              <span class="hint-bad">0-2 答错：明天重学</span>
              <span class="hint-good">3-5 答对：按 SM-2 调度</span>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </el-card>
</template>

<style scoped>
.study-card-wrapper {
  max-width: 800px;
  margin: 0 auto;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.header h2 {
  margin: 0;
}
.progress {
  font-size: 16px;
  color: #909399;
  font-weight: 600;
}
.state-loading,
.state-finished {
  padding: 60px 0;
  text-align: center;
}
.card-area {
  padding: 40px 0;
  min-height: 400px;
}
.card-face {
  text-align: center;
  padding: 40px;
}
.card-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
.card-text {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin: 16px 0 32px;
  line-height: 1.4;
}
.card-text.secondary {
  font-size: 20px;
  color: #909399;
  margin: 8px 0 16px;
}
.card-text.answer {
  font-size: 28px;
  color: #67c23a;
}
.divider {
  height: 1px;
  background: #ebeef5;
  margin: 24px 0;
}
.rating-section {
  margin-top: 32px;
}
.rating-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 16px;
}
.rating-buttons {
  display: flex;
  justify-content: center;
}
.rating-hint {
  margin-top: 16px;
  display: flex;
  justify-content: center;
  gap: 24px;
  font-size: 12px;
}
.hint-bad {
  color: #f56c6c;
}
.hint-good {
  color: #67c23a;
}

/* 加载 spinner */
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e4e7ed;
  border-top-color: #409eff;
  border-radius: 50%;
  margin: 0 auto 16px;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 翻转动画 */
.flip-enter-active,
.flip-leave-active {
  transition: all 0.3s ease;
}
.flip-enter-from {
  opacity: 0;
  transform: rotateY(90deg);
}
.flip-leave-to {
  opacity: 0;
  transform: rotateY(-90deg);
}
</style>
