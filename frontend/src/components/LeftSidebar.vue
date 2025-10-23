<template>
  <div class="sidebar">
    <div class="icon-group">
      <div class="icon" @click="goToPage('/process')" :class="{ active: currentPath === '/process' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
          :fill="currentPath === '/process' ? '#1890ff' : '#1a1a1a'">
          <path fill-rule="evenodd" clip-rule="evenodd"
            d="M8 21.9999C6.0233 21.9983 4.98717 21.9732 4.18404 21.564C3.43139 21.1805 2.81947 20.5686 2.43597 19.8159C2 18.9603 2 17.8402 2 15.6V12.614C2 10.9196 2 10.0724 2.21548 9.29017C2.40638 8.59722 2.72024 7.9442 3.14209 7.36225C3.61828 6.70535 4.27982 6.17611 5.60292 5.11763L6.00292 4.79763C8.14324 3.08538 9.21339 2.22925 10.4002 1.90092C11.4471 1.61131 12.5529 1.61131 13.5998 1.90092C14.7866 2.22925 15.8568 3.08538 17.9971 4.79763L18.3971 5.11762C19.7202 6.17611 20.3817 6.70535 20.8579 7.36225C21.2798 7.9442 21.5936 8.59722 21.7845 9.29017C22 10.0724 22 10.9196 22 12.614V15.6C22 17.8402 22 18.9603 21.564 19.8159C21.1805 20.5686 20.5686 21.1805 19.816 21.564C19.0128 21.9732 17.9767 21.9983 16 21.9999H8ZM20 12.614V15.6C20 16.7531 19.9984 17.4976 19.9521 18.0643C19.9078 18.6076 19.8324 18.8091 19.782 18.9079C19.5903 19.2843 19.2843 19.5902 18.908 19.782C18.8091 19.8324 18.6077 19.9077 18.0643 19.9521C17.566 19.9928 16.9302 19.9989 16 19.9998V15C16 12.7908 14.2091 11 12 11C9.79086 11 8 12.7908 8 15V19.9998C7.06979 19.9989 6.43396 19.9928 5.93567 19.9521C5.39235 19.9077 5.19091 19.8324 5.09202 19.782C4.71569 19.5902 4.40973 19.2843 4.21799 18.9079C4.1676 18.8091 4.09225 18.6076 4.04785 18.0643C4.00156 17.4976 4 16.7531 4 15.6V12.614C4 10.8084 4.01684 10.2817 4.14366 9.82135C4.27092 9.35938 4.48016 8.92404 4.7614 8.53607C5.04164 8.14947 5.44238 7.80732 6.85232 6.67936L7.25232 6.35936C8.34513 5.48511 9.08192 4.89728 9.69095 4.47924C10.2792 4.07548 10.6363 3.91073 10.9335 3.82852C11.6314 3.63545 12.3686 3.63545 13.0665 3.82852C13.3637 3.91073 13.7208 4.07548 14.3091 4.47924C14.9181 4.89727 15.6549 5.48511 16.7477 6.35936L17.1477 6.67936C18.5576 7.80732 18.9584 8.14947 19.2386 8.53607C19.5198 8.92404 19.7291 9.35938 19.8563 9.82135C19.9832 10.2817 20 10.8084 20 12.614ZM10 20V15C10 13.8954 10.8954 13 12 13C13.1046 13 14 13.8954 14 15V20H10Z">
          </path>
        </svg>
      </div>
      <div class="icon" @click="goToPage('/export')" :class="{ active: currentPath === '/export' }">
        <svg :fill="currentPath === '/export' ? '#1890ff' : '#1a1a1a'" width="24px" height="24px" viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg">
          <path
            d="M8.71,7.71,11,5.41V15a1,1,0,0,0,2,0V5.41l2.29,2.3a1,1,0,0,0,1.42,0,1,1,0,0,0,0-1.42l-4-4a1,1,0,0,0-.33-.21,1,1,0,0,0-.76,0,1,1,0,0,0-.33.21l-4,4A1,1,0,1,0,8.71,7.71ZM21,14a1,1,0,0,0-1,1v4a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V15a1,1,0,0,0-2,0v4a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V15A1,1,0,0,0,21,14Z" />
        </svg>
      </div>
      <div class="icon" @click="goToPage('/import')" :class="{ active: currentPath === '/import' }">
        <svg :fill="currentPath === '/import' ? '#1890ff' : '#1a1a1a'" width="24px" height="24px"
          viewBox="0 0 24.00 24.00" xmlns="http://www.w3.org/2000/svg">
          <path
            d="M21,14a1,1,0,0,0-1,1v4a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V15a1,1,0,0,0-2,0v4a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V15A1,1,0,0,0,21,14Zm-9.71,1.71a1,1,0,0,0,.33.21.94.94,0,0,0,.76,0,1,1,0,0,0,.33-.21l4-4a1,1,0,0,0-1.42-1.42L13,12.59V3a1,1,0,0,0-2,0v9.59l-2.29-2.3a1,1,0,1,0-1.42,1.42Z" />
        </svg>
      </div>
    </div>
    <div class="profile-icon" @click="goToPage('/login')">
      <img
        src="data:data:image/png;base64,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"
        alt="Profile" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftSidebar',
  computed: {
    currentPath() {
      return this.$route.path;
    }
  },
  methods: {
    goToPage(path) {
      this.$router.push(path);
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: clamp(4rem, 6vw, 4.5rem);
  height: 100vh;
  background-color: #F5F5F5;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  padding: clamp(0.75rem, 3vw, 1rem) 0;
  box-sizing: border-box;
}

.icon-group {
  display: flex;
  flex-direction: column;
  gap: clamp(0.75rem, 3vw, 1rem);
  align-items: center;
}

.icon {
  width: clamp(2.5rem, 6vw, 3rem);
  height: clamp(2.5rem, 6vw, 3rem);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 0.5rem;
  transition: background-color 0.2s ease;
}

.icon:hover {
  background-color: #e0e0e0;
}

.profile-icon {
  width: clamp(2rem, 4vw, 2.5rem);
  height: clamp(2rem, 4vw, 2.5rem);
  margin-bottom: 0.5rem;
  cursor: pointer;
}

.profile-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 50%;
}
</style>