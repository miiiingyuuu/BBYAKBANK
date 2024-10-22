<template>
  <div>
    <div>
      <header class="d-flex justify-space-between">
        <h1><span class="color">예금</span> 검색하기</h1>
        <div class="w-25">
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
        <div v-if="selectedDeposit" class="card py-5 px-3 modal-content">
          <div class="card-title d-flex align-center justify-space-between">
            <h3>{{ selectedDeposit['금융 상품명'] }}</h3>
            <div v-if="userStore.isLogin">
              <button
                v-if="isLikeDeposit"
                @click.prevent="deleteDepositUser"
                class="red-button"
              >
                관심 등록 취소
              </button>
              <button
                v-else
                @click.prevent="addDepositUser"
                class="blue-button"
              >
                관심 상품 등록
              </button>
            </div>
          </div>

          <div class="card-text">
            <table>
              <tbody>
                <tr v-for="(value, key) in selectedDeposit" :key="key">
                  <td width="28%" class="font-weight-bold">{{ key }}</td>
                  <td v-if="key === '최고 한도'">{{ value?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") }}</td>
                  <td v-else>{{ value }}</td>
                </tr>
              </tbody>
            </table>
            <hr class="my-3">
            <div class="mx-auto">
              <BarChartDetail
                :title="selectedDepositSimple.fin_prdt_nm"
                :average-intr-rate="averageIntrRate"
                :intr-rate="intrRate"
                :intr-rate2="intrRate2"
              />
              <p class="text-caption">* 개월별 평균 예금 금리는 2024년 4월 기준입니다.</p>
            </div>
          </div>

          <div class="card-actions">
            <button @click="close" class="btn" style="color: #1089FF;">
              닫기
            </button>
          </div>
        </div>
      </div>

      <div v-if="depositLength !== 0" class="table-container" >
        <table class="table elevation-6">
          <thead>
            <tr>
              <th>공시월</th>
              <th>은행명</th>
              <th class="text-center" align="cetner">상품명</th>
              <th align="center">6개월</th>
              <th align="center">12개월</th>
              <th align="center">24개월</th>
              <th align="center">36개월</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in deposits" :key="item.deposit_code" @click="clickRow(item)">
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
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useUserStore } from '@/stores/user'
  import BarChartDetail from '@/components/BarChartDetail.vue'
  import axios from 'axios'

  const headers = [
{ title: '공시 제출일', align: 'start', sortable: false, width:'10%', key: 'dcls_month' },
{ title: '금융회사명', align: 'start', sortable: false, key: 'kor_co_nm' },
{ title: '상품명', align: 'center', sortable: false, width:'32%', key: 'fin_prdt_nm' },
{ title: '6개월', align: 'end', width:'12%', key: '6month' },
{ title: '12개월 ', align: 'end', width:'12%', key: '12month' },
{ title: '24개월', align: 'end', width:'12%', key: '24month' },
{ title: '36개월', align: 'end', width:'12%', key: '36month' },
]
const API_URL = 'http://localhost:8000/accounts'
const deposits = ref([])
const depositLength = computed(() => {
return deposits.value.length
})
const banks = ref(['전체 보기'])
const selectedBank = ref('전체 보기')
const selectedDepositSimple = ref(null)
const selectedDeposit = ref()
const selectedDepositCode = computed(() => {
  return selectedDepositSimple.value?.['deposit_code']
})
console.log(selectedDepositCode)
const dialog = ref(false)

const averageIntrRate = [3.45, 4.08, 3.4, 3.35]
const intrRate = ref([null, null, null, null])
const intrRate2 = ref([null, null, null, null])

const userStore = useUserStore()
const router = useRouter()
const likeList = ref([])

const isLikeDeposit = computed(() => {
  return likeList.value?.some(e => e['deposit_code'] === selectedDepositCode.value)
})

const makeItems = function (item) {
const result = {
  'deposit_code': item['deposit_code'],
  'dcls_month': item['dcls_month'],
  'kor_co_nm': item['kor_co_nm'],
  'fin_prdt_nm': item['fin_prdt_nm'],
  '6month': null,
  '12month': null,
  '24month': null,
  '35month': null,
}

const options = Array.isArray(item['depositoption_set']) ? item['depositoption_set'] : []

for (const option of options) {
  const saveTrm = option['save_trm']

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

return result
}

const getAllDeposit = function () {
axios({
  method: 'get',
  url: `${userStore.API_URL}/finance/deposit_list/`
})
  .then((res) => {
      const results = res.data
      deposits.value = results.map(makeItems)
      const bankSet = new Set(banks.value)
      results.forEach(item => bankSet.add(item['kor_co_nm']))
      banks.value = Array.from(bankSet)
  })
  .catch((err) => {
    console.log(err)
  })
}

onMounted(() => {
  getAllDeposit()
})

const clickBank = function () {
if (selectedBank.value === '전체 보기') {
  getAllDeposit()
} else {
  axios({
    method: 'get',
    url: `${userStore.API_URL}/finance/get_bank_deposit/${selectedBank.value}/`
  })
    .then((res) => {
        deposits.value = res.data.map(makeItems)
    })
    .catch((err) => {
      console.log(err)
    })
}
}

const close = function () {
  dialog.value = false
}

const clickRow = function (data) {
  selectedDepositSimple.value = data
  console.log('Selected Deposit Simple:', selectedDepositSimple.value)  // 확인을 위한 로그
  console.log('Selected Deposit Code:', selectedDepositCode.value)  // 확인을 위한 로그
  intrRate.value = []
  intrRate2.value = []
  getDeposit()
  getDepositLikeList()
  // console.log(likeList)
  dialog.value = true
}

const getDeposit = function () {
axios({
  method: 'get',
  url: `${userStore.API_URL}/finance/deposit_list/${selectedDepositCode.value}/`
})
  .then((res) => {
    const data = res.data
    // console.log(res.data)
    selectedDeposit.value = {
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
    const optionList = res.data.depositoption_set

    for (const option of optionList) {
      if (option.save_trm === "6") {
        intrRate.value[0] = option.intr_rate
        intrRate2.value[0] = option.intr_rate2
      } else if (option.save_trm === "12") {
        intrRate.value[1] = option.intr_rate
        intrRate2.value[1] = option.intr_rate2
      } else if (option.save_trm === "24") {
        intrRate.value[2] = option.intr_rate
        intrRate2.value[2] = option.intr_rate2
      } else if (option.save_trm === "36") {
        intrRate.value[3] = option.intr_rate
        intrRate2.value[3] = option.intr_rate2
      }
    }
  })
  .catch((err) => {
    console.log(err)
  })
}

const addDepositUser = function () {
    axios({
      method: 'post',
      url: `${userStore.API_URL}/finance/deposit_list/${selectedDepositCode.value}/like/`,
      headers: {
        Authorization: `Token ${userStore.token}`
      }
    }).then(response => {
      console.log('예금 저장 완료')
      getDepositLikeList()
    }).catch(error => {
      console.log('예금 저장 오류 발생', error)
    })
}

const getDepositLikeList = function () {
  axios ({
    method: 'get',
    url: `${userStore.API_URL}/finance/deposit_list/${selectedDepositCode.value}/like/`,
    headers: {
        Authorization: `Token ${userStore.token}`
      }
  }).then(response => {
    likeList.value = response.data
  }).catch(error => {
    console.log('오류 발생', error)
  })
}


const deleteDepositUser = function () {
  axios({
    method: 'delete',
    url: `${userStore.API_URL}/finance/deposit_list/${selectedDepositCode.value}/like/`,
    headers: {
      Authorization: `Token ${userStore.token}`
    }
  }).then(() => {
    console.log('삭제 완료')
    getDepositLikeList()
  }).catch(error => {
    console.log('오류 발생', error)
  })
}

</script>
  
<style lang="scss" scoped>
.red-button {
  background-color: red;
  color: white;
  border-radius: 8px; /* 모서리를 네모로 만듭니다. */
  padding: 10px 20px; /* 버튼의 크기와 여백을 조정합니다. */
  border: none; /* 테두리를 없앱니다. */
  white-space: nowrap; /* 텍스트 줄 바꿈을 금지합니다. */
  cursor: pointer; /* 마우스 커서를 포인터로 변경합니다. */
}
.blue-button {
  background-color: blue;
  color: white;
  border-radius: 8px; /* 모서리를 네모로 만듭니다. */
  padding: 10px 20px; /* 버튼의 크기와 여백을 조정합니다. */
  border: none; /* 테두리를 없앱니다. */
  white-space: nowrap; /* 텍스트 줄 바꿈을 금지합니다. */
  cursor: pointer; /* 마우스 커서를 포인터로 변경합니다. */
}
.custom-select {
  border: 2px solid #7a17a1; /* Bootstrap 기본 파란색 */
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
  box-shadow: 0 0 0 0.2rem rgba(195, 0, 255, 0.25);
}

.dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  margin-top: 45px;
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