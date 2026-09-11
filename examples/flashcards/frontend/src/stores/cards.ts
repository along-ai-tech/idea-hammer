import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api, type Card, type CardCreate } from '@/api'

export const useCardsStore = defineStore('cards', () => {
  const cards = ref<Card[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchCards() {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get<Card[]>('/cards')
      cards.value = data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : 'unknown error'
    } finally {
      loading.value = false
    }
  }

  async function createCard(payload: CardCreate) {
    const { data } = await api.post<Card>('/cards', payload)
    cards.value.push(data)
    return data
  }

  async function updateCard(id: number, payload: CardCreate) {
    const { data } = await api.put<Card>(`/cards/${id}`, payload)
    const idx = cards.value.findIndex((c) => c.id === id)
    if (idx >= 0) cards.value[idx] = data
    return data
  }

  async function deleteCard(id: number) {
    await api.delete(`/cards/${id}`)
    cards.value = cards.value.filter((c) => c.id !== id)
  }

  return { cards, loading, error, fetchCards, createCard, updateCard, deleteCard }
})
