<template>
  <div class="import-preview">
    <div class="preview-header">
      <button @click="$emit('back')" class="back-button">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <line x1="19" y1="12" x2="5" y2="12" />
          <polyline points="12,19 5,12 12,5" />
        </svg>
        Назад к выбору файла
      </button>
    </div>

    <div class="inputs-section">
      <div class="input-group">
        <label for="table-name" class="input-label">Название таблицы</label>
        <input id="table-name" :value="tableName" @input="$emit('update:tableName', $event.target.value)" type="text"
          placeholder="Введите название таблицы" class="input-field" />
      </div>

      <div class="input-group">
        <label for="schema-name" class="input-label">Название схемы</label>
        <input id="schema-name" :value="schemaName" @input="$emit('update:schemaName', $event.target.value)" type="text"
          placeholder="Введите название схемы" class="input-field" />
      </div>
    </div>

    <div class="table-section">
      <h3 class="table-title">Предпросмотр таблицы</h3>
      <div class="table-container">
        <table v-if="fileData && fileData.headers" class="preview-table">
          <thead>
            <tr>
              <th v-for="header in fileData.headers.slice(0, 10)" :key="header">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in fileData.rows.slice(0, 20)" :key="index">
              <td v-for="(cell, cellIndex) in row.slice(0, 10)" :key="cellIndex">{{ cell }}</td>
            </tr>
          </tbody>
        </table>
        <div v-else class="no-data">Данные не загружены</div>
      </div>
      <div v-if="fileData && fileData.rows && fileData.rows.length > 20" class="table-footer">
        Первые 20 строк из {{ fileData.rows.length }}.
      </div>
    </div>
    <div class="actions">
      <button class="import-button" @click="handleImport">Импортировать на сервер</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
import ApiController from '@/utils/ApiController'
import LogController from '@/utils/LogController'

const props = defineProps({
  file: {
    type: File,
    default: null
  },
  fileData: {
    type: Object,
    default: null
  },
  tableName: {
    type: String,
    default: ''
  },
  schemaName: {
    type: String,
    default: ''
  },
  servers: {
    type: Array,
    default: () => []
  },
  logController: {
    type: LogController,
    default: null
  }
})

defineEmits(['back', 'update:tableName', 'update:schemaName'])

const api = new ApiController();

async function handleImport() {
  if (!props.tableName.trim()) {
    alert('Введите название таблицы');
    return;
  }

  if (!props.schemaName.trim()) {
    alert('Введите название схемы');
    return;
  }

  if (!props.servers || props.servers.length === 0) {
    alert('Выберите серверы для импорта');
    return;
  }

  try {
    for (const server of props.servers) {
      const logId = props.logController.addLog('loading', 'Импорт', `Импорт на сервер`, server.name);

      api.import(props.file, props.tableName, props.schemaName, server.id)
        .then((data) => {
          if (data.status === 'error') {
            props.logController.changeLog(logId, 'error', 'Импорт', data.message);
          } else {
            props.logController.changeLog(logId, 'success', 'Импорт', data.message, data.time);
          }
        })
        .catch(err => {
          props.logController.changeLog(logId, 'error', 'Импорт', err.message || 'Ошибка импорта');
        });
    }
  } catch (e) {
    console.error('Ошибка импорта', e);
  }
}
</script>

<style scoped>
.import-preview {
  display: flex;
  flex-direction: column;
  height: 100%;
  gap: clamp(1rem, 3vw, 1.25rem);
}

.preview-header {
  display: flex;
  align-items: center;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: clamp(0.5rem, 2vw, 0.75rem) clamp(1rem, 3vw, 1rem);
  background: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 0.5rem;
  color: #333;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: #e6e6e6;
  border-color: #1890ff;
}

.inputs-section {
  display: flex;
  flex-direction: column;
  gap: clamp(0.75rem, 2vw, 1rem);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.input-label {
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  font-weight: 500;
  color: #333;
}

.input-field {
  padding: clamp(0.5rem, 2vw, 0.75rem);
  border: 1px solid #d9d9d9;
  border-radius: 0.375rem;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  transition: border-color 0.2s ease;
}

.input-field:focus {
  outline: none;
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
}

.table-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.table-title {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  font-weight: 600;
  color: #333;
  margin-bottom: clamp(0.5rem, 2vw, 0.75rem);
}

.table-container {
  flex: 1;
  overflow-y: auto;
  border: 1px solid #d9d9d9;
  border-radius: 0.5rem;
  background: white;
}

.preview-table {
  width: 100%;
  border-collapse: collapse;
  font-size: clamp(0.75rem, 1.5vw, 0.8125rem);
}

.preview-table th,
.preview-table td {
  padding: clamp(0.5rem, 1.5vw, 0.75rem);
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 15rem;
}

.preview-table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
}

.preview-table tr:hover {
  background: #f9f9f9;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
}

.table-footer {
  font-size: clamp(0.75rem, 1.5vw, 0.8125rem);
  color: #666;
  text-align: center;
  padding-top: 0.5rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
}

.import-button {
  padding: clamp(0.75rem, 2vw, 0.75rem) clamp(1.25rem, 3vw, 1.25rem);
  background-color: #52c41a;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.import-button:hover {
  background-color: #73d13d;
}
</style>