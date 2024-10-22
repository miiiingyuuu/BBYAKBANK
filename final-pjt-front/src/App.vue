<!-- src/App.vue -->
<template>
  <header class="header">
    <div class="header-wrapper">
      <nav class="nav">
        <div class="nav-left">
          <RouterLink to="/" class="nav-link">
            <img src="@/assets/Logo(1).png" alt="홈" class="logo-image">
          </RouterLink>
        </div>
        <div class="nav-right" v-if="!store.isLogin">
          <RouterLink to="/signin" class="nav-link">로그인</RouterLink>
          <RouterLink to="/signup" class="nav-link">회원가입</RouterLink>
          <RouterLink to="/community" class="nav-link">자유게시판</RouterLink>
        </div>
        <div class="nav-right" v-else>
          <RouterLink to="/exchange" class="nav-link">환율 계산기</RouterLink>
          <RouterLink to="/finance" class="nav-link">예적금 금리 비교</RouterLink>
          <RouterLink to="/map" class="nav-link">근처 은행 검색</RouterLink>
          <RouterLink to="/community" class="nav-link">자유 게시판</RouterLink>
          <RouterLink to="/myprofile" class="nav-link">마이 페이지</RouterLink>
          <button @click="logout" class="logout-btn">Logout</button>
          <strong><p class="nav-link">{{ user.username }}님 환영합니다!</p></strong>
        </div>
      </nav>
    </div>
  </header>
  <RouterView />
  <!-- <div className="wrap-container"> -->
  <!-- </div> -->
    <footer class="footer-container">
    <small>
      <div class="footer-content">
        <div class="footer-section about">
          <h2 class="logo-text">CompanyName</h2>
          <p>
            PPYAKK.BANK provides innovative solutions and does its best for your convenience.
            If you have any questions, please feel free to contact us.
          </p>
        </div>
        <div class="footer-section contact">
          <ul>
            <li>Address: 302, 3gongdan 3-ro, Gumi-si, Gyeongsangbuk-do, Republic of Korea</li>
            <li>Contact: 02-3429-5100 Email: ssafy@ssafy.com</li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>Copyright (C) 2024. PPYAK.BANK. All Rights Reserved</p>
      </div>
    </small>
  </footer>
 
  
  <button v-if="store.isLogin" @click="openChatbot" class="chatbot-btn">💬</button>

</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useUserStore } from './stores/user';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import FooterView from '@/views/FooterView.vue';

const store = useUserStore();
const router = useRouter();
const user = store.user

const logout = function() {
  store.token = null;
  router.push({ name: 'signin' });
};

const openChatbot = () => {
  router.push({ name: 'cgpt' });
};
</script>

<style scoped>
footer{
  height: auto;
  position: relative;
  transform: translateY(0%);
  border-top:1px solid #248efe;
  text-align: left;
  display: flex;
  /* align-items:center; */
  justify-content: center;
  background-color: #626262;
}

/* // <uniquifier>: Use a unique and descriptive class name
// <weight>: Use a value from 200 to 700 */

* {
  font-family: "Jua", sans-serif;
  font-optical-sizing: auto;
  font-weight: <weight>;
  font-style: normal;
}
.header {
  background-color: #FFFFFF; /* 배경을 흰색으로 변경 */
  padding: 1rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;

  .header-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav {
    display: flex;
    align-items: center;
    width: 100%;
    justify-content: space-between;
    

    .nav-left {
      flex: 0 0 auto; /* 왼쪽에 고정 */

      .logo-image {
        height: 60px; /* 원하는 높이로 설정 */
        width: auto; /* 비율 유지 */
      }
    }

    .nav-right {
      display: flex;
      gap: 1rem; /* 간격 조정 */
      flex: 1; /* 남은 공간 차지 */
      justify-content: flex-end; /* 오른쪽 정렬 */
      flex-wrap: nowrap; /* 한 줄로 유지 */
      margin-top: 10px;
    }

    .nav-link {
      color: #6A1B9A; /* 보라색 계열 */
      text-decoration: none;
      font-size: 1rem;
      font-weight: bold;
      white-space: nowrap; /* 줄 바꿈 방지 */
      transition: color 0.3s ease;

      &:hover {
        color: #BA68C8; /* 더 밝은 보라색 계열 */
      }

      &.router-link-active {
        color: #BA68C8; /* 더 밝은 보라색 계열 */
      }
    }

    .logout-btn {
      background-color: #6A1B9A; /* 보라색 계열 */
      color: #fff;
      border: none;
      padding: 0.5rem 1rem;
      font-size: 1rem;
      font-weight: bold;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      white-space: nowrap; /* 줄 바꿈 방지 */

      &:hover {
        background-color: #BA68C8; /* 더 밝은 보라색 계열 */
      }
    }
  }
}
.chatbot-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #6A1B9A; /* 보라색 계열 */
  color: #fff;
  border: none;
  padding: 0.75rem;
  font-size: 1.5rem;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #BA68C8; /* 더 밝은 보라색 계열 */
  }
}

@media (max-width: 768px) {
  .header {
    padding: 0.75rem 0;

    .header-wrapper {
      padding: 0 1rem;
    }

    .nav {
      flex-direction: column; /* 세로 배치 */
      align-items: flex-start;

      .nav-left,
      .nav-right {
        flex: none;
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 0.5rem;
      }

      .nav-link {
        font-size: 0.9rem;
      }

      .logout-btn {
        padding: 0.4rem 0.8rem;
        font-size: 0.9rem;
      }
    }
  }

  .chatbot-btn {
    bottom: 15px;
    right: 15px;
    padding: 0.6rem;
    font-size: 1.2rem;
  }
}
.footer-container {
  background: #333;
  color: #fff;
  padding: 20px 0;
}

.footer-content {
  text-align: left; /* 왼쪽 정렬 */
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-section {
  flex: 1;
  margin: 10px;
  min-width: 250px;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
}

.footer-section h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.footer-section p, .footer-section ul, .footer-section li {
  font-size: 14px;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-bottom {
  text-align: left; /* 왼쪽 정렬 */
  padding: 10px;
  background: #222;
}

.footer-bottom p {
  margin: 0;
  font-size: 14px;
}
</style>