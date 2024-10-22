<!-- src/components/Footer.vue -->
<template>
  <div id="wrapper">
    <footer class="footer">
    <div class="footer-content">
      <div class="footer-section company-info">
        <h3>회사 정보</h3>
        <p>회사 이름: ABC Corp</p>
        <p>주소: 서울특별시 강남구 테헤란로 123</p>
        <p>전화: 02-1234-5678</p>
        <p>이메일: info@abccorp.com</p>
      </div>
      <div class="footer-section nav-links">
        <h3>링크</h3>
        <ul>
          <li><RouterLink to="/">홈</RouterLink></li>
          <li><RouterLink to="/services">서비스</RouterLink></li>
          <li><RouterLink to="/blog">블로그</RouterLink></li>
          <li><RouterLink to="/faq">FAQ</RouterLink></li>
        </ul>
      </div>
      <div class="footer-section legal-info">
        <h3>법적 정보</h3>
        <ul>
          <li><RouterLink to="/terms">이용 약관</RouterLink></li>
          <li><RouterLink to="/privacy">개인정보 보호정책</RouterLink></li>
        </ul>
      </div>
      <div class="footer-section social-media">
        <h3>소셜 미디어</h3>
        <p>
          <a href="https://facebook.com" target="_blank">페이스북</a> |
          <a href="https://twitter.com" target="_blank">트위터</a> |
          <a href="https://instagram.com" target="_blank">인스타그램</a>
        </p>
      </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router';

export default {
  name: 'Footer',
  components: {
    RouterLink
  }
};
</script>

<style scoped>
#wrapper {
  #wrap{
	min-height: calc(100vh - 10rem); /* footer 높이를 빼준다. */
	background: pink;
}
}

.footer {
  background-color: #333;
  color: #fff;
  padding: 2rem 1rem;
  text-align: center;
  height: 25rem

}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}

.footer-section {
  margin-bottom: 1rem;
  flex: 1 1 200px;
}

.footer-section h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  border-bottom: 1px solid #fff;
  display: inline-block;
}

.footer-section p,
.footer-section ul,
.footer-section a {
  font-size: 0.9rem;
  color: #ccc;
  text-decoration: none;
}

.footer-section a:hover {
  color: #fff;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}
</style>
