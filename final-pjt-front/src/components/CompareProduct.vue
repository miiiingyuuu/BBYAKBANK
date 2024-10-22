<template>
  <div class="wrap-container">
    <div class="home-container">
      <div>
        <h1 class="title">
          회원님의 정보에 맞는 추천 상품 목록
        </h1>
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <div class="loading-message">
            회원님의 개인정보와 적절한 상품을 찾는 중입니다....
          </div>
        </div>
        <ul v-else class="product-list">
          <li v-for="product in depositProducts" :key="product.product_id" class="product-item">
            <div class="product-card">
              <h2>{{ product.fin_prdt_nm }}</h2>
              <p>{{ user }}</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';

const API_URL = 'http://localhost:8000/api/accounts'; // Django 서버 주소

const depositProducts = ref([]);
const loading = ref(true);
const userStore = useUserStore();

onMounted(() => {
  setTimeout(() => {
    fetchRecommendations();
  }, 5000);
});

const fetchRecommendations = async () => {
  try {
    const response = await axios.get(`${API_URL}/profile/recommendations/`, {
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    });
    depositProducts.value = response.data;
    loading.value = false;
  } catch (error) {
    console.error('Error fetching recommendations:', error);
  }
};
</script>

<style scoped>
.wrap-container {
  height: auto;
  min-height: 100%;
  padding-bottom: 60px;
  background-color: #f5f5f5; /* 배경색 추가 */
}

.home-container {
  min-height: 600px;
  padding: 20px; /* 내부 패딩 추가 */
}

.title {
  margin-top: 40px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  margin-top: 40px;
  height: 400px;
}

.spinner {
  border: 8px solid #f3f3f3;
  border-top: 8px solid #3498db;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 2s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-message {
  font-size: 24px;
}

.product-list {
  margin-top: 40px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.product-item {
  list-style: none;
  flex: 1 1 calc(33.333% - 40px); /* 3개의 항목을 한 줄에 배치 */
  max-width: calc(33.333% - 40px);
  box-sizing: border-box; /* 박스 사이징 설정 */
}

.product-card {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  height: 100%; /* 카드 높이를 100%로 설정 */
}

.product-card h2 {
  font-size: 20px;
  margin-bottom: 10px;
}

.product-card p {
  font-size: 16px;
  color: #555;
}
</style>
