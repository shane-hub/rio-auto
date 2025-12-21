<template>
  <div class="task-list">
    <div class="header">
      <h2>{{ $t('task.title') }}</h2>
      <el-button type="primary" @click="fetchTasks">{{ $t('task.refresh') }}</el-button>
    </div>

    <el-table :data="tasks" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" :label="$t('task.id')" width="80" />
      <el-table-column prop="project_id" :label="$t('task.projectId')" width="100" />
      <el-table-column prop="status" :label="$t('task.status')" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" :label="$t('task.createdAt')" />
      <el-table-column prop="completed_at" :label="$t('task.completedAt')" />
    </el-table>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted } from 'vue'
import axios from '@/api/axios'

const tasks = ref<any[]>([])
const loading = ref(false)

const fetchTasks = async () => {
  loading.value = true
  try {
    const res = await axios.get('/execution/')
    tasks.value = res as any
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'completed': return 'success'
    case 'failed': return 'danger'
    case 'running': return 'primary'
    default: return 'info'
  }
}

onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
