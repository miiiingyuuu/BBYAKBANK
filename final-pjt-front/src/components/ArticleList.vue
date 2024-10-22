<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6 col-lg-4 mb-4" v-for="article in store.articles" :key="article.pk">
        <div class="card article-card">
          <div class="card-body">
            <h1 class="card-title">제목 : {{ article.title }}</h1>
            <!-- <p>{{ article.user.id }}</p> -->
            <RouterLink :to="{ name: 'articleDetail', params: { id: article.pk } }" class="btn btn-primary">
              게시글 보러가기
            </RouterLink>
            <p v-if="article.user.id === userStore.user?.pk" class="text-caption"><br>회원님이 작성한 글입니다</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/articles'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user';

const store = useArticleStore()
const userStore = useUserStore();
onMounted(() => {
  store.getArticles()
})
</script>


<style>
.container {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.article-card {
  height: 200px !important;
  box-sizing: border-box;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .card-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #333;
    margin-bottom: 0.5rem;
  }

  .card-text {
    font-size: 0.95rem;
    color: #555;
    margin-bottom: 1rem;
  }

  .btn {
    font-size: 0.9rem;
  }
}

@media (max-width: 767px) {
  .article-card {
    .card-title {
      font-size: 1.1rem;
    }

    .card-text {
      font-size: 0.9rem;
    }

    .btn {
      font-size: 0.85rem;
    }
  }
}
</style>