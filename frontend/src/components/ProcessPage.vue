<template>
  <div class="process-page">
    <LeftSidebar />

    <MainSidebar ref="mainSidebarRef" />

    <div class="main-content">
      <div class="input-section">
        <div class="input-header">
          <h2 class="section-title">SQL Редактор</h2>
          <div class="execute-button-container">
            <button @click="executeQuery" :disabled="isExecuting" class="execute-button">
              <svg v-if="isExecuting" width="16" height="16" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg"
                class="spin">
                <circle cx="25" cy="25" r="20" fill="none" stroke="white" stroke-width="5" stroke-linecap="round"
                  stroke-dasharray="31.4 31.4" />
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"
                stroke-linecap="round" stroke-linejoin="round">
                <polygon points="5,3 19,12 5,21" />
              </svg>
              {{ isExecuting ? 'Выполняется...' : 'Выполнить' }}
            </button>
          </div>
        </div>
        <div class="input-container">
          <InputZone ref="inputZoneRef" />
        </div>
      </div>

      <div class="output-section">
        <h2 class="section-title">Результаты выполнения</h2>
        <OutputZone ref="outputZoneRef" :logs="logs" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import LeftSidebar from './LeftSidebar.vue'
import MainSidebar from './MainSidebar.vue'
import InputZone from './InputZone.vue'
import OutputZone from './OutputZone.vue'
import ApiController from '@/utils/ApiController'
import LogController from '@/utils/LogController'

const inputZoneRef = ref(null)
const mainSidebarRef = ref(null)
const outputZoneRef = ref(null)
const isExecuting = ref(false)
const logs = ref([])

const apiController = new ApiController()

const getSQLFromEditor = () => {
  if (inputZoneRef.value && inputZoneRef.value.getSQL) {
    return inputZoneRef.value.getSQL()
  }
  return ''
}

const getServers = () => {
  if (mainSidebarRef.value && mainSidebarRef.value.getSelectedServers) {
    return mainSidebarRef.value.getSelectedServers()
  }

  return []
}

let logController;
onMounted(() => {
  logController = new LogController(logs)
})

const executeQuery = async () => {
  isExecuting.value = true

  try {
    const sql = getSQLFromEditor()
    const servers = getServers()

    for (const server of servers) {
      const id = logController.addLog('loading', sql, 'Загрузка...', server.name);
      apiController.query(sql, server)
        .then((data) => {
          if (data.status == 'error') {
            logController.changeLog(id, data.status, sql, data.message)
          } else {
            logController.changeLog(id, data.status, sql, data.message, data.time)
          }
          return
        })
        .catch((err) => {
          logController.changeLog(id, 'error', sql, err)
          return
        });
    }

  } catch (error) {
    console.error('Ошибка выполнения SQL:', error)
  } finally {
    isExecuting.value = false
  }
}
</script>

<style scoped>
.process-page {
  display: flex;
  height: 100vh;
  background-color: #ffffff;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: clamp(1rem, 4vw, 1.5rem);
  gap: clamp(1rem, 4vw, 1.5rem);
  overflow: hidden;
}

.section-title {
  margin: 0 0 clamp(0.5rem, 2vw, 1rem) 0;
  font-size: clamp(1.125rem, 3vw, 1.25rem);
  font-weight: 600;
  color: #333;
}

.input-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: clamp(0.5rem, 2vw, 1rem);
}

.input-section {
  flex: 0 1 40%;
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 2vw, 1rem);
  min-height: 40vh;
  margin-bottom: 30px;
}

.input-container {
  display: flex;
  align-items: flex-start;
  flex: 1;
  min-height: 20vh;
}

.execute-button-container {
  display: flex;
  justify-content: flex-start;
}

.execute-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: clamp(0.75rem, 2vw, 0.75rem) clamp(1.25rem, 3vw, 1.25rem);
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: clamp(8rem, 10vw, 9rem);
  justify-content: center;
}

.execute-button:hover:not(:disabled) {
  background-color: #40a9ff;
  transform: translateY(-1px);
  box-shadow: 0 0.25rem 0.75rem rgba(24, 144, 255, 0.3);
}

.execute-button:active:not(:disabled) {
  transform: translateY(0);
}

.execute-button:disabled {
  background-color: #d9d9d9;
  cursor: not-allowed;
}

.output-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  gap: clamp(0.5rem, 2vw, 1rem);
  padding-right: clamp(1rem, 4vw, 1.5rem);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}
</style>