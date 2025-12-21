<template>
  <div class="login-container">
    <div class="lang-switch">
      <el-dropdown @command="handleLangCommand" style="cursor: pointer;">
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
    </div>
    <el-card class="login-card">
      <h2>{{ $t('login.title') }}</h2>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" :placeholder="$t('login.username')" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" :placeholder="$t('login.password')" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" block>{{ $t('login.loginBtn') }}</el-button>
        </el-form-item>
        <div class="links">
            <router-link to="/register">{{ $t('login.createAccount') }}</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, computed } from 'vue'
// @ts-ignore
import { useRouter } from 'vue-router'
// @ts-ignore
import { useI18n } from 'vue-i18n'
import axios from '@/api/axios'

const router = useRouter()
const { t, locale } = useI18n()
const form = ref({ username: '', password: '' })
const loading = ref(false)

const currentLanguage = computed(() => {
  return locale.value === 'zh' ? '中文' : 'English'
})

const handleLangCommand = (command: string) => {
  locale.value = command
  localStorage.setItem('language', command)
}

const handleLogin = async () => {
    loading.value = true
    try {
        // FastAPI OAuth2 expects form data, but we can send JSON if configured or use URLSearchParams
        const params = new URLSearchParams()
        params.append('username', form.value.username)
        params.append('password', form.value.password)
        
        const res = await axios.post('/auth/token', params) as any
        localStorage.setItem('token', res.access_token)
        
        // Fetch user info
        const userRes = await axios.get('/auth/me') as any
        localStorage.setItem('user', JSON.stringify(userRes))
        
        ElMessage.success(t('common.welcome') + ' ' + userRes.username)
        router.push('/')
    } catch (e) {
        ElMessage.error(t('login.loginFailed'))
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
  position: relative;
}
.lang-switch {
  position: absolute;
  top: 20px;
  right: 20px;
}
.login-card {
  width: 400px;
  padding: 20px;
}
.links {
    text-align: right;
    margin-top: 10px;
}
</style>
