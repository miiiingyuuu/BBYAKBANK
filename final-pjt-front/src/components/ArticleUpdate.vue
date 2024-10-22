<template>
  <v-container class="background">
    <v-card class="mx-auto my-5 form-card" max-width="600">
      <form @submit.prevent="updateArticle">
        <v-card-title>
          <label for="title" class="label">제목 :</label>
          <input type="text" v-model="article.title" id="title" class="input">
        </v-card-title>
        <v-card-text>
          <label for="content" class="label">내용 :</label>
          <textarea v-model="article.content" id="content" class="textarea"></textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn type="submit" color="primary">Save</v-btn>
        </v-card-actions>
      </form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      article: {
        title: '',
        content: '',
      },
      articleId: this.$route.params.id, // Assuming you're using vue-router
    };
  },
  created() {
    this.fetchArticle();
  },
  methods: {
    fetchArticle() {
      axios.get(`http://127.0.0.1:8000/api/v1/articles/${this.articleId}/`)
        .then(response => {
          this.article = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    },
    updateArticle() {
      axios.put(`http://127.0.0.1:8000/api/v1/articles/${this.articleId}/`, this.article)
        .then(response => {
          this.$router.push({ name: 'articleDetail', params: { id: this.articleId } });
        })
        .catch(error => {
          console.log(this.article);
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.background {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-card {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.input,
.textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.v-btn {
  width: 100%;
  font-size: 16px;
}
</style>
