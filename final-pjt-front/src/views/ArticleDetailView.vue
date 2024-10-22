<!-- src/views/ExchangeView.vue -->

<template>
  <div class="exchange-view">
    <h1>게시글 상세 페이지</h1>
    <ArticleDetail />
  </div>
</template>

<script setup>
import ArticleDetail from '@/components/ArticleDetail.vue'
</script>

<style scoped>
.exchange-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 수직으로도 중앙 정렬 */
  min-height: 100vh; /* 뷰포트 전체 높이 */
  padding: 20px;

}

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

/* ArticleDetail 컴포넌트에 대한 스타일을 추가할 수 있습니다. */
.article-detail-container {
  width: 100%;
  max-width: 800px;
  background-color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}
</style>
