<template>
  <div class="signup-container">
    <form @submit.prevent="onSubmit" class="signup-form">
      <h2>회원가입</h2>
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>
      <div class="form-group">
        <label for="email">E-mail</label>
        <input type="email" id="email" v-model.trim="email" required>
      </div>
      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input type="password" id="password1" v-model="password1" required>
      </div>
      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input type="password" id="password2" v-model="password2" required>
      </div>
     
      <input type="submit" value="회원가입" class="signup-button">
    </form>
  </div>
</template>

<script setup>
import { useUserStore } from '@/stores/user';
import { ref } from 'vue';

const userStore = useUserStore();
const username = ref('');
const password1 = ref('');
const password2 = ref('');
const email = ref('');
const age = ref('');
const gender = ref('');
const salary = ref('');
const wealth = ref('');
const tendency = ref('');

const onSubmit = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: email.value,
    age: age.value,
    gender: gender.value,
    salary: salary.value,
    wealth: wealth.value,
    tendency: tendency.value,
  };
  userStore.signup(payload);
};
</script>

<style scoped>
.signup-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.signup-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.signup-form h2 {
  margin-bottom: 1rem;
  text-align: center;
}

.form-group {
  margin-bottom: 0.75rem; /* 마진 간격을 줄였습니다 */
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="password"],
.form-group input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.radio-inline {
  display: inline-block;
  margin-right: 10px;
  margin-bottom: 0.5rem; /* 마진 간격을 줄였습니다 */
}

.signup-button {
  width: 100%;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  background-color: #007bff;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.signup-button:hover {
  background-color: #0056b3;
}
</style>
