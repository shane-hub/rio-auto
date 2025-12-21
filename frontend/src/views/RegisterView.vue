<template>
  <div class="register-container">
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
    <el-card class="register-card">
      <h2>{{ $t('register.title') }}</h2>
      <el-form :model="form" @submit.prevent="handleRegister">
        <el-form-item>
          <el-input v-model="form.email" :placeholder="$t('register.email')" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.username" :placeholder="$t('register.username')" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" :placeholder="$t('register.password')" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading" block>{{ $t('register.registerBtn') }}</el-button>
        </el-form-item>
        <div class="links">
            <router-link to="/login">{{ $t('login.backToLogin') }}</router-link>
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
const form = ref({ email: '', username: '', password: '' })
const loading = ref(false)

const currentLanguage = computed(() => {
  return locale.value === 'zh' ? '中文' : 'English'
})

const handleLangCommand = (command: string) => {
  locale.value = command
  localStorage.setItem('language', command)
}

const handleRegister = async () => {
    loading.value = true
    try {
        await axios.post('/auth/register', form.value)
        ElMessage.success(t('register.registerSuccess'))
        router.push('/login')
    } catch (e) {
        ElMessage.error(t('register.registerFailed'))
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.register-container {
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
.register-card {
  width: 400px;
  padding: 20px;
}
.links {
    text-align: right;
    margin-top: 10px;
}
</style>
