<template>
  <div class="report-list">
    <div class="header">
      <h2>{{ $t('report.title') }}</h2>
      <el-button type="primary" @click="fetchReports">{{ $t('report.refresh') }}</el-button>
    </div>

    <el-table :data="reports" style="width: 100%" v-loading="loading">
      <el-table-column prop="id" :label="$t('report.id')" width="80" />
      <el-table-column prop="task_id" :label="$t('report.taskId')" width="100" />
      <el-table-column :label="$t('report.summary')" width="200">
        <template #default="{ row }">
          <el-tag type="success">{{ $t('report.pass') }}: {{ row.passed }}</el-tag>
          <el-tag type="danger" style="margin-left: 5px">{{ $t('report.fail') }}: {{ row.failed }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="duration" :label="$t('report.duration')" width="120" />
      <el-table-column prop="created_at" :label="$t('report.generatedAt')" />
      <el-table-column :label="$t('common.actions')">
        <template #default="{ row }">
            <el-button size="small" @click="viewDetails(row)">{{ $t('report.details') }}</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
// @ts-ignore
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from '@/api/axios'
import { ElMessage } from 'element-plus'

const { t } = useI18n()
const reports = ref<any[]>([])
const loading = ref(false)

const fetchReports = async () => {
  loading.value = true
  try {
    const res = await axios.get('/execution/reports')
    reports.value = res as any
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const viewDetails = (row: any) => {
    // Placeholder for details view
    console.log(row)
    ElMessage.info(t('common.notImplemented') + ': ' + t('report.details'))
}

onMounted(() => {
  fetchReports()
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
