<template>
  <section>
    <h2>{{ isEdit ? '编辑文章' : '写文章' }}</h2>

    <el-form label-width="80px">
      <el-form-item label="标题" :error="errors.title">
        <el-input v-model="form.title" data-test="title" maxlength="200" />
      </el-form-item>
      <el-form-item label="正文" :error="errors.content">
        <el-input v-model="form.content" data-test="content" type="textarea" :rows="16" />
      </el-form-item>
      <el-form-item label="置顶">
        <el-switch v-model="form.is_pinned" />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          data-test="save-post"
          :loading="saving"
          @click="save"
        >
          保存
        </el-button>
        <el-button @click="$router.push('/admin')">返回</el-button>
      </el-form-item>
    </el-form>

    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" />
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createPost, getPost, updatePost } from '../api/posts'
import { validatePost } from '../utils/validation'

const props = defineProps({
  id: { type: String, default: '' },
})

const router = useRouter()
const form = reactive({ title: '', content: '', is_pinned: false })
const errors = reactive({ title: '', content: '' })
const saving = ref(false)
const error = ref('')
const isEdit = computed(() => Boolean(props.id))

async function load() {
  if (!isEdit.value) return
  try {
    const data = await getPost(props.id)
    form.title = data.title
    form.content = data.content
    form.is_pinned = data.is_pinned
  } catch (e) {
    error.value = e.message
  }
}

async function save() {
  const check = validatePost(form)
  errors.title = check.errors.title || ''
  errors.content = check.errors.content || ''
  if (!check.valid) return

  saving.value = true
  error.value = ''
  const payload = {
    title: form.title.trim(),
    content: form.content.trim(),
    is_pinned: form.is_pinned,
  }
  try {
    if (isEdit.value) {
      await updatePost(props.id, payload)
    } else {
      await createPost(payload)
    }
    ElMessage.success('已保存')
    router.push('/admin')
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
