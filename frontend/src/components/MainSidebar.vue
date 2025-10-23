<template>
    <transition name="sidebar" mode="out-in">
        <div v-if="!sidebarCollapsed" key="expanded" class="sidebar">
            <div class="header">
                <div class="header-content">
                    <div class="title" @click="getSelectedServers">Сервера</div>
                    <div class="icon-button" role="button" tabindex="0" @click="toggleSidebar"
                        @keydown.enter="toggleSidebar">
                        <svg v-if="!sidebarCollapsed" class="closeSidebar" xmlns="http://www.w3.org/2000/svg" width="15"
                            height="16" viewBox="0 0 15 16" fill="none">
                            <path
                                d="M1 0C1.55228 0 2 0.447715 2 1V15C2 15.5523 1.55228 16 1 16C0.447715 16 0 15.5523 0 15V1C0 0.447715 0.447715 0 1 0Z"
                                fill="#999999" />
                            <path
                                d="M7.41422 7L9.70711 4.70711C10.0976 4.31658 10.0976 3.68342 9.70711 3.29289C9.31658 2.90237 8.68342 2.90237 8.29289 3.29289L5 6.58579C4.21895 7.36684 4.21895 8.63317 5 9.41421L8.29289 12.7071C8.68342 13.0976 9.31658 13.0976 9.70711 12.7071C10.0976 12.3166 10.0976 11.6834 9.70711 11.2929L7.41421 9H14C14.5523 9 15 8.55228 15 8C15 7.44772 14.5523 7 14 7H7.41422Z"
                                fill="#999999" />
                        </svg>
                    </div>
                </div>
            </div>
            <div class="search-container">
                <div class="search-box">
                    <div class="search-icon">
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path fill-rule="evenodd" clip-rule="evenodd"
                                d="M6 0C2.68629 0 0 2.68629 0 6C0 9.31371 2.68629 12 6 12C7.29583 12 8.49571 11.5892 9.47653 10.8908L12.2929 13.7071C12.6834 14.0976 13.3166 14.0976 13.7071 13.7071C14.0976 13.3166 14.0976 12.6834 13.7071 12.2929L10.8907 9.47654C11.5892 8.49572 12 7.29583 12 6C12 2.68629 9.31371 0 6 0ZM2 6C2 3.79086 3.79086 2 6 2C8.20914 2 10 3.79086 10 6C10 8.20914 8.20914 10 6 10C3.79086 10 2 8.20914 2 6Z"
                                fill="#999999" />
                        </svg>
                    </div>
                    <input type="text" placeholder="Поиск..." class="search-input" v-model="searchQuery" />
                </div>
            </div>
            <div class="select-all-container">
                <div class="select-all-content">
                    <div class="select-all-label">Выбрать всё</div>
                    <input type="checkbox" class="checkbox" :checked="isAllSelected"
                        @change="toggleSelectAll($event.target.checked)" />
                </div>
            </div>
            <div class="servers-container">
                <div v-for="server in filteredServers" :key="server.id"
                    :class="['server-item', { selected: selectedServerIds.includes(server.id) }]"
                    @click="toggleSelectServer(server.id)" tabindex="0" @keydown.enter="toggleSelectServer(server.id)">
                    <div class="server-name">{{ server.name }}#</div>
                    <div class="server-port">{{ server.host }}:{{ server.port }}</div>
                </div>
            </div>
        </div>

        <div v-else key="collapsed" class="sidebar-collapsed">
            <div class="header-collapsed">
                <div class="header-content-collapsed">
                    <div class="icon-button" role="button" tabindex="0" @click="toggleSidebar"
                        @keydown.enter="toggleSidebar">
                        <svg xmlns="http://www.w3.org/2000/svg" width="15" height="16" viewBox="0 0 15 16" fill="none">
                            <path
                                d="M15 0C14.4477 0 14 0.447715 14 1V15C14 15.5523 14.4477 16 15 16C15.5523 16 16 15.5523 16 15V1C16 0.447715 15.5523 0 15 0Z"
                                fill="#999999"></path>
                            <path
                                d="M8.58578 7L6.29289 4.70711C5.90237 4.31658 5.90237 3.68342 6.29289 3.29289C6.68342 2.90237 7.31658 2.90237 7.70711 3.29289L11 6.58579C11.781 7.36684 11.781 8.63317 11 9.41421L7.70711 12.7071C7.31658 13.0976 6.68342 13.0976 6.29289 12.7071C5.90237 12.3166 5.90237 11.6834 6.29289 11.2929L8.58579 9H2C1.44771 9 1 8.55228 1 8C1 7.44772 1.44771 7 2 7H8.58578Z"
                                fill="#999999"></path>
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import ApiController from '@/utils/ApiController'
import { defineExpose } from "vue";

const apiController = new ApiController();

const servers = ref([])
const selectedServerIds = ref([])
const isAllSelected = ref(false)
const sidebarCollapsed = ref(false)
const searchQuery = ref("")
const isLoading = ref(true)

const filteredServers = computed(() => {
    if (!searchQuery.value.trim()) {
        return servers.value;
    }
    const query = searchQuery.value.trim().toLowerCase();
    return servers.value.filter(server =>
        server.name.toLowerCase().includes(query) ||
        server.port.toString().toLowerCase().includes(query) ||
        server.host.toString().toLowerCase().includes(query)
    );
})

watch(selectedServerIds, () => {
    const filteredIds = filteredServers.value.map(s => s.id);
    isAllSelected.value = filteredIds.length > 0 && filteredIds.every(id => selectedServerIds.value.includes(id));
});

const toggleSelectServer = (id) => {
    if (!selectedServerIds.value) {
        selectedServerIds.value = []
    }
    const index = selectedServerIds.value.indexOf(id)
    if (index === -1) {
        selectedServerIds.value.push(id)
    } else {
        selectedServerIds.value.splice(index, 1)
    }
}

const toggleSelectAll = (checked) => {
    const filteredIds = filteredServers.value.map(s => s.id);
    if (checked) {
        selectedServerIds.value = Array.from(new Set([...selectedServerIds.value, ...filteredIds]));
    } else {
        selectedServerIds.value = selectedServerIds.value.filter(id => !filteredIds.includes(id));
    }
};

const toggleSidebar = () => {
    sidebarCollapsed.value = !sidebarCollapsed.value
}

const loadServers = async () => {
    const serversData = await apiController.getServers()

    if (!serversData) {
        console.error('Не удалось загрузить сервера')
        return
    }

    if (!serversData.length) {
        console.error('Нету серверов для загрузки')
        return
    }

    servers.value = serversData
    isLoading.value = false
}

const getSelectedServers = () => {
    const selectedServers = [];

    for (const server of servers.value) {
        if (selectedServerIds.value.includes(server.id)) {
            selectedServers.push(server);
        }
    }

    return selectedServers;
}

onMounted(() => {
    loadServers()
})

defineExpose({
    getSelectedServers
})
</script>

<style scoped>
.sidebar {
    width: clamp(18rem, 25vw, 20rem);
    height: 100vh;
    background-color: #ffffff;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: width 0.3s ease, opacity 0.3s ease;
}

.sidebar-collapsed {
    width: clamp(3.5rem, 5vw, 4rem);
    height: 100vh;
    background-color: #ffffff;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    transition: width 0.3s ease, opacity 0.3s ease;
}

.sidebar-enter-active,
.sidebar-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}

.sidebar-enter-from,
.sidebar-leave-to {
    opacity: 0;
    transform: translateX(-20px);
}

.sidebar-enter-to,
.sidebar-leave-from {
    opacity: 1;
    transform: translateX(0);
}

.header,
.search-container,
.select-all-container {
    width: clamp(18rem, 25vw, 20rem);
    height: clamp(3.5rem, 5vh, 4rem);
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.header-collapsed {
    width: clamp(3.5rem, 5vw, 4rem);
    height: clamp(3.5rem, 5vh, 4rem);
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.showSidebar {
    display: block;
}

.closeSidebar {
    display: block;
}

.show,
.close {
    display: none;
}

.header-content,
.select-all-content {
    width: calc(clamp(18rem, 25vw, 20rem) - 2rem);
    height: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-content-collapsed {
    width: clamp(3.5rem, 5vw, 4rem);
    height: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
}

.title {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    height: 2rem;
    width: clamp(4rem, 8vw, 4.5rem);
    color: #333;
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.icon-button {
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    height: 2rem;
    width: 2rem;
    transition: background-color 0.3s ease;
    border-radius: 0.25rem;
}

.icon-button:hover,
.icon-button:focus {
    background-color: #e0e0e0;
    outline: none;
}

.search-box {
    display: flex;
    align-items: center;
    width: calc(clamp(18rem, 25vw, 20rem) - 2rem);
    height: 2rem;
    background-color: #fff;
    border-radius: 0.25rem;
    padding: 0 0.5rem;
    box-shadow: 0 0 0.25rem rgba(0, 0, 0, 0.1);
}

.search-icon {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 1rem;
    height: 1rem;
}

.search-input {
    flex-grow: 1;
    margin-left: 0.5rem;
    height: 1.5rem;
    border: none;
    outline: none;
    background-color: transparent;
    color: #333;
    font-size: 0.875rem;
    font-family: Arial, sans-serif;
}

.search-input::placeholder {
    color: #bbb;
}

.select-all-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    height: 2rem;
    width: clamp(6rem, 10vw, 6.5rem);
    color: #333;
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.checkbox {
    width: 1.125rem;
    height: 1.125rem;
    cursor: pointer;
    accent-color: #1890ff;
    transition: box-shadow 0.3s ease;
}

.checkbox:hover,
.checkbox:focus {
    box-shadow: 0 0 0.3125rem #1890ff;
    outline: none;
}

.servers-container {
    flex-grow: 1;
    overflow-y: auto;
    width: calc(clamp(18rem, 25vw, 20rem) - 1.5rem);
    padding: 0.5rem 0.75rem;
}

.server-item {
    padding: clamp(0.5rem, 2vw, 0.625rem);
    margin-bottom: 0.375rem;
    background-color: transparent;
    border-radius: 1.25rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    outline: none;
    transition: background-color 0.3s ease;
    text-align: left;
}

.server-item:hover {
    background-color: #e0e0e0;
}

.server-item.selected {
    background-color: #d9d9d9;
}

.server-info {
    display: flex;
    flex-direction: column;
    gap: 0.125rem;
}

.server-name {
    font-weight: bold;
    color: #333;
}

.server-port {
    font-size: 0.75rem;
    color: #666;
}
</style>