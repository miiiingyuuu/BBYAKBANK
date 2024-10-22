<!-- src/views/HomeView.vue -->
<template>
  <div class="home-container">
    <div class="home-container">
    <!-- <h1>Welcome to the Home View</h1> -->
    <!-- 이미지 표시 -->
      <img src="@/assets/Home.png" alt="Large Image" class="large-image" />
    </div>
  </div>
</template>

<script>
// export default {
//   name: 'HomeView'
// }
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px; /* 여백 추가 */
}

.large-image {
  width: 90%; /* 원래 크기의 80%로 조정 */
  max-width: 1702.4px; /* 원래 크기의 80%에 해당하는 최대 너비 */
  height: auto; /* 이미지 비율을 유지하면서 높이를 자동으로 조정 */
  object-fit: cover; /* 필요한 경우 이미지 비율을 유지합니다. */
}
</style>
