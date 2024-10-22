import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from './user' 
import { useRouter } from 'vue-router'

export const useArticleStore = defineStore('article', () => {
  const articles = ref([])
  const store = useUserStore()
  const router = useRouter()
  const API_URL = 'http://127.0.0.1:8000'
  const getArticles = function () {
    if (!store.token) {
      // console.error('User is not authenticated.')
      alert('로그인 후 이용 가능합니다.')
      router.push({ name: 'signin' })
      return
    }

    console.log('Token:', store.token) // 토큰 확인
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      headers: {
        Authorization: `Token ${store.token}`,
      }
    })
    .then(res => articles.value = res.data)
    .catch(error => {
      if (error.response && error.response.status === 401) {
        alert('You are not authorized to view this content. Please log in.')
      } else {
        console.error('Error fetching articles:', error)
      }
    })
  }

  const createArticle = function (title, content) {
    if (!store.token) {
      console.error('User is not authenticated.')
      alert('Please log in to create an article.')
      return
    }
    const userConfirmed = confirm('작성을 완료하시겠습니까?')
    if (!userConfirmed){
      console.log('User cancelled article creation.')
      return
    }



    console.log('Token:', store.token) // 토큰 확인
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v1/articles/',
      data: {
        title,
        content
      },
      headers: {
        Authorization: `Token ${store.token}`,
      }
    })
    .then(res => {
      console.log('Article created successfully')
      getArticles()
      console.log(res)
    })
    .catch(error => {
      if (error.response && error.response.status === 401) {
        alert('You are not authorized to create an article. Please log in.')
      } else {
        console.error('Error creating article:', error)
      }
    })
  }

  return { articles, getArticles, createArticle ,API_URL}
})
