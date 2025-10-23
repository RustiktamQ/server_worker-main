<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content" role="dialog" aria-modal="true">
      <div class="export-options">
        <div v-for="option in exportOptions" :key="option.text" @click="sendExport(option.tag)" class="export-option">
          <div class="icon" v-html="option.svg"></div>
          <span class="label">{{ option.text }}</span>
        </div>
      </div>

      <div class="divider"></div>

      <div class="log-toggle">
        <svg class="icon eye-icon" viewBox="0 0 24 24" fill="none" stroke="#666" stroke-width="2" stroke-linecap="round"
          stroke-linejoin="round">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        </svg>
        <label class="toggle-label">
          Показать логи
          <input type="checkbox" :checked="props.showLogs" @change="$emit('update:show-logs', $event.target.checked)" />
          <span class="slider"></span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  showLogs: {
    type: Boolean,
    default: false
  }
});

const emits = defineEmits(['close', 'export', 'update:show-logs']);

const close = () => emits('close');

const exportOptions = [
  {
    tag: 'excel',
    text: 'Экспортировать в Excel',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none">
            <path d="M10.4142 0.585787C9.63317 -0.195261 8.36684 -0.195264 7.58579 0.585787L3.29289 4.87868C2.90237 5.2692 2.90237 5.90237 3.29289 6.29289C3.68342 6.68342 4.31658 6.68342 4.70711 6.29289L8 3V12.5858C8 13.1381 8.44771 13.5858 9 13.5858C9.55229 13.5858 10 13.1381 10 12.5858V3L13.2929 6.29289C13.6834 6.68342 14.3166 6.68342 14.7071 6.29289C15.0976 5.90237 15.0976 5.2692 14.7071 4.87868L10.4142 0.585787Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1 11.5858C1.55228 11.5858 2 12.0335 2 12.5858V13.5858C2 15.2426 3.34315 16.5858 5 16.5858H13C14.6569 16.5858 16 15.2426 16 13.5858V12.5858C16 12.0335 16.4477 11.5858 17 11.5858C17.5523 11.5858 18 12.0335 18 12.5858V13.5858C18 16.3472 15.7614 18.5858 13 18.5858H5C2.23858 18.5858 0 16.3472 0 13.5858V12.5858C0 12.0335 0.447715 11.5858 1 11.5858Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>`
  },
  {
    tag: 'json',
    text: 'Экспортировать в JSON',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none">
            <path d="M10.4142 0.585787C9.63317 -0.195261 8.36684 -0.195264 7.58579 0.585787L3.29289 4.87868C2.90237 5.2692 2.90237 5.90237 3.29289 6.29289C3.68342 6.68342 4.31658 6.68342 4.70711 6.29289L8 3V12.5858C8 13.1381 8.44771 13.5858 9 13.5858C9.55229 13.5858 10 13.1381 10 12.5858V3L13.2929 6.29289C13.6834 6.68342 14.3166 6.68342 14.7071 6.29289C15.0976 5.90237 15.0976 5.2692 14.7071 4.87868L10.4142 0.585787Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1 11.5858C1.55228 11.5858 2 12.0335 2 12.5858V13.5858C2 15.2426 3.34315 16.5858 5 16.5858H13C14.6569 16.5858 16 15.2426 16 13.5858V12.5858C16 12.0335 16.4477 11.5858 17 11.5858C17.5523 11.5858 18 12.0335 18 12.5858V13.5858C18 16.3472 15.7614 18.5858 13 18.5858H5C2.23858 18.5858 0 16.3472 0 13.5858V12.5858C0 12.0335 0.447715 11.5858 1 11.5858Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>`
  },
  {
    tag: 'csv',
    text: 'Экспортировать в CSV',
    svg: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none">
            <path d="M10.4142 0.585787C9.63317 -0.195261 8.36684 -0.195264 7.58579 0.585787L3.29289 4.87868C2.90237 5.2692 2.90237 5.90237 3.29289 6.29289C3.68342 6.68342 4.31658 6.68342 4.70711 6.29289L8 3V12.5858C8 13.1381 8.44771 13.5858 9 13.5858C9.55229 13.5858 10 13.1381 10 12.5858V3L13.2929 6.29289C13.6834 6.68342 14.3166 6.68342 14.7071 6.29289C15.0976 5.90237 15.0976 5.2692 14.7071 4.87868L10.4142 0.585787Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1 11.5858C1.55228 11.5858 2 12.0335 2 12.5858V13.5858C2 15.2426 3.34315 16.5858 5 16.5858H13C14.6569 16.5858 16 15.2426 16 13.5858V12.5858C16 12.0335 16.4477 11.5858 17 11.5858C17.5523 11.5858 18 12.0335 18 12.5858V13.5858C18 16.3472 15.7614 18.5858 13 18.5858H5C2.23858 18.5858 0 16.3472 0 13.5858V12.5858C0 12.0335 0.447715 11.5858 1 11.5858Z" stroke="#666" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>`
  }
];

function sendExport(tag) {
  emits('export', tag)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-container {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  width: 280px;
  height: 169px;
  background-color: #fff;
  border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.export-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.export-option {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #666;
  font-size: 13px;
  font-weight: 500;
  padding: 6px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  user-select: none;
}

.export-option:hover {
  background-color: #f0f0f0;
}

.icon {
  width: 18px;
  height: 18px;
  stroke: #666;
  flex-shrink: 0;
}

.divider {
  height: 1px;
  background-color: #ddd;
  margin: 8px 0;
  width: 100%;
}

.log-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  padding: 6px;
}

.eye-icon {
  width: 20px;
  height: 20px;
  stroke: #666;
  flex-shrink: 0;
}

.toggle-label {
  position: relative;
  display: inline-block;
  cursor: pointer;
  user-select: none;
}

.toggle-label input[type="checkbox"] {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.slider {
  position: absolute;
  top: 50%;
  left: 100px;
  transform: translateY(-50%);
  width: 36px;
  height: 20px;
  background-color: #ccc;
  border-radius: 12px;
  transition: 0.4s;
}

.slider::before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  border-radius: 50%;
  transition: 0.4s;
}

.toggle-label input:checked+.slider {
  background-color: #1890ff;
}

.toggle-label input:checked+.slider::before {
  transform: translateX(16px);
}
</style>
