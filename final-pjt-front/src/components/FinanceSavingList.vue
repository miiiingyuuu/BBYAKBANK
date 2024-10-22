<template>
  <div>
  <header class="d-flex justify-space-between">
    <h1><span class="color">적금</span> 검색하기</h1>
    <div class="w-50 d-flex align-center">
      <div class="btn-container">
        <button 
          :class="['btn', 'btn-primary', { 'selected': selectedTypeRsrv === '자유적립식' }]" 
          @click="selectedTypeRsrv = '자유적립식'"
        >
          자유 적금
        </button>
        <button 
          :class="['btn', 'btn-primary', { 'selected': selectedTypeRsrv === '정액적립식' }]" 
          @click="selectedTypeRsrv = '정액적립식'"
        >
          정기 적금
        </button>
      </div>
      <select 
        v-model="selectedBank" 
        @change="clickBank" 
        class="form-select custom-select"
      >
        <option value="" disabled>은행</option>
        <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
      </select>
    </div>
  </header>
  <hr class="my-3">

  <div v-if="dialog" class="dialog scroll-container">
    <div v-if="selectedSaving" class="card py-5 px-3 modal-content">
      <div class="card-title d-flex align-center justify-space-between">
        <h3>{{ selectedSaving['금융 상품명'] }}</h3>
        <div v-if="userStore.isLogin">
          <button
            v-if="isLikeSaving"
            @click.prevent="deleteSavingUser"
            class="red-button"
          >
            관심 상품 취소
          </button>
          <button
            v-else
            @click.prevent="addSavingUser"
            class="blue-button"
          >
            관심 상품 등록
          </button>
        </div>
      </div>

      <div class="card-text">
        <table>
         <tbody>
          <tr v-for="(value, key) in selectedSaving" :key="key">
            <td width="28%" class="font-weight-bold">{{ key }}</td>
            <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
            <td v-else>{{ value }}</td>
          </tr>
        </tbody>
      </table>
      <hr class="my-3">
      <div class="mx-auto">
        <BarChartDetail
          :title="`${selectedSavingSimple.fin_prdt_nm} (자유적립식)`"
          :average-intr-rate="averageIntrRate"
          :intr-rate="intrRateF"
          :intr-rate2="intrRate2F"
        />
        <BarChartDetail
          :title="`${selectedSavingSimple.fin_prdt_nm} (정액적립식)`"
          :average-intr-rate="averageIntrRate"
          :intr-rate="intrRateS"
          :intr-rate2="intrRate2S"
        />
      </div>
      <p class="text-caption">* 개월별 평균 예금 금리는 2024년 4월 기준입니다.</p>
    </div>

    <div class="card-actions">
      <button @click="close" style="color: #1089FF;">
        닫기
      </button>
    </div>
  </div>
  </div>

  <div v-if="savingLength !== 0" class="table-container">
  <table class="table elevation-6">
    <thead>
      <tr>
        <th>공시월</th>
        <th>은행명</th>
        <th class="text-center" align="center">상품명</th>
        <th align="center">6개월</th>
        <th align="center">12개월</th>
        <th align="center">24개월</th>
        <th align="center">36개월</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in savings" :key="item.saving_code" @click="clickRow(item)">
        <td>{{ item['dcls_month'] }}</td>
        <td>{{ item['kor_co_nm'] }}</td>
        <td align="center">{{ item['fin_prdt_nm'] }}</td>
        <td align="center">{{ item['6month'] }}</td>
        <td align="center">{{ item['12month'] }}</td>
        <td align="center">{{ item['24month'] }}</td>
        <td align="center">{{ item['36month'] }}</td>
      </tr>
    </tbody>
  </table>
  </div>

  <div v-else class="loading">
    <div class="progress-circular">
      <div class="spinner" style="color: #1089FF;"></div>
    </div>
  </div>
</div>

</template>

<script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import BarChartDetail from '@/components/BarChartDetail.vue'
  import axios from 'axios'

const headers = [
{ title: '공시 제출일', align: 'start', sortable: false, width:'10%',key: 'dcls_month' },
{ title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
{ title: '상품명', align: 'center', sortable: false, width:'32%', key: 'fin_prdt_nm' },
{ title: '6개월', align: 'end', width:'12%', key: '6month' },
{ title: '12개월', align: 'end', width:'12%', key: '12month' },
{ title: '24개월', align: 'end',  width:'12%', key: '24month' },
{ title: '36개월', align: 'end', width:'12%', key: '36month' },
]

const API_URL = 'http://localhost:8000/accounts'
const results = ref()
const savings = ref([])
const savingLength = computed(() => {
return savings.value.length
})
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedSavingSimple = ref()
const selectedSaving = ref()
const selectedSavingCode = computed(() => {
  return selectedSavingSimple.value?.['saving_code']
})
const dialog = ref(false)

const averageIntrRate = [2.78, 3.62, 3.57, 3.52]
const intrRateF = ref([null, null, null, null])
const intrRate2F = ref([null, null, null, null])
const intrRateS = ref([null, null, null, null])
const intrRate2S = ref([null, null, null, null])

const selectedTypeRsrv = ref('자유적립식')

const userStore = useUserStore()
const router = useRouter()

const likeList = ref([])

const isLikeSaving = computed(() => {
  return likeList.value?.some(e => e['saving_code'] === selectedSavingCode.value)
})

const makeItems = function (item) {
const result = {
  'saving_code': item['saving_code'],
  'dcls_month': item['dcls_month'],
  'kor_co_nm': item['kor_co_nm'],
  'fin_prdt_nm': item['fin_prdt_nm'],
  '6month': null,
  '12month': null,
  '24month': null,
  '35month': null,
}

const options = Array.isArray(item['savingoption_set']) ? item['savingoption_set'] : []

for (const option of options) {
  const saveTrm = option['save_trm']
  const rsrvTypeNm = option['rsrv_type_nm']

  if (rsrvTypeNm === selectedTypeRsrv.value) {
    if (saveTrm === "6") {
      result['6month'] = option['intr_rate']
    } else if (saveTrm === "12") {
      result['12month'] = option['intr_rate']
    } else if (saveTrm === "24") {
      result['24month'] = option['intr_rate']
    } else if (saveTrm === "36") {
      result['36month'] = option['intr_rate']
    }
  }
}

return result
}

const getAllSaving = function () {
axios({
  method: 'get',
  url: `${userStore.API_URL}/finance/saving_list/`
})
  .then((res) => {
    results.value = res.data
    for (const item of results.value){
      savings.value.push(makeItems(item))
      if (!banks.value.includes(item['kor_co_nm'])) {
        banks.value.push(item['kor_co_nm'])
      }
    }
    // console.log(savings.value)
    // console.log(banks.value)
  }).catch((error) => {
    console.log(error)
  })
}

onMounted(() => {
  getAllSaving()
})

const clickBank = function () {
if (selectedBank.value === '전체 보기') {
  getAllSaving()
} else {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/finance/get_bank_saving/${selectedBank.value}/`
  })
    .then((res) => {
      savings.value = []
      const results = res.data
      for (const item of results){
        savings.value.push(makeItems(item))
      }
    })
    .catch((err) => {
      console.log(err)
    })
}
}

watch(selectedTypeRsrv, () => {
  savings.value = []
  selectedBank.value = '전체 보기'
  for (const item of results.value){
    savings.value.push(makeItems(item))
    if (!banks.value.includes(item['kor_co_nm'])) {
      banks.value.push(item['kor_co_nm'])
    }
  }
})

const close = function () {
  dialog.value = false
  // console.log(dialog.value)
}

const clickRow = function (data) {
  selectedSavingSimple.value = data
  // console.log('Selected Saving Simple:', selectedSavingSimple.value)  // 확인을 위한 로그
  // console.log('Selected Saving Code:', selectedSavingCode.value)  // 확인을 위한 로그
  intrRateF.value = []
  intrRate2F.value = []
  intrRateS.value = []
  intrRate2S.value = []
  getSaving()
  getSavingLikeList()
  // console.log(likeList)
  dialog.value = true
  // console.log(dialog.value)
}

const getSaving = function () {
// const savingCode = selectedSavingSimple.value['saving_code']
axios({
  method: 'get',
  url: `${userStore.API_URL}/finance/saving_list/${selectedSavingCode.value}/`
})
  .then((res) => {
    const data = res.data
    selectedSaving.value = {
      '공시 제출월': data['dcls_month'],
      '금융 회사명': data['kor_co_nm'],
      '금융 상품명': data['fin_prdt_nm'],
      '가입 방법': data['join_way'],
      '만기 후 이자율': data['mtrt_int'],
      '우대 조건': data['spcl_cnd'],
      '가입 대상': data['join_member'],
      '가입 제한': data['join_deny'] === 1 ? '제한없음' : data['join_deny'] === 2 ? '서민전용' : '일부제한',
      '최고 한도': data['max_limit'],
      '기타 유의사항': data['etc_note']
    }

    const optionList = res.data.savingoption_set

    for (const option of optionList) {
      if (option.rsrv_type_nm === '자유적립식') {
        if (option.save_trm === "6") {
          intrRateF.value[0] = option.intr_rate
          intrRate2F.value[0] = option.intr_rate2
        } else if (option.save_trm === "12") {
          intrRateF.value[1] = option.intr_rate
          intrRate2F.value[1] = option.intr_rate2
        } else if (option.save_trm === "24") {
          intrRateF.value[2] = option.intr_rate
          intrRate2F.value[2] = option.intr_rate2
        } else if (option.save_trm === "36") {
          intrRateF.value[3] = option.intr_rate
          intrRate2F.value[3] = option.intr_rate2
        }
      } else {
        if (option.save_trm === "6") {
          intrRateS.value[0] = option.intr_rate
          intrRate2S.value[0] = option.intr_rate2
        } else if (option.save_trm === "12") {
          intrRateS.value[1] = option.intr_rate
          intrRate2S.value[1] = option.intr_rate2
        } else if (option.save_trm === "24") {
          intrRateS.value[2] = option.intr_rate
          intrRate2S.value[2] = option.intr_rate2
        } else if (option.save_trm === "36") {
          intrRateS.value[3] = option.intr_rate
          intrRate2S.value[3] = option.intr_rate2
        }
      }
    }

  })
  .catch((err) => {
    console.log(err)
  })
}

const addSavingUser = function () {
  axios({
    method: 'post',
    url: `${userStore.API_URL}/finance/saving_list/${selectedSavingCode.value}/like/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  })
    .then(response => {
      console.log('적금 저장 완료')
      getSavingLikeList()
      // calculate()
    }).catch(error => {
      console.log('적금 저장 오류 발생', error)
    })
}

const getSavingLikeList = function () {
  axios ({
    method: 'get',
    url: `${userStore.API_URL}/finance/saving_list/${selectedSavingCode.value}/like/`,
    headers: {
        Authorization: `Token ${userStore.token}`
      }
  }).then(response => {
    likeList.value = response.data
  }).catch(error => {
    console.log('오류 발생', error)
  })
}

const deleteSavingUser = function () {
  axios({
    method: 'delete',
    url: `${userStore.API_URL}/finance/saving_list/${selectedSavingCode.value}/like/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then(() => {
    console.log('삭제 완료')
    getSavingLikeList()
  }).catch(error => {
    console.log('오류 발생', error)
  })
}
</script>

<style scoped>
.btn {
  white-space: nowrap; /* 줄 바꿈 방지 */
  margin-right: 15px;
  background-color: #590d77;
  border-color: #590d77;
}
.red-button {
  background-color: red;
  color: white;
  border-radius: 8px; /* 모서리를 네모로 만듭니다. */
  padding: 10px 20px; /* 버튼의 크기와 여백을 조정합니다. */
  border: none; /* 테두리를 없앱니다. */
  cursor: pointer; /* 마우스 커서를 포인터로 변경합니다. */
  white-space: nowrap; /* 텍스트 줄 바꿈을 금지합니다. */
}
.blue-button {
  background-color: blue;
  color: white;
  border-radius: 8px; /* 모서리를 네모로 만듭니다. */
  padding: 10px 20px; /* 버튼의 크기와 여백을 조정합니다. */
  border: none; /* 테두리를 없앱니다. */
  cursor: pointer; /* 마우스 커서를 포인터로 변경합니다. */
  white-space: nowrap; /* 텍스트 줄 바꿈을 금지합니다. */
}
.btn-container {
  display: flex;
  justify-content: start;
}
.selected {
  background-color: #6d0a9b !important; /* 선택된 버튼의 배경색 변경 */
  border-color: #6d0a9b !important; /* 선택된 버튼의 테두리색 변경 */
}
.custom-select {
  border: 2px solid #590d77; /* Bootstrap 기본 파란색 */
  border-radius: 0.25rem;
  padding: 0.375rem 1.75rem 0.375rem 0.75rem;
  color: #495057;
  background-color: #fff;
  background-image: url('data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 4 5%27%3E%3Cpath fill=%27%23000000%27 d=%27M2 0L0 2h4L2 0zm0 5L0 3h4L2 5z%27/%3E%3C/svg%3E');
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 8px 10px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

.custom-select:focus {
  border-color: #0056b3; /* 더 진한 파란색 */
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  /* 모달 스타일링 */
}

.modal-content {
  background-color: white;
  /* 모달 내용 스타일링 */
}
.scroll-container {
  max-height: 850px; /* 원하는 높이로 조절 */
  overflow-y: auto;
}

</style>