<template>
  <div class="chatbot">
    <h1>챗봇</h1>
    <div class="chat-history">
      <div v-for="(chat, index) in chatHistory" :key="index" :class="chat.sender">
        <h2>{{ chat.sender }}:</h2>
        <p>{{ chat.message }}</p>
      </div>
    </div>
    <textarea v-model="message" placeholder="궁금한 내용을 물어보세요!"></textarea>
    <button @click="sendMessage">보내기</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
      chatHistory: [
        // Initialize chat history with previous conversation data
        { sender: 'User', message: 'Hi there!' },
        { sender: 'Chatbot', message: 'Hello! How can I help you today?' }
      ]
    };
  },
  methods: {
    sendMessage() {
      // Add user message to chat history
      this.chatHistory.push({ sender: 'User', message: this.message });

      // Send user message to backend and get response
      axios.post('http://127.0.0.1:8000/CGPT/', { message: this.message })
        .then(res => {
          // Add chatbot response to chat history
          this.chatHistory.push({ sender: 'Chatbot', message: res.data.response });
          this.message = ''; // Clear the input field
        })
        .catch(err => {
          console.error(err);
          alert('An error occurred. Check console for details.');
        });
    }
  }
};
</script>

<style>
.chatbot {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ccc;
}
.chat-history {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 1rem;
}
.chat-history .User {
  text-align: right;
  background-color: #f1f1f1;
  padding: 0.5rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}
.chat-history .Chatbot {
  text-align: left;
  background-color: #e1e1e1;
  padding: 0.5rem;
  border-radius: 0.5rem;
  margin-bottom: 0.5rem;
}
textarea {
  width: 100%;
  height: 100px;
}
button {
  display: block;
  margin-top: 10px;
}
</style>
