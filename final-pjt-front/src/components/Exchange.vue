<script setup>
import { ref, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const API_URL = import.meta.env.VITE_APP_API_URL

const currencies = ref([])
const response = ref([])
const selectedState = ref('송금 받으실 때')
const selectedCurrency = ref('미국 달러')
const selectedCurrencyUnit = ref('USD')
const selectedTtb = ref()
const selectedTts = ref()
const selectedDeal = ref()
const calculateVariable = ref()
const krwInput = ref()
const otherInput = ref()

const states = ['송금 받으실 때', '송금 보내실 때', '매매 기준율']

const emit = defineEmits(['passCurrency'])

onMounted(() => {
  axios.get(`${API_URL}/exchange/`)
    .then((res) => {
      response.value = res.data.filter(data => data.ttb !== '0')
      currencies.value = response.value.map(item => item.cur_nm)
      const units = response.value.map(item => item.cur_unit)
      emit('passCurrency', currencies.value, units)
      const usdInfo = response.value.find(item => item.cur_nm === '미국 달러')
      selectedTtb.value = Number(usdInfo.ttb.replaceAll(',', ''))
      selectedTts.value = Number(usdInfo.tts.replaceAll(',', ''))
      selectedDeal.value = Number(usdInfo.deal_bas_r.replaceAll(',', ''))
      calculateVariable.value = selectedTtb.value
    })
})

watch(selectedCurrency, () => {
  const selectedInfo = response.value.find(item => item.cur_nm === selectedCurrency.value)
  selectedCurrencyUnit.value = selectedInfo.cur_unit
  if (selectedCurrency.value === '일본 옌' || selectedCurrency.value === "인도네시아 루피아") {
    selectedCurrencyUnit.value = selectedCurrencyUnit.value.replace('(100)', '')
    selectedTtb.value = Number(selectedInfo.ttb.replaceAll(',', '')) / 100
    selectedTts.value = Number(selectedInfo.tts.replaceAll(',', '')) / 100
    selectedDeal.value = Number(selectedInfo.deal_bas_r.replaceAll(',', '')) / 100
  } else {
    selectedTtb.value = Number(selectedInfo.ttb.replaceAll(',', ''))
    selectedTts.value = Number(selectedInfo.tts.replaceAll(',', ''))
    selectedDeal.value = Number(selectedInfo.deal_bas_r.replaceAll(',', ''))
  }
  if (selectedState.value === '송금 받으실 때') {
    calculateVariable.value = selectedTtb.value
  } else if (selectedState.value === '송금 보내실 때') {
    calculateVariable.value = selectedTts.value
  } else {
    calculateVariable.value = selectedDeal.value
  }
  inputEventOther()
})

watch(selectedState, () => {
  if (selectedState.value === '송금 받으실 때') {
    calculateVariable.value = selectedTtb.value
  } else if (selectedState.value === '송금 보내실 때') {
    calculateVariable.value = selectedTts.value
  } else {
    calculateVariable.value = selectedDeal.value
  }
  inputEventOther()
})

const roundToTwo = (num) => {
  return +(Math.round(num + 'e+2') + 'e-2')
}

const inputEventKrw = function () {
  otherInput.value = krwInput.value / calculateVariable.value
  otherInput.value = roundToTwo(otherInput.value)
}

const inputEventOther = function () {
  krwInput.value = otherInput.value * calculateVariable.value
  krwInput.value = roundToTwo(krwInput.value)
}
</script>

<template>
  <div class="card">
    <form class="form">
      <div class="form-group">
        <label for="state-select">기준</label>
        <select id="state-select" v-model="selectedState" class="form-control">
          <option v-for="state in states" :key="state" :value="state">{{ state }}</option>
        </select>
      </div>

      <div class="form-group">
        <label for="currency-select">통화 선택</label>
        <select id="currency-select" v-model="selectedCurrency" class="form-control">
          <option v-for="currency in currencies" :key="currency" :value="currency">{{ currency }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="krw-input">KRW(원)</label>
        <input type="number" id="krw-input" v-model="krwInput" @input="inputEventKrw" class="form-control" />
      </div>
      <div class="form-group">
        <label :for="selectedCurrencyUnit">통화 금액</label>
        <input type="number" :id="selectedCurrencyUnit" v-model="otherInput" @input="inputEventOther" class="form-control" />
      </div>

    
    </form>
  </div>
</template>

<style >
.card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 500px;
  margin: 0 auto;
}

.form {
  &-group {
    margin-bottom: 1.5rem;

    label {
      font-size: 0.9rem;
      font-weight: bold;
      color: #333;
      margin-bottom: 0.5rem;
    }

    .form-control {
      width: 100%;
      padding: 0.75rem 1rem;
      font-size: 1rem;
      border: 1px solid #ccc;
      border-radius: 4px;
      transition: border-color 0.3s ease;

      &:focus {
        outline: none;
        border-color: #007bff;
      }
    }
  }
}

@media (max-width: 768px) {
  .card {
    padding: 1.5rem;
  }

  .form {
    &-group {
      margin-bottom: 1.2rem;

      label {
        font-size: 0.85rem;
      }

      .form-control {
        padding: 0.6rem 0.9rem;
        font-size: 0.9rem;
      }
    }
  }
}
</style>
