<!-- src/views/UpdateProfileView.vue -->
<template>
  <div class="update-profile-container">
    <h2>회원정보 수정하기</h2>
    <form @submit.prevent="updateProfile">
      <div class="form-group">
        <label for="age">나이:</label>
        <input type="number" v-model="user.age" id="age" required />
      </div>
      <div class="form-group">
        <label for="gender">성별:</label>
        <select v-model="user.gender" id="gender" required>
          <option value="1">남자</option>
          <option value="2">여자</option>
        </select>
      </div>
      <div class="form-group">
        <label for="salary">연봉(만원):</label>
        <input type="number" v-model="user.salary" id="salary" required />
      </div>
      <div class="form-group">
        <label for="wealth">자산(만원):</label>
        <input type="number" v-model="user.wealth" id="wealth" required />
      </div>
      <div class="form-group">
        <label for="tendency">저축 선호 성향:</label>
        <select v-model="user.tendency" id="tendency" required>
          <option value="1">단기 1년미만 적금 선호</option>
          <option value="2">1년 ~ 2년 적금 선호</option>
          <option value="3">2년 이상 적금 선호</option>
        </select>
      </div>
      <button type="submit" class="update-button">수정하기</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';

export default {
  data() {
    return {
      user: {
        age: '',
        gender: '',
        salary: '',
        wealth: '',
        tendency: '',
      },
    };
  },
  async created() {
    await this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      const store = useUserStore();
      try {
        const response = await axios.get(`${store.API_URL}/api/accounts/profile/`, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });
        this.user = response.data;
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    },
    async updateProfile() {
      const store = useUserStore();
      try {
        const response = await axios.put(`${store.API_URL}/api/accounts/profile/update/`, this.user, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });
        if (response.status === 200) {
          alert('프로필이 성공적으로 업데이트되었습니다.');
          this.$router.push('/myprofile');  // Redirect to profile page
        }
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },
  },
};
</script>

<style scoped>
.update-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.update-button {
  display: inline-block;
  padding: 10px 20px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.3s;
}

.update-button:hover {
  background-color: #0056b3;
}
</style>
