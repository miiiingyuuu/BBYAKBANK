<!-- src/views/ExchangeView.vue -->
<template>
  <div class="exchange-view" style="margin-top: 40px;">
    <h1>게시글 생성 페이지</h1>
    <ArticleCreate />
  </div>
</template>

<script setup>
import ArticleCreate from '@/components/ArticleCreate.vue'
</script>

<style scoped>
.exchange-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f0f4f8; /* 부드러운 배경색 */
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  min-height: 100vh;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* ArticleCreate 컴포넌트에 대한 스타일을 추가할 수 있습니다. */
.article-create-container {
  width: 100%;
  max-width: 100%;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
