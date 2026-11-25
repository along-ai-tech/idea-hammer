<template>
  <div class="reaction-bar">
    <el-button
      :type="mine === 'up' ? 'primary' : 'default'"
      data-test="react-up"
      @click="$emit('react', 'up')"
    >
      👍 {{ up }}
    </el-button>
    <el-button
      :type="mine === 'down' ? 'danger' : 'default'"
      data-test="react-down"
      @click="$emit('react', 'down')"
    >
      👎 {{ down }}
    </el-button>
  </div>
</template>

<script setup>
defineProps({
  up: { type: Number, default: 0 },
  down: { type: Number, default: 0 },
  mine: { type: String, default: '' },
})

defineEmits(['react'])
</script>

<style scoped>
.reaction-bar {
  display: flex;
  gap: 8px;
  margin: 20px 0;
}
</style>
