<template>
  <div class="output-zone">
    <div class="header-row">
      <div class="header-cell status-cell"></div>
      <div class="header-cell time-cell">Время</div>
      <div class="header-cell server-cell">Сервер</div>
      <div class="header-cell action-cell">Действие</div>
      <div class="header-cell message-cell">Сообщение</div>
      <div class="header-cell duration-cell">Длительность</div>
    </div>

    <div v-for="log in logs" :key="log.id" class="log-row" :class="log.status">
      <div class="header-cell status-cell">
        <svg v-if="log.status === 'loading'" width="16" height="16" viewBox="0 0 50 50"
          xmlns="http://www.w3.org/2000/svg" class="spin">
          <circle cx="25" cy="25" r="20" fill="none" stroke="#999" stroke-width="5" stroke-linecap="round"
            stroke-dasharray="31.4 31.4" />
        </svg>
        <svg v-else-if="log.status === 'success'" width="16" height="16" viewBox="0 0 24 24" fill="none"
          stroke="#4caf50" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 6L9 17l-5-5" />
        </svg>
        <svg v-else-if="log.status === 'error'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#f44336"
          stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18" />
          <line x1="6" y1="6" x2="18" y2="18" />
        </svg>
        <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2196f3" stroke-width="3"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="6" x2="12" y2="12" />
          <line x1="12" y1="18" x2="12" y2="18" />
        </svg>
      </div>
      <div class="header-cell time-cell">{{ log.time }}</div>
      <div class="header-cell server-cell">{{ log.server || 'servertest' }}</div>
      <div class="header-cell action-cell">{{ log.action }}</div>
      <div class="header-cell message-cell">{{ log.message }}</div>
      <div class="header-cell duration-cell">{{ log.duration }}</div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  logs: {
    type: Array,
    default: () => []
  }
})
</script>

<style scoped>
.output-zone {
  flex: 1;
  width: 100%;
  background-color: #f7f7f7;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  padding: clamp(0.75rem, 3vw, 1rem);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.header-row {
  height: clamp(2rem, 4vh, 2.5rem);
  width: 100%;
  background-color: #d0d0d0;
  display: grid;
  grid-template-columns: 0.1fr 0.8fr 0.8fr 1fr 1.5fr 0.8fr;
  gap: clamp(0.5rem, 2vw, 0.625rem);
  border-radius: 0.375rem;
  align-items: center;
  font-weight: bold;
  color: #333;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
}

.header-cell {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.5rem 0.25rem;
  word-break: break-word;
  text-align: center;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
}

.status-cell {
  justify-content: center;
  min-width: 30px;
}

.time-cell {
  justify-content: center;
  min-width: 80px;
}

.server-cell {
  justify-content: center;
  min-width: 70px;
}

.action-cell {
  justify-content: flex-start;
  min-width: 100px;
}

.message-cell {
  justify-content: flex-start;
  text-align: left;
  min-width: 120px;
  word-break: break-word;
  white-space: normal;
  overflow-wrap: anywhere;
  flex: 1;
}

.duration-cell {
  justify-content: center;
  min-width: 60px;
}

.log-row {
  display: grid;
  grid-template-columns: 0.1fr 0.8fr 0.8fr 1fr 1.5fr 0.8fr;
  gap: clamp(0.5rem, 2vw, 0.625rem);
  align-items: center;
  min-height: clamp(2rem, 4vh, 2.5rem);
  border-bottom: 1px solid #ccc;
  color: #000;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  padding: 0.25rem 0;
}

.log-row .header-cell {
  justify-content: flex-start;
  text-align: left;
  padding: 0.25rem 0.5rem;
}

.log-row .status-cell,
.log-row .time-cell,
.log-row .server-cell,
.log-row .duration-cell {
  justify-content: center;
  text-align: center;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% {
    transform: rotate(360deg);
  }
}

/* Адаптивность для мобильных устройств */
@media (max-width: 768px) {
  .output-zone {
    padding: 0.5rem;
    gap: 0.5rem;
  }

  .header-row {
    grid-template-columns: 0.1fr 0.7fr 0.7fr 0.8fr 1.2fr 0.7fr;
    gap: 0.4rem;
    font-size: 0.7rem;
  }

  .log-row {
    grid-template-columns: 0.1fr 0.7fr 0.7fr 0.8fr 1.2fr 0.7fr;
    gap: 0.4rem;
    font-size: 0.7rem;
  }

  .header-cell {
    padding: 0.25rem 0.125rem;
    font-size: 0.7rem;
  }

  .time-cell {
    min-width: 60px;
  }

  .server-cell {
    min-width: 50px;
  }

  .action-cell {
    min-width: 80px;
  }

  .message-cell {
    min-width: 90px;
  }

  .duration-cell {
    min-width: 50px;
  }
}

@media (max-width: 480px) {
  .header-row {
    grid-template-columns: 0.1fr 0.6fr 0.6fr 0.7fr 1fr 0.6fr;
    gap: 0.3rem;
    font-size: 0.65rem;
  }

  .log-row {
    grid-template-columns: 0.1fr 0.6fr 0.6fr 0.7fr 1fr 0.6fr;
    gap: 0.3rem;
    font-size: 0.65rem;
  }

  .header-cell {
    padding: 0.2rem 0.1rem;
    font-size: 0.65rem;
  }

  .time-cell {
    min-width: 50px;
  }

  .server-cell {
    min-width: 40px;
  }

  .action-cell {
    min-width: 60px;
  }

  .message-cell {
    min-width: 70px;
  }

  .duration-cell {
    min-width: 40px;
  }
}
</style>