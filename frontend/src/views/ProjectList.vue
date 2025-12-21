<template>
  <div class="projects">
    <div class="header">
      <h2>{{ $t('project.title') }}</h2>
      <el-button type="primary" @click="dialogVisible = true">{{ $t('project.createProject') }}</el-button>
    </div>

    <el-table :data="projects" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" :label="$t('project.name')" width="180" />
      <el-table-column prop="description" :label="$t('project.description')" />
      <el-table-column prop="owner" :label="$t('project.owner')" width="120" />
      <el-table-column :label="$t('common.actions')" width="250">
        <template #default="scope">
          <el-button size="small" @click="handleEdit(scope.row)">{{ $t('common.edit') }}</el-button>
          <el-button size="small" type="success" @click="runProject(scope.row.id)">{{ $t('project.run') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="$t('project.createProject')">
      <el-form :model="form">
        <el-form-item :label="$t('project.name')" :label-width="100">
          <el-input v-model="form.name" autocomplete="off" />
        </el-form-item>
        <el-form-item :label="$t('project.description')" :label-width="100">
          <el-input v-model="form.description" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="createProject">{{ $t('common.confirm') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted } from 'vue'
// @ts-ignore
import { useI18n } from 'vue-i18n'
import axios from '@/api/axios'
import { ElMessage } from 'element-plus'

const { t } = useI18n()
const projects = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const form = ref({
  name: '',
  description: ''
})

const fetchProjects = async () => {
  loading.value = true
  try {
    const data = await axios.get('/projects/')
    projects.value = data as any
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const createProject = async () => {
  try {
    await axios.post('/projects/', form.value)
    dialogVisible.value = false
    fetchProjects()
    ElMessage.success(t('project.createSuccess'))
  } catch (error) {
    console.error(error)
    ElMessage.error(t('project.createFailed'))
  }
}

const runProject = async (id: number) => {
    try {
        await axios.post('/execution/project', { project_id: id })
        ElMessage.success(t('project.taskQueued'))
    } catch (e) {
        ElMessage.error(t('project.queueFailed'))
        console.error(e)
    }
}

const handleEdit = (row: any) => {
    // Placeholder for edit logic
    console.log('Edit', row)
}

onMounted(() => {
  fetchProjects()
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
