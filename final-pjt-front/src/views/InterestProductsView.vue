<template className="wrap-container">
  <div class="interest-products-container" className="home-container">
    <div >
    <h2 style="margin-top: 40px; margin-left: 20px;">내가 좋아하는 상품 목록</h2>
    <ul>
      <h1 style="margin-top: 40px; margin-left: 25px;" >예금 목록</h1>
      <li v-for="product in interestProducts" :key="product.deposit_code" v-if="interestProducts.length !== 0">
        <div class="product-card" style="margin-left: 20px;">
          <!-- {{ product }} -->
          <h3>{{ product.fin_prdt_nm }} <{{ product.kor_co_nm }}></h3>
          <p>코드: {{ product.deposit_code }}</p>
          <p>금융 회사명: {{ product.kor_co_nm }}</p>
          <p>공시월: {{ product.dcls_month }}</p>
          <hr>
          <p>상세설명: {{ product.etc_note }}</p>
          <p>우대조건: {{ product.spcl_cnd }}</p>
          <p>만기 후 금리: {{ product.mtrt_int }}</p>
          <p>가입방법: {{ product.join_way }}</p>
          <button @click="removeProduct(product.id, product.like_user[0], 'deposit')">삭제</button>
        </div>
      </li>
      <span v-else style="margin-top: 40px;">상품 코드가 유효하지 않습니다.</span>
    </ul>
    <ul  className="wrap-container">
      <h1 style="margin-top: 40px; margin-left: 25px;">적금 목록</h1>
      <li v-for="product in interestProducts2" :key="product.saving_code"  v-if="interestProducts2.length !== 0">
        <div class="product-card" style="margin-left: 20px;">
          <!-- {{ product }} -->
          <h3>{{ product.fin_prdt_nm }} <{{ product.kor_co_nm }}></h3>
          <p>코드: {{ product.saving_code }}</p>
          <p>금융 회사명: {{ product.kor_co_nm }}</p>
          <p>공시월: {{ product.dcls_month }}</p>
          <hr>
          <p>상세설명: {{ product.etc_note }}</p>
          <p>우대조건: {{ product.spcl_cnd }}</p>
          <p>만기 후 금리: {{ product.mtrt_int }}</p>
          <p>가입방법: {{ product.join_way }}</p>

          <button @click="removeProduct(product.id, product.like_user[0], 'saving')">삭제</button>
        </div>
        
      </li>
      <!-- <span v-else>상품 코드가 유효하지 않습니다.</span> -->
    </ul>
  </div>
</div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';

export default {
  data() {
    return {
      interestProducts: [],
      interestProducts2: []
    };
  },
  created() {
    this.fetchInterestProducts();
  },
  methods: {
    async fetchInterestProducts() {
      const store = useUserStore();
      try {
        const response = await axios.get('http://127.0.0.1:8000/finance/user-likes', {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });
        const response2 = await axios.get('http://127.0.0.1:8000/finance/user-likes2', {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });
        this.interestProducts = response.data;
        this.interestProducts2 = response2.data;
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching interest products:', error);
      }
    },
    async removeProduct(productid, userid, type) {
      const store = useUserStore();
      try {
        const url = type === 'deposit'
          ? `http://127.0.0.1:8000/finance/remove_like/${productid}/${userid}`
          : `http://127.0.0.1:8000/finance/remove_like2/${productid}/${userid}`;

        await axios.delete(url, {
          headers: {
            Authorization: `Token ${store.token}`
          }
        });

        if (type === 'deposit') {
          this.interestProducts = this.interestProducts.filter(product => product.id !== productid);
        } else {
          this.interestProducts2 = this.interestProducts2.filter(product => product.id !== productid);
        }

        console.log(`Product with id ${productid} removed from ${type} list`);
      } catch (error) {
        console.error('Error removing product:', error);
      }
    }
  }
}
</script>

<style scoped>

.wrap-container{
  height: auto;
  min-height: 100%;
  padding-bottom: 60px ;
}
.home-container{
  min-height: 600px;
}
.interest-products-container {
  padding: 20px;
  height: 100vh;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

.product-card {
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 10px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.product-card h3 {
  margin-top: 0;
}

.product-card button {
  background-color: #ff0000;
  color: white;
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
}

.product-card button:hover {
  background-color: #cc0000;
}
</style>
