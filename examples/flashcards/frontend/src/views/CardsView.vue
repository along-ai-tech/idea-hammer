<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useCardsStore } from '@/stores/cards'
import type { CardCreate } from '@/api'

const store = useCardsStore()

const dialogVisible = reactive({ create: false, edit: false })
const form = reactive<CardCreate & { id?: number }>({ front: '', back: '' })

onMounted(() => store.fetchCards())

function openCreate() {
  form.front = ''
  form.back = ''
  dialogVisible.create = true
}

async function submitCreate() {
  if (!form.front || !form.back) {
    ElMessage.warning('正面和反面都不能为空')
    return
  }
  await store.createCard({ front: form.front, back: form.back })
  dialogVisible.create = false
  ElMessage.success('创建成功')
}

function openEdit(card: { id: number; front: string; back: string }) {
  form.id = card.id
  form.front = card.front
  form.back = card.back
  dialogVisible.edit = true
}

async function submitEdit() {
  if (!form.id) return
  await store.updateCard(form.id, { front: form.front, back: form.back })
  dialogVisible.edit = false
  ElMessage.success('更新成功')
}

async function confirmDelete(id: number) {
  await ElMessageBox.confirm('确认删除这张卡片？', '警告', { type: 'warning' })
  await store.deleteCard(id)
  ElMessage.success('已删除')
}
</script>

<template>
  <el-card>
    <template #header>
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <h2 style="margin: 0;">卡片管理</h2>
        <el-button type="primary" @click="openCreate">+ 新建卡片</el-button>
      </div>
    </template>

    <el-table :data="store.cards" v-loading="store.loading" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="front" label="正面（问题）" />
      <el-table-column prop="back" label="反面（答案）" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-empty v-if="!store.loading && store.cards.length === 0" description="还没有卡片，点右上角新建" />
  </el-card>

  <!-- 创建对话框 -->
  <el-dialog v-model="dialogVisible.create" title="新建卡片" width="500px">
    <el-form>
      <el-form-item label="正面（问题）">
        <el-input v-model="form.front" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="反面（答案）">
        <el-input v-model="form.back" type="textarea" :rows="3" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible.create = false">取消</el-button>
      <el-button type="primary" @click="submitCreate">确定</el-button>
    </template>
  </el-dialog>

  <!-- 编辑对话框 -->
  <el-dialog v-model="dialogVisible.edit" title="编辑卡片" width="500px">
    <el-form>
      <el-form-item label="正面（问题）">
        <el-input v-model="form.front" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="反面（答案）">
        <el-input v-model="form.back" type="textarea" :rows="3" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible.edit = false">取消</el-button>
      <el-button type="primary" @click="submitEdit">确定</el-button>
    </template>
  </el-dialog>
</template>
