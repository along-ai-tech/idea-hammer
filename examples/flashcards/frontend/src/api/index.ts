import axios from 'axios'

export const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

export interface Card {
  id: number
  front: string
  back: string
}

export interface CardCreate {
  front: string
  back: string
}
