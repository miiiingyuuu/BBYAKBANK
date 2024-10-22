import { defineStore } from 'pinia';
import axios from 'axios';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

export const useUserStore = defineStore('user', () => {
  const BASE_URL = 'http://localhost:8000/accounts';
  const API_URL = 'http://127.0.0.1:8000';
  const token = ref(localStorage.getItem('token'));
  const user = ref(null);  // 사용자 정보를 저장할 상태 추가
  const router = useRouter();

  const login = async (payload) => {
    const data = new FormData();
    data.append('username', payload.username);
    data.append('password', payload.password);
    try {
      const response = await axios({
        method: 'POST',
        url: `${BASE_URL}/login/`,
        data: data,
      });
      console.log('성공');
      token.value = response.data.key;
      localStorage.setItem('token', token.value);
      
      // 사용자 정보를 가져오는 요청
      const userResponse = await axios({
        method: 'GET',
        url: `${BASE_URL}/user/`,
        headers: {
          Authorization: `Token ${token.value}`,
        },
      });
      user.value = userResponse.data;
      console.log('User:', user.value.pk);  // 사용자 정보 출력

      router.push({ name: 'home' });
    } catch (error) {
      console.log(error);
      console.log('흠..');
      alert('회원정보가 올바르지 않습니다.');
    }
  };

  const signup = async (payload) => {
    const data = new FormData();
    data.append('username', payload.username);
    data.append('password1', payload.password1);
    data.append('password2', payload.password2);
    data.append('email', payload.email);
    data.append('age', payload.age);
    data.append('gender', payload.gender);
    data.append('salary', payload.salary);
    data.append('wealth', payload.wealth);
    data.append('tendency', payload.tendency);
    try {
      const response = await axios({
        method: 'POST',
        url: `${BASE_URL}/signup/`,
        data: data,
      });
      console.log('성공');
      router.push({ name: 'signin' });
      alert('회원가입 성공');
    } catch (error) {
      console.log(error);
      console.log('흠..');
      alert('회원정보가 올바르지 않습니다.');
    }
  };

  const logout = () => {
    token.value = null;
    user.value = null;  // 로그아웃 시 사용자 정보 초기화
    localStorage.removeItem('token');
    router.push({ name: 'signin' });
  };

  const isLogin = computed(() => {
    return !!token.value;
  });

  return { login, signup, logout, token, isLogin, API_URL, user };
}, { persist: true });
