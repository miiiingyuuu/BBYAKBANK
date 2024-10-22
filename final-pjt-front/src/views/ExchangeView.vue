<!-- src/views/ExchangeView.vue -->

<template>
  <div class="container" style="display: flex; justify-content: center;">
    <div class="exchange-container">
      <h1>환율계산기</h1>
      <Exchange />
    </div>
  </div>
</template>

<script setup>
import Exchange from '@/components/Exchange.vue'
</script>

<style scoped>
/* .exchange-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
  background-color: #e7eff6; /* 부드러운 하늘색 배경 */
/* } */

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* Exchange 컴포넌트에 대한 스타일을 추가할 수 있습니다. */
.exchange-container {
  height: 100Vh;
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.container {
  display: relative;
  margin: auto;
}
</style>
