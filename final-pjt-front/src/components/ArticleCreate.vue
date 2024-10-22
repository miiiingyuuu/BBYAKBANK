<template>
  <div class="form-container">
    <form @submit.prevent="submitData" class="form">
      <div class="form-group">
        <label for="title" class="form-label">제목</label>
        <input type="text" id="title" v-model="title" class="form-control" />
      </div>
      <div class="form-group">
        <label for="content" class="form-label">내용</label>
        <textarea id="content" v-model="content" class="form-control"></textarea>
      </div>
      <button type="submit" class="btn btn-primary">작성</button>
    </form>
    <div class="back-link">
      <RouterLink to="/community" class="link">뒤로가기</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useArticleStore } from '@/stores/articles.js'
import { useRouter ,RouterLink} from 'vue-router';
const router = useRouter()
const store = useArticleStore()

const title = ref('')
const content = ref('')

const submitData = function () {
  const article = {
    title: title.value,
    content: content.value
  }
  store.createArticle(title.value,content.value)
  title.value = ''
  content.value = ''
  router.push({name:'community'})
}

</script>

<style>
.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: bold;
  color: #333;
}

.form-control {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s ease;

  &:focus {
    outline: none;
    border-color: #007bff;
  }
}

.btn {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: bold;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #0056b3;
  }
}

.back-link {
  margin-top: 1rem;
  text-align: center;

  .link {
    color: #007bff;
    text-decoration: none;
    transition: color 0.3s ease;

    &:hover {
      color: #0056b3;
    }
  }
}

</style>
