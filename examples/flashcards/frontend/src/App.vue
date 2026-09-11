<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
</script>

<template>
  <el-config-provider>
    <div class="app">
      <header class="app-header">
        <h1>💡 IdeaHammer Flashcards</h1>
        <nav>
          <router-link to="/">首页</router-link>
          <router-link to="/cards">卡片</router-link>
          <router-link to="/study">学习</router-link>
        </nav>
      </header>
      <main class="app-main">
        <router-view />
      </main>
    </div>
  </el-config-provider>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background: #f5f7fa;
}
.app-header {
  background: #fff;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}
.app-header h1 {
  margin: 0;
  font-size: 20px;
}
.app-header nav {
  display: flex;
  gap: 24px;
}
.app-header a {
  color: #409eff;
  text-decoration: none;
}
.app-main {
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
