<template>
  <div class="import-page">
    <LeftSidebar :currentPage="'import'" @navigate="(v) => $emit('navigate', v)" />
    <MainSidebar ref="mainSidebarRef" />

    <div class="main-content">
      <div v-if="!isPreviewVisible" class="input-section">
        <div class="input-header">
          <h2 class="section-title">Импорт файлов</h2>
          <div class="execute-button-container">
            <button @click="loadPreview" :disabled="isProcessing || !hasFile" class="execute-button">
              {{ isProcessing ? 'Обрабатывается...' : 'Обработать файл' }}
            </button>
          </div>
        </div>

        <div class="input-container">
          <ImportZone @file-selected="onFileSelected" @file-removed="onFileRemoved" />
        </div>
      </div>

      <ImportPreview v-if="isPreviewVisible" :file-data="filePreview" :file="selectedFile" :servers="getServers()"
        :log-controller="logController" v-model:table-name="tableName" v-model:schema-name="schemaName"
        @back="resetToFileSelect" />

      <div class="output-section">
        <h2 class="section-title">Результаты</h2>
        <OutputZone :logs="logs" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import LeftSidebar from './LeftSidebar.vue';
import MainSidebar from './MainSidebar.vue';
import ImportZone from './ImportZone.vue';
import ImportPreview from './ImportTablePreview.vue';
import OutputZone from './OutputZone.vue';
import ApiController from '@/utils/ApiController'
import LogController from '@/utils/LogController'

const api = new ApiController();

const isProcessing = ref(false);
const hasFile = ref(false);
const selectedFile = ref(null);
const isPreviewVisible = ref(false);

const mainSidebarRef = ref(null)

const tableName = ref('');
const schemaName = ref('');
const filePreview = ref(null);
const logs = ref([]);
const logController = ref(null);

onMounted(() => {
  logController.value = new LogController(logs);
});

const getServers = () => {
  if (mainSidebarRef.value && mainSidebarRef.value.getSelectedServers) {
    return mainSidebarRef.value.getSelectedServers()
  }
  return []
}

function onFileSelected(file) {
  selectedFile.value = file;
  hasFile.value = true;
}

function onFileRemoved() {
  selectedFile.value = null;
  hasFile.value = false;
}

async function loadPreview() {
  if (!selectedFile.value) return;
  isProcessing.value = true;

  try {
    const preview = await api.previewImportFile(selectedFile.value);
    filePreview.value = preview;
    isPreviewVisible.value = true;

    if (logController.value) {
      logController.value.addLog('success', 'Предпросмотр', `Файл "${selectedFile.value.name}" успешно прочитан`);
    }
  } catch (e) {
    if (logController.value) {
      logController.value.addLog('error', 'Ошибка', e?.message ?? 'Не удалось загрузить предпросмотр');
    }
  } finally {
    isProcessing.value = false;
  }
}

function resetToFileSelect() {
  isPreviewVisible.value = false;
}
</script>

<style scoped>
.import-page {
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
  min-height: 40vh;
  display: flex;
  flex-direction: column;
  gap: clamp(0.5rem, 2vw, 1rem);
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
  min-width: clamp(10rem, 12vw, 10rem);
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