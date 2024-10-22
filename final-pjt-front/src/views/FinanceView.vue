<template>
  <div class="interest-info-container"  className="wrap-container">
    <div  className="home-container">
    <h1 style="margin-top: 40px;"> 금리 정보 확인</h1>
    <header class="d-flex justify-content-center align-center mb-7">
      <RouterLink :to="{ name: 'depositList'}" exact-active-class="active" class="silver-button">정기예금</RouterLink>
      <RouterLink  outerLink :to="{ name: 'savingList'}" exact-active-class="active" class="silver-button">정기적금</RouterLink>
    </header>
  <div class="container">
    <RouterView />
  </div>
  </div>
</div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
import FinanceDepositList from '@/components/FinanceDepositList.vue';
import FinanceSavingList from '@/components/FinanceSavingList.vue';
</script>

<style scoped>
.wrap-container{
  height: auto;
  min-height: 100%;
  padding-bottom: 60px ;
}
.home-container{
  min-height: 600px;
}
.interest-info-container {
  /* background-color: #e7eff6; 부드러운 하늘색 배경 */
  padding: 20px;
  /* height: 100%; */
  height: 100Vh;
}


h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  
}

.container {
  max-width: 800px;
  margin: 0 auto;
  /* height: 100Vh; */
}

header {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  text-align: center;
}

span {
  margin: 0 0.5rem;
}

.active {
  font-weight: bold;
  color: #007bff; /* 활성화된 링크 색상 */
  margin-right: 10px;
}

.silver-button {
  color: #000000;
  background-color: #C0C0C0; /* 은색 배경 */
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s ease;
  margin-right: 10px;
}

.silver-button:hover {
  background-color: #A9A9A9; /* 호버시 조금 더 어두운 은색 */
}

.silver-button.active {
  background-color: #808080; /* 활성화된 링크 색상 */
}
</style>
