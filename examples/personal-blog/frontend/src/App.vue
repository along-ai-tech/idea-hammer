<template>
  <el-container class="page">
    <el-header class="header">
      <router-link to="/" class="brand">Personal Blog</router-link>
      <nav class="nav">
        <router-link to="/">首页</router-link>
        <router-link to="/posts">文章</router-link>
        <router-link to="/admin">管理</router-link>
      </nav>
    </el-header>
    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>
