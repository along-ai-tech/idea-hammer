<template>
  <section v-if="post">
    <div class="title-row">
      <el-tag v-if="post.is_pinned" type="danger" size="small">📌 置顶</el-tag>
      <h2>{{ post.title }}</h2>
    </div>
    <div class="meta">
      <span>{{ formatDate(post.created_at) }}</span>
      <span>评论 {{ comments.length }}</span>
    </div>
    <p class="content">{{ post.content }}</p>

    <ReactionBar :up="counts.up" :down="counts.down" :mine="counts.mine" @react="onReact" />

    <el-divider />
    <h3>评论（{{ comments.length }}）</h3>
    <p v-if="!comments.length" class="meta">还没有评论，来抢沙发。</p>
    <div v-for="comment in comments" :key="comment.id" class="comment-item">
      <span class="comment-author">{{ comment.nickname }}</span>
      <span>{{ comment.content }}</span>
    </div>

    <el-form class="comment-form" label-width="72px">
      <el-form-item label="昵称" :error="formErrors.nickname">
        <el-input v-model="form.nickname" data-test="nickname" maxlength="50" />
      </el-form-item>
      <el-form-item label="评论" :error="formErrors.content">
        <el-input
          v-model="form.content"
          data-test="content"
          type="textarea"
          :rows="3"
          maxlength="5000"
        />
      </el-form-item>
      <el-form-item>
        <el-button
          type="primary"
          data-test="submit-comment"
          :loading="submitting"
          @click="submitComment"
        >
          发表
        </el-button>
      </el-form-item>
    </el-form>
  </section>

  <el-skeleton v-else-if="loading" :rows="6" animated />
  <el-alert v-else-if="error" :title="error" type="error" show-icon :closable="false" />
</template>

<script setup>
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getPost } from '../api/posts'
import { createComment } from '../api/comments'
import { reactToPost } from '../api/reactions'
import { applyReaction } from '../utils/reaction'
import { validateComment } from '../utils/validation'
import { formatDate } from '../utils/format'
import ReactionBar from '../components/ReactionBar.vue'

const props = defineProps({
  id: { type: String, default: '' },
})

const post = ref(null)
const comments = ref([])
const counts = reactive({ up: 0, down: 0, mine: '' })
const form = reactive({ nickname: '', content: '' })
const formErrors = reactive({ nickname: '', content: '' })
const loading = ref(false)
const error = ref('')
const submitting = ref(false)

async function load() {
  loading.value = true
  error.value = ''
  try {
    const data = await getPost(props.id)
    post.value = data
    comments.value = data.comments || []
    counts.up = data.up_count || 0
    counts.down = data.down_count || 0
    counts.mine = ''
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function onReact(type) {
  const previous = { up: counts.up, down: counts.down, mine: counts.mine }
  Object.assign(counts, applyReaction(previous, type))
  try {
    const result = await reactToPost(post.value.id, type)
    counts.up = result.up_count
    counts.down = result.down_count
    counts.mine = result.my_reaction
  } catch (e) {
    Object.assign(counts, previous)
    ElMessage.error(e.message)
  }
}

async function submitComment() {
  const check = validateComment(form)
  formErrors.nickname = check.errors.nickname || ''
  formErrors.content = check.errors.content || ''
  if (!check.valid) return

  submitting.value = true
  try {
    const created = await createComment(post.value.id, {
      nickname: form.nickname.trim(),
      content: form.content.trim(),
    })
    comments.value = [...comments.value, created]
    form.content = ''
    ElMessage.success('评论已发布')
  } catch (e) {
    ElMessage.error(e.message)
  } finally {
    submitting.value = false
  }
}

onMounted(load)
watch(() => props.id, load)
</script>

<style scoped>
.comment-form {
  margin-top: 20px;
}
</style>
