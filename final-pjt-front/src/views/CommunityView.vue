<template>
  <div class="post-list-page">
    <h1>게시글 목록 페이지</h1>
    <button class="create-button" @click="router.push({ name: 'create' })">게시글 생성</button>
    <ArticleList />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import ArticleList from '../components/ArticleList.vue';
const router = useRouter();
</script>

<style lang="scss" scoped>
.post-list-page {
  margin-top: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  
  h1 {
    /* font-size: 2rem; */
    margin-bottom: 20px;
    /* color: #333; */
  }

  .create-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    margin-bottom: 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #45a049;
    }

    &:active {
      background-color: #3e8e41;
    }
  }

  .article-list {
    width: 100%;
    max-width: 800px;
  }
}
</style>
