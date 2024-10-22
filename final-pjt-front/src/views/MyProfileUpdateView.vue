<template>
  <div class="profile-page" style="margin-top: 22px;">
    <h1>회원정보 수정하기</h1>
    <div class="profile-container">
    <MyProfileUpdate />
  </div>
  </div>
  </template>
  
  <script setup>
  import MyProfileUpdate from '@/components/MyProfileUpdate.vue'
  </script>
  

  <style lang="scss" scoped>
  .profile-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    height: 100vh;
  
    h1 {
      font-size: 2.5rem;
      margin-bottom: 30px;
      color: #333;
    }
  
    .profile-container {
      width: 100%;
      max-width: 600px;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 10px;
    }
  }
  </style>
  