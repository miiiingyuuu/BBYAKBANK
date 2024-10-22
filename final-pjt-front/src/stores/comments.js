import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useUserStore } from './user' 
import { useRouter,useRoute } from 'vue-router'

export const useCommentStore = defineStore('comment', () => {
    const comments = ref([])
    const store = useUserStore()
    const router = useRouter()
    const route = useRoute()
    const API_URL = 'http://127.0.0.1:8000'

    const getComments = function(){
        axios({
            method: 'get',
            url: `http://127.0.0.1:8000/api/v1/articles/${route.params.id}`,
            // headers: {
            //   Authorization: `Token ${store.token}`,
            // }
          })
          .then(res => comments.value = res.data)
          .catch(err=>{
            console.log(err)
          })
    }
    const createComment = function(){}

    return{getComments}
})