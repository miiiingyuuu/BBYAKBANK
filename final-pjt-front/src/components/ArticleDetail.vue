<template>
  <v-container>
    <v-card v-if="article" class="mx-auto my-5" max-width="600">
      <!-- <p>{{ article }}</p>  -->
      <v-card-title>{{ article.user.username }}님이 작성한 글입니다.</v-card-title>
      <v-card-subtitle>글 번호: {{ article.id }}</v-card-subtitle>
      <v-card-text>
        <p>제목: {{ article.title }}</p>
        <h3>내용: {{ article.content }}</h3>
        <br>
        <p>작성시간: {{ article.created_at.substring(0, 19) }}</p>
        <p>수정시간: {{ article.updated_at.substring(0, 19) }}</p>
        <div>
          <p>댓글:</p>
          <v-list>
            <v-list-item v-for="comment in article.comment_set" :key="comment.id">
              <v-list-item-content>
                <v-list-item-title>내용: {{ comment.content }} </v-list-item-title>
                <v-list-item-subtitle class ='mb-2'>작성자 : {{ comment.user.username }} 작성시간 : {{ comment.created_at.substring(0, 19) }}</v-list-item-subtitle>
                <v-btn
                  v-if="comment.user.id === userStore.user?.pk"
                  color="error"
                  @click="deleteComment(comment.id)"
                >
                  댓글 삭제
                </v-btn>
              </v-list-item-content>
              <v-divider></v-divider>
            </v-list-item>
          </v-list>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-form @submit.prevent="createComment" class="d-flex align-center">
          <v-text-field
            v-model="comment"
            label="댓글"
            outlined
            dense
            hide-details
            class="mr-3"
          ></v-text-field>
          <v-btn type="submit" color="primary">댓글 생성</v-btn>
        </v-form>
        <v-btn v-if="article.user.id === userStore.user?.pk" @click="update_article">
          게시글 수정
        </v-btn> 
        <v-btn v-if="article.user.id === userStore.user?.pk" color="error" @click="deleteArticle">
          게시글 삭제
        </v-btn>
        <v-btn to="/community" text>뒤로가기</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useArticleStore } from '@/stores/articles';
import { useUserStore } from '@/stores/user';

const store = useArticleStore();
const userStore = useUserStore();
const route = useRoute();
const router = useRouter();
const article = ref(null);
const comment = ref('');

onMounted(() => {
  fetchArticle();
});

const fetchArticle = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
  })
    .then((res) => {
      // console.log(res.data);
      article.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

const deleteArticle = () => {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/`,
  })
    .then(() => {
      router.push('/');
    })
    .catch((err) => {
      console.log(err);
    });
};

const deleteComment = (pk) => {
  axios({
    method: 'delete',
    url: `${store.API_URL}/api/v1/articles/${route.params.id}/${pk}/delete/`,
    headers: {
      Authorization: `Token ${userStore.token}`,
    },
  })
    .then((response) => {
      article.value.comment_set = article.value.comment_set.filter((c) => c.id !== pk);
      // console.log(response);
    })
    .catch((err) => {
      console.log(err);
    });
};

const createComment = () => {
  axios({
    method: 'post',
    url: `${store.API_URL}/api/v1/articles/${article.value.id}/comments/`,
    data: {
      content: comment.value,
    },
    headers: {
      Authorization: `Token ${userStore.token}`,
    },
  })
    .then((res) => {
      console.log(res.data);
      // 새로운 댓글을 불러와서 기존 댓글 목록에 추가
      fetchArticle();
      comment.value = ''; // 댓글 입력창 초기화
    })
    .catch((err) => {
      console.log(err);
    });
};

const update_article = () => {
  router.push({ name: 'articleUpdate', params: { id: route.params.id } });
};
</script>


<style>
.v-card {
  margin-top: 20px;
  border: 1px solid black;
}
.v-form {
  width: 100%;
  display: flex;
  align-items: center;
}
</style>
