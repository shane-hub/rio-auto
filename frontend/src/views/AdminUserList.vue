<template>
  <div class="admin-user-list">
    <div class="header">
      <h2>{{ $t('admin.userManagement') }}</h2>
      <el-button type="primary" @click="fetchUsers">{{ $t('admin.refresh') }}</el-button>
    </div>

    <el-table :data="users" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" :label="$t('admin.id')" width="80" />
      <el-table-column prop="username" :label="$t('admin.username')" />
      <el-table-column prop="email" :label="$t('admin.email')" />
      <el-table-column prop="is_superuser" :label="$t('admin.role')">
        <template #default="{ row }">
          <el-tag :type="row.is_superuser ? 'danger' : 'info'">{{ row.is_superuser ? $t('admin.admin') : $t('admin.user') }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" :label="$t('admin.status')">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'warning'">{{ row.is_active ? $t('admin.active') : $t('admin.inactive') }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('common.actions')" width="200">
        <template #default="{ row }">
          <el-button 
            size="small" 
            :type="row.is_active ? 'warning' : 'success'" 
            @click="toggleStatus(row)"
            :disabled="row.id === currentUser.id"
          >
            {{ row.is_active ? $t('admin.deactivate') : $t('admin.activate') }}
          </el-button>
          <el-button 
            size="small" 
            type="danger" 
            @click="deleteUser(row)"
            :disabled="row.id === currentUser.id"
          >
            {{ $t('admin.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted } from 'vue'
// @ts-ignore
import { useI18n } from 'vue-i18n'
import axios from '@/api/axios'
import { ElMessage, ElMessageBox } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  is_superuser: boolean
}

const { t } = useI18n()
const users = ref<User[]>([])
const loading = ref(false)
const currentUser = ref<User>(JSON.parse(localStorage.getItem('user') || '{}'))

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await axios.get('/admin/users')
    users.value = res as any
  } catch (error) {
    ElMessage.error(t('admin.fetchFailed'))
  } finally {
    loading.value = false
  }
}

const toggleStatus = async (user: User) => {
  try {
    await axios.put(`/admin/users/${user.id}/status?is_active=${!user.is_active}`)
    user.is_active = !user.is_active
    ElMessage.success(t('admin.statusSuccess'))
  } catch (error) {
    ElMessage.error(t('admin.statusFailed'))
  }
}

const deleteUser = (user: User) => {
  ElMessageBox.confirm(
    t('admin.deleteConfirmMessage', { name: user.username }),
    t('admin.deleteConfirmTitle'),
    {
      confirmButtonText: t('common.delete'),
      cancelButtonText: t('common.cancel'),
      type: 'warning',
    }
  ).then(async () => {
    try {
      await axios.delete(`/admin/users/${user.id}`)
      users.value = users.value.filter(u => u.id !== user.id)
      ElMessage.success(t('admin.deleteSuccess'))
    } catch (error) {
      ElMessage.error(t('admin.deleteFailed'))
    }
  })
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style>
