<template>
  <div class="export-page">
    <LeftSidebar />
    <MainSidebar ref="mainSidebarRef" />

    <div class="main-content">
      <div class="input-section">
        <div class="input-header">
          <h2 class="section-title">Экспорт файлов</h2>
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
        <div class="output-header">
          <h2 class="section-title">Результаты выполнения</h2>
          <button @click="toggleModal" class="execute-button">
            {{ isModalOpen ? 'Закрыть' : 'Экспортировать' }}
          </button>
        </div>

        <OutputZone v-if="showLogs" ref="outputZoneRef" :logs="logs" />
        <DataZone v-else :data="dataToExport" />
      </div>
    </div>

    <teleport to="body">
      <ExportModal v-if="isModalOpen" :show-logs="showLogs" @update:show-logs="showLogs = $event" @export="exportData"
        @close="closeModal" />
    </teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import LeftSidebar from './LeftSidebar.vue'
import MainSidebar from './MainSidebar.vue'
import InputZone from './InputZone.vue'
import OutputZone from './OutputZone.vue'
import DataZone from './DataZone.vue'
import ExportModal from './ExportModal.vue'
import ApiController from '@/utils/ApiController'
import LogController from '@/utils/LogController'

const isExecuting = ref(false)
const isModalOpen = ref(false)
const showLogs = ref(true)

const logs = ref([])
const dataToExport = ref([])

const inputZoneRef = ref(null)
const outputZoneRef = ref(null)
const mainSidebarRef = ref(null)

const apiController = new ApiController()

function toggleModal() {
  isModalOpen.value = !isModalOpen.value;
}

function closeModal() {
  isModalOpen.value = false;
}

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
  dataToExport.value = []

  try {
    const sql = getSQLFromEditor()
    const servers = getServers()

    if (servers.length === 0) {
      alert('Выберите серверы для выполнения запроса')
      return
    }

    const promises = servers.map(server => {
      const id = logController.addLog('loading', sql, 'Загрузка...', server.name);

      return apiController.query(sql, server)
        .then((res) => {
          if (res.status === 'error') {
            logController.changeLog(id, res.status, sql, res.message)
            return null
          } else {
            logController.changeLog(id, res.status, sql, res.message, res.time)
            return res.data
          }
        })
        .catch((err) => {
          logController.changeLog(id, 'error', sql, err)
          return null
        })
    })

    const results = await Promise.all(promises)
    const validResults = results.filter(result => result !== null)

    dataToExport.value = validResults

    await nextTick()

  } catch (error) {
    console.error('Ошибка выполнения запроса:', error)
  } finally {
    isExecuting.value = false
  }
}

const exportData = async (format) => {
  if (!dataToExport.value || dataToExport.value.length === 0) {
    alert("Нет данных для экспорта")
    return
  }

  let isEmpty = true;
  for (const table of dataToExport.value) {
    if (table && table.length > 0) {
      isEmpty = false;
      break;
    }
  }

  if (isEmpty) {
    alert("Все таблицы пустые");
    return;
  }

  try {
    const res = await apiController.export(dataToExport.value, format);

    const blob = res.data;

    if (blob.size === 0) {
      throw new Error('Получен пустой файл');
    }

    const contentDisposition = res.headers.get('Content-Disposition');
    let filename = 'exported_file';

    if (contentDisposition) {
      const match = contentDisposition.match(/filename="(.+)"/);
      if (match) filename = match[1];
    }

    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
  } catch (error) {
    console.error('Ошибка экспорта:', error)
    alert('Ошибка при экспорте данных')
  }
};
</script>

<style scoped>
.export-page {
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

.input-header,
.output-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: clamp(0.5rem, 2vw, 1rem);
}

.input-section {
  flex: 0 1 40%;
  min-height: 40vh;
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 2vw, 1rem);
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