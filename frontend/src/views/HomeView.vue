<template>
  <div class="dashboard">
    <h1>{{ $t('dashboard.title') }}</h1>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>{{ $t('dashboard.totalProjects') }}</template>
          <div class="card-value">12</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>{{ $t('dashboard.testCases') }}</template>
          <div class="card-value">150</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>{{ $t('dashboard.tasksRunning') }}</template>
          <div class="card-value">2</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <template #header>{{ $t('dashboard.passRate') }}</template>
          <div class="card-value success">98%</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.card-value {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}
.success {
  color: #67c23a;
}
</style>
