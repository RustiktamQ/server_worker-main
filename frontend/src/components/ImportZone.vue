<template>
  <div ref="root" :class="[
    'import-zone',
    {
      'drag-over': isDragOver,
      'has-file': selectedFile,
      'error': hasError
    }
  ]" @drop="handleDrop" @dragover="handleDragOver" @dragenter="handleDragEnter" @dragleave="handleDragLeave"
    @click="triggerFileInput">
    <input ref="fileInput" type="file" accept=".xlsx,.xls,.csv,.json" @change="handleFileSelect" class="hidden-input" />

    <div class="import-content">
      <div class="import-icon">
        <svg v-if="!selectedFile" width="clamp(2.5rem, 6vw, 3rem)" height="clamp(2.5rem, 6vw, 3rem)" viewBox="0 0 24 24"
          fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14,2 14,8 20,8" />
          <line x1="12" y1="18" x2="12" y2="12" />
          <polyline points="9,15 12,12 15,15" />
        </svg>

        <svg v-else width="clamp(2.5rem, 6vw, 3rem)" height="clamp(2.5rem, 6vw, 3rem)" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14,2 14,8 20,8" />
          <path d="M9 15l2 2 4-4" />
        </svg>
      </div>

      <div class="import-text">
        <h3 v-if="!selectedFile" class="primary-text">
          {{ isDragOver ? 'Отпустите файл' : 'Перенесите файл' }}
        </h3>
        <h3 v-else class="primary-text success">
          Файл выбран
        </h3>

        <p v-if="!selectedFile" class="secondary-text">
          или <span class="click-text">нажмите для выбора</span>
        </p>
        <p v-else class="secondary-text">
          {{ selectedFile.name }}
        </p>
      </div>

      <div v-if="selectedFile" class="file-info">
        <div class="file-details">
          <span class="file-size">{{ formatFileSize(selectedFile.size) }}</span>
          <span class="file-type">{{ getFileType(selectedFile.name) }}</span>
        </div>
        <button @click.stop="removeFile" class="remove-btn">
          <svg width="clamp(1rem, 3vw, 1rem)" height="clamp(1rem, 3vw, 1rem)" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <div v-if="!selectedFile" class="supported-formats">
        <small>Поддерживаемые форматы: Excel (.xlsx, .xls), CSV, JSON</small>
      </div>

      <div v-if="hasError" class="error-message">
        <svg width="clamp(1rem, 3vw, 1rem)" height="clamp(1rem, 3vw, 1rem)" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'
import config from "@/config"

const emit = defineEmits(['file-selected', 'file-removed'])

const root = ref(null)
const fileInput = ref(null)

const isDragOver = ref(false)
const selectedFile = ref(null)
const hasError = ref(false)
const errorMessage = ref('')

const supportedTypes = [
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
  'text/csv',
  'application/csv',
  'application/json',
  'text/json',
]

function handleDragOver(e) {
  e.preventDefault();
  isDragOver.value = true;
}

function handleDragEnter(e) {
  e.preventDefault();
  isDragOver.value = true;
}

function handleDragLeave(e) {
  e.preventDefault()
  const next = e.relatedTarget
  if (!root.value || !next || !root.value.contains(next)) {
    isDragOver.value = false
  }
}

function handleDrop(e) {
  e.preventDefault()
  isDragOver.value = false
  const files = Array.from(e.dataTransfer?.files || [])
  if (files.length > 0) processFile(files[0])
}

function triggerFileInput() {
  if (!selectedFile.value) fileInput.value?.click()
}

function handleFileSelect(e) {
  const file = e.target.files?.[0]
  if (file) processFile(file)
}

function processFile(file) {
  clearError()

  if (!isValidFileType(file)) {
    showError('Неподдерживаемый тип файла. Выберите Excel (.xlsx, .xls) или CSV, JSON файл.')
    return
  }

  if (file.size > config.IMPORT_MAX_FILE_SIZE * 1024 * 1024) {
    showError(`Файл слишком большой. Максимальный размер: ${config.IMPORT_MAX_FILE_SIZE}MB.`)
    return
  }

  selectedFile.value = file
  emit('file-selected', file)
}

function isValidFileType(file) {
  if (supportedTypes.includes(file.type)) return true
  const extension = file.name.toLowerCase().split('.').pop()
  return ['xlsx', 'xls', 'csv', 'json'].includes(extension)
}

function removeFile() {
  selectedFile.value = null
  clearError()
  if (fileInput.value) fileInput.value.value = ''
  emit('file-removed')
}

function showError(message) {
  hasError.value = true
  errorMessage.value = message
  setTimeout(() => clearError(), 5000)
}

function clearError() {
  hasError.value = false
  errorMessage.value = ''
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`
}

function getFileType(filename) {
  const extension = filename.toLowerCase().split('.').pop()
  const types = { xlsx: 'Excel', xls: 'Excel', csv: 'CSV', json: 'JSON' }
  return types[extension] || 'Unknown'
}
</script>

<style scoped>
.import-zone {
  width: 100%;
  min-height: clamp(16rem, 30vh, 18rem);
  background-color: #fafafa;
  border: 2px dashed #d9d9d9;
  border-radius: clamp(0.75rem, 2vw, 0.75rem);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.import-zone:hover {
  border-color: #1890ff;
  background-color: #f6f9ff;
}

.import-zone.drag-over {
  border-color: #1890ff;
  background-color: #e6f7ff;
  transform: scale(1.02);
}

.import-zone.has-file {
  border-color: #52c41a;
  background-color: #f6ffed;
  cursor: default;
}

.import-zone.error {
  border-color: #ff4d4f;
  background-color: #fff2f0;
}

.hidden-input {
  display: none;
}

.import-content {
  text-align: center;
  padding: clamp(1rem, 4vw, 1.25rem);
  width: 100%;
}

.import-icon {
  color: #8c8c8c;
  margin-bottom: clamp(0.75rem, 3vw, 1rem);
  transition: all 0.3s ease;
}

.import-zone:hover .import-icon {
  color: #1890ff;
  transform: translateY(-2px);
}

.import-zone.has-file .import-icon {
  color: #52c41a;
}

.import-zone.error .import-icon {
  color: #ff4d4f;
}

.import-text {
  margin-bottom: clamp(0.75rem, 3vw, 1rem);
}

.primary-text {
  font-size: clamp(1rem, 3vw, 1.125rem);
  font-weight: 600;
  color: #262626;
  margin: 0 0 clamp(0.5rem, 2vw, 0.5rem) 0;
  transition: color 0.3s ease;
}

.primary-text.success {
  color: #52c41a;
}

.secondary-text {
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  color: #8c8c8c;
  margin: 0;
  line-height: 1.4;
}

.click-text {
  color: #1890ff;
  font-weight: 500;
}

.file-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.75rem, 2vw, 0.75rem);
  margin-bottom: clamp(0.75rem, 2vw, 0.75rem);
  padding: clamp(0.5rem, 2vw, 0.5rem) clamp(1rem, 3vw, 1rem);
  background: rgba(82, 196, 26, 0.1);
  border-radius: 0.5rem;
}

.file-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.file-size {
  font-size: clamp(0.75rem, 2vw, 0.75rem);
  color: #52c41a;
  font-weight: 500;
}

.file-type {
  font-size: clamp(0.625rem, 1.5vw, 0.625rem);
  color: #8c8c8c;
  background: #f0f0f0;
  padding: clamp(0.125rem, 0.5vw, 0.125rem) clamp(0.375rem, 1vw, 0.375rem);
  border-radius: 0.25rem;
}

.remove-btn {
  background: none;
  border: none;
  color: #ff4d4f;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover {
  background: rgba(255, 77, 79, 0.1);
  transform: scale(1.1);
}

.supported-formats {
  color: #bfbfbf;
  font-size: clamp(0.75rem, 2vw, 0.75rem);
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #ff4d4f;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  font-weight: 500;
  background: rgba(255, 77, 79, 0.1);
  padding: clamp(0.5rem, 2vw, 0.5rem) clamp(0.75rem, 2vw, 0.75rem);
  border-radius: 0.5rem;
  margin-top: 0.5rem;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.05);
  }

  100% {
    transform: scale(1);
  }
}

.import-zone.drag-over {
  animation: pulse 1s infinite;
}
</style>