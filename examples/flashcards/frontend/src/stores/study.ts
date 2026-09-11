import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import { api, type Card } from '@/api'

/** 学习模式卡片：含 SM-2 调度字段 */
export interface StudyCard extends Card {
  repetitions: number
  interval: number
  easiness_factor: number
  due_at: string | null
  last_reviewed_at: string | null
}

export const useStudyStore = defineStore('study', () => {
  const queue = ref<StudyCard[]>([])
  const currentIndex = ref(0)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const currentCard = computed(() => queue.value[currentIndex.value] ?? null)
  const isFinished = computed(() => currentIndex.value >= queue.value.length)
  const progress = computed(
    () => `${Math.min(currentIndex.value + 1, queue.value.length)} / ${queue.value.length}`,
  )

  async function fetchQueue() {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get<StudyCard[]>('/study/queue')
      queue.value = data
      currentIndex.value = 0
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'unknown error'
      queue.value = []
    } finally {
      loading.value = false
    }
  }

  async function submitReview(quality: number) {
    const card = currentCard.value
    if (!card) return
    await api.post(`/study/${card.id}/review`, { quality })
  }

  function nextCard() {
    currentIndex.value++
  }

  return {
    queue,
    currentIndex,
    loading,
    error,
    currentCard,
    isFinished,
    progress,
    fetchQueue,
    submitReview,
    nextCard,
  }
})
