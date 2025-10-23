<template>
  <div class="data-zone">
    <div class="data-header">
      <h2 class="data-title">Данные для экспорта</h2>
    </div>

    <div class="data-placeholder">
      <div class="table-container" v-if="data.length > 0">
        <div class="placeholder-table">
          <div class="placeholder-row header-row">
            <div class="placeholder-cell" v-for="(key, index) in allKeys" :key="index">
              {{ key }}
            </div>
          </div>

          <div class="placeholder-row" v-for="(row, rowIndex) in flattenedData" :key="rowIndex">
            <div class="placeholder-cell" v-for="(key, keyIndex) in allKeys" :key="keyIndex">
              {{ row[key] || '' }}
            </div>
          </div>
        </div>
      </div>

      <div v-else class="no-data">
        Нет данных для отображения
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  data: {
    type: Array,
    default: () => []
  }
});

const flattenedData = computed(() => {
  if (!props.data.length) return [];

  const flattened = [];
  props.data.forEach(rowArray => {
    rowArray.forEach(obj => {
      flattened.push(obj);
    });
  });
  return flattened;
});

const allKeys = computed(() => {
  if (!flattenedData.value.length) return [];

  const keys = new Set();
  flattenedData.value.forEach(obj => {
    Object.keys(obj).forEach(key => keys.add(key));
  });
  return Array.from(keys);
});
</script>

<style scoped>
.data-zone {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: #f9f9f9;
  border-radius: 0.5rem;
  padding: clamp(1rem, 3vw, 1.25rem);
  height: 100%;
  width: 100%;
}

.data-header {
  margin-bottom: clamp(1rem, 3vw, 1.25rem);
  flex-shrink: 0;
}

.data-title {
  font-size: clamp(1rem, 2.5vw, 1.125rem);
  font-weight: 600;
  color: #333;
  margin: 0 0 clamp(0.25rem, 1vw, 0.5rem) 0;
}

.data-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.table-container {
  flex: 1;
  overflow: auto;
  background: white;
  border-radius: 0.375rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
}

.placeholder-table {
  width: 100%;
  min-width: fit-content;
  display: table;
  border-collapse: collapse;
}

.placeholder-row {
  display: table-row;
  transition: background-color 0.2s ease;
}

.placeholder-row:hover {
  background: #f5f5f5;
}

.placeholder-cell {
  display: table-cell;
  padding: 0.5rem 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  font-size: 0.8125rem;
  color: #666;
  background: #f9f9f9;
  vertical-align: top;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
  min-width: 80px;
}

.header-row .placeholder-cell {
  background: #e6e6e6;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
  z-index: 1;
  border-bottom: 2px solid #d0d0d0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #999;
  background: white;
  border-radius: 0.375rem;
}

.table-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.table-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.table-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .placeholder-cell {
    padding: 0.375rem 0.5rem;
    font-size: 0.75rem;
    max-width: 150px;
    min-width: 60px;
  }

  .data-zone {
    padding: 0.75rem;
  }
}
</style>