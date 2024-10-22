<template>
  <div class="profile-container">
    <div v-if="user" class="profile-details">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>나이 :</strong> {{ user.age }}</p>
      <p><strong>성별 :</strong> {{ genderText }}</p>
      <p><strong>연봉(만원):</strong> {{ user.salary }}</p>
      <p><strong>자산(만원):</strong> {{ user.wealth }}</p>
      <p><strong>저축 선호 성향:</strong> {{ tendencyText }}</p>
      <p>
        <RouterLink to="/myprofile/interest-products" class="interest-link">
          <i class="fas fa-heart"></i> <!-- 하트 모양 아이콘 -->
          관심 상품 목록보기
        </RouterLink>
      </p>
      <p>
        <RouterLink to="recommend/" class="interest-link">
          나에 정보에 맞는 추천 상품 보기
        </RouterLink>
      </p>
      <RouterLink to="/myprofile/update" class="update-link">회원정보 수정하기</RouterLink>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';
import { RouterLink } from 'vue-router';

export default {
  data() {
    return {
      user: null,
    };
  },
  computed: {
    genderText() {
      if (this.user) {
        return this.user.gender === 1 ? '남자' : '여자';
      }
      return '';
    },
    tendencyText() {
      if (this.user) {
        switch (this.user.tendency) {
          case 1:
            return '단기 1년미만 적금 선호';
          case 2:
            return '1년 ~ 2년 적금 선호';
          case 3:
            return '2년 이상 적금 선호';
          default:
            return '';
        }
      }
      return '';
    },
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
  },
};
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.profile-details p {
  margin: 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}

.update-link,
.interest-link {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  color: #fff;
  background-color: #007bff;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  transition: background-color 0.3s;
}

.update-link:hover,
.interest-link:hover {
  background-color: #0056b3;
}

.interest-link i {
  margin-right: 8px; /* 아이콘과 텍스트 사이의 간격 */
}

.recommend-link {
  color: #000; /* 검은색 글자 */
  text-decoration: none;
  transition: color 0.3s;
}

.recommend-link:hover {
  color: #555; /* 호버 시 약간 밝은 검은색 */
}
</style>
