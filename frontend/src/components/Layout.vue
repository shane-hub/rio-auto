<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        router
      >
        <div class="logo">Rio Auto</div>
        <el-menu-item index="/">
          <el-icon><Menu /></el-icon>
          <span>{{ $t('menu.dashboard') }}</span>
        </el-menu-item>
        <el-menu-item index="/projects">
          <el-icon><Folder /></el-icon>
          <span>{{ $t('menu.projects') }}</span>
        </el-menu-item>
        <el-menu-item index="/test-cases">
          <el-icon><Document /></el-icon>
          <span>{{ $t('menu.testCases') }}</span>
        </el-menu-item>
        <el-menu-item index="/tasks">
          <el-icon><VideoPlay /></el-icon>
          <span>{{ $t('menu.tasks') }}</span>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><DataLine /></el-icon>
          <span>{{ $t('menu.reports') }}</span>
        </el-menu-item>
        <el-menu-item v-if="user.is_superuser" index="/admin/users">
          <el-icon><UserFilled /></el-icon>
          <span>{{ $t('menu.userManagement') }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <div class="header-content">
          <el-dropdown @command="handleLangCommand" style="margin-right: 20px; cursor: pointer;">
            <span class="el-dropdown-link">
              {{ currentLanguage }}
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="zh">中文</el-dropdown-item>
                <el-dropdown-item command="en">English</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span>{{ $t('common.welcome') }}, {{ user.username }}</span>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, computed } from 'vue'
// @ts-ignore
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()
const user = ref(JSON.parse(localStorage.getItem('user') || '{}'))

const currentLanguage = computed(() => {
  return locale.value === 'zh' ? '中文' : 'English'
})

const handleLangCommand = (command: string) => {
  locale.value = command
  localStorage.setItem('language', command)
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.el-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e6e6e6;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  border-bottom: 1px solid #e6e6e6;
}
.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
</style>
