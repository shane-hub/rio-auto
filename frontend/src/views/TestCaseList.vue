<template>
  <div class="test-case-list">
    <div class="header">
      <h2>{{ $t('testCase.title') }}</h2>
      <el-button type="primary" @click="openCreateDialog">{{ $t('testCase.createTestCase') }}</el-button>
    </div>

    <el-table :data="testCases" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" :label="$t('testCase.id')" width="80" />
      <el-table-column prop="name" :label="$t('testCase.name')" />
      <el-table-column prop="type" :label="$t('testCase.type')" width="120">
        <template #default="{ row }">
          <el-tag>{{ row.type }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="project_id" :label="$t('testCase.projectId')" width="100" />
      <el-table-column :label="$t('common.actions')" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="editCase(row)">{{ $t('common.edit') }}</el-button>
          <el-button size="small" type="danger" @click="deleteCase(row.id)">{{ $t('common.delete') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Create/Edit Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? $t('testCase.editTestCase') : $t('testCase.createTestCase')"
      width="60%"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item :label="$t('project.title')" required>
          <el-select v-model="form.project_id" :placeholder="$t('testCase.selectProject')">
             <el-option
                v-for="p in projects"
                :key="p.id"
                :label="p.name"
                :value="p.id"
             />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('testCase.name')" required>
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item :label="$t('testCase.type')" required>
          <el-select v-model="form.type" :placeholder="$t('testCase.selectType')">
            <el-option label="API" value="api" />
            <el-option label="UI" value="ui" />
            <el-option label="Performance" value="performance" />
          </el-select>
        </el-form-item>
        
        <!-- API Specific Fields -->
        <template v-if="form.type === 'api'">
           <el-divider>{{ $t('testCase.apiRequestDetails') }}</el-divider>
           <el-form-item :label="$t('testCase.method')">
             <el-select v-model="form.data.method">
               <el-option label="GET" value="GET" />
               <el-option label="POST" value="POST" />
               <el-option label="PUT" value="PUT" />
               <el-option label="DELETE" value="DELETE" />
             </el-select>
           </el-form-item>
           <el-form-item :label="$t('testCase.url')">
             <el-input v-model="form.data.url" placeholder="http://api.example.com/v1/resource" />
           </el-form-item>
           <el-form-item :label="$t('testCase.headers')">
             <el-input type="textarea" v-model="headersJson" placeholder='{"Content-Type": "application/json"}' />
           </el-form-item>
           <el-form-item :label="$t('testCase.body')">
             <el-input type="textarea" v-model="bodyJson" :rows="4" placeholder='{"key": "value"}' />
           </el-form-item>
        </template>

        <!-- UI Specific Fields -->
        <template v-if="form.type === 'ui'">
            <el-divider>{{ $t('testCase.uiTestDetails') }}</el-divider>
            <el-form-item :label="$t('testCase.startUrl')">
                <el-input v-model="form.data.url" />
            </el-form-item>
            <!-- Placeholder for complex script editor -->
            <el-alert :title="$t('testCase.complexScriptAlert')" type="info" :closable="false" />
        </template>

      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">{{ $t('common.cancel') }}</el-button>
          <el-button type="primary" @click="saveCase">{{ $t('common.confirm') }}</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from '@/api/axios'

const { t } = useI18n()
const testCases = ref<any[]>([])
const projects = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)

const form = ref<any>({
  id: null,
  project_id: null,
  name: '',
  type: 'api',
  data: {
      method: 'GET',
      url: '',
      headers: {},
      body: null
  }
})

// Helpers for JSON fields
const headersJson = ref('{}')
const bodyJson = ref('{}')

watch(() => form.value.data.headers, () => {
    // Only update string if object changed (avoid loop if parsing failed)
    // Simplified: we sync from string to object on save usually, but here we do 2-way with care
    // For now, let's just init string on open
})

const fetchCases = async () => {
  loading.value = true
  try {
    // Assuming we have an endpoint to list all cases or we need to iterate projects
    // For now, let's assume GET /test-cases/ (we need to create this endpoint or filter by project)
    // Actually the backend has `GET /test-cases/?skip=0&limit=100`
    const res = await axios.get('/test-cases/')
    testCases.value = res as any
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const fetchProjects = async () => {
    const res = await axios.get('/projects/')
    projects.value = res as any
}

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    id: null,
    project_id: projects.value.length > 0 ? projects.value[0].id : null,
    name: '',
    type: 'api',
    data: { method: 'GET', url: '', headers: {}, body: null }
  }
  headersJson.value = '{}'
  bodyJson.value = '{}'
  dialogVisible.value = true
}

const editCase = (row: any) => {
  isEdit.value = true
  // Deep copy to avoid modifying row directly
  form.value = JSON.parse(JSON.stringify(row))
  
  // Parse data for UI
  if (!form.value.data) form.value.data = {}
  
  headersJson.value = JSON.stringify(form.value.data.headers || {}, null, 2)
  bodyJson.value = JSON.stringify(form.value.data.body || {}, null, 2)
  
  dialogVisible.value = true
}

const saveCase = async () => {
  try {
    // Parse JSON fields
    try {
        form.value.data.headers = JSON.parse(headersJson.value)
    } catch (e) {
        form.value.data.headers = {}
    }
    
    try {
        form.value.data.body = JSON.parse(bodyJson.value)
    } catch (e) {
        form.value.data.body = null
    }

    if (isEdit.value) {
      await axios.put(`/test-cases/${form.value.id}`, form.value)
      ElMessage.success(t('common.updated'))
    } else {
      await axios.post('/test-cases/', form.value)
      ElMessage.success(t('common.created'))
    }
    dialogVisible.value = false
    fetchCases()
  } catch (e) {
    ElMessage.error(t('common.fail'))
    console.error(e)
  }
}

const deleteCase = async (id: number) => {
  if (!confirm(t('common.confirmDelete'))) return
  try {
    await axios.delete(`/test-cases/${id}`)
    ElMessage.success(t('common.deleted'))
    fetchCases()
  } catch (e) {
    ElMessage.error(t('common.fail'))
  }
}

onMounted(() => {
  fetchCases()
  fetchProjects()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
