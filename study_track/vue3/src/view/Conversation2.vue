<template>
  <div class="page-container">
    <div class="left-section">
      <div class="form-group">
        <label for="action-select">请选择具体行为:</label>
        <select id="action-select" v-model="selectedAction">
          <option>学会拒绝</option>
		  <option>拍马屁</option>
		  <option>总结发言</option>
		  <option>道喜</option>
          <!-- Add more options as needed -->
        </select>
      </div>

      <div class="helper-section">
        <p>帮你的社交小助手选择一个人设吧:</p>
        <textarea readonly>{{ helperText }}</textarea>
        <button @click="dislikeCharacter">我不喜欢，换一个</button>
      </div>
    </div>

    <div class="right-section">
      <div class="response-box">
        <p>好的, 请提供具体的请求内容和你想要拒绝的原因...</p>
        <textarea readonly>{{ responseText }}</textarea>
      </div>
      <textarea v-model="userInput" placeholder="请你重新生成一个..."></textarea>
      <div class="button-group">
        <button @click="clearRecords">删除记录</button>
        <button @click="submit">发送</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      selectedAction: "学会拒绝",
      helperText: `你是一个善于化解"尴尬"场合的专家，当你想委婉的拒绝别人的请求时，你能够考虑到请求者与你的社会关系，以一些合理的理由，用高情商、委婉含蓄的语句回绝请求。下面我将给你提供请求者的称呼、请求者跟我的关系、我的称呼、请求我的内容这些信息，请你根据这些信息，从我的角度出发帮我委婉含蓄、拒绝请求。
请求者的称呼、请求者跟我的关系、我的称呼、请求我的内容`, // Insert the full text here
      responseText: `好的, 请提供具体的请求内容...`, // Insert the full text here
      userInput: ""
    };
  },
  methods: {
    dislikeCharacter() {
      // Logic to change the helper text
      this.helperText = "换一个新的角色介绍a...";
	  this.helperText = "换一个新的角色介绍b...";
    },
    clearRecords() {
      this.userInput = "";
    },
    submit() {
      // Submit form logic
	  //console.log(result);
	  axios.post('http://127.0.0.1:8000/chat/',{"prompt":this.userInput,"history":'',"system":'你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。在处理问题时，你应当考虑到文化背景、社会规范和个人情感，以帮助用户更好地理解复杂的人际关系和社会互动。'})
			.then(result=>{
				this.responseText=result.data.result
				console.log(result)
			})
      
    }
  }
};
</script>

<style scoped>
.page-container {
  display: flex;
  justify-content: space-around;
  padding: 50px 20px; /* 增加顶部的内边距 */
  background-color: #f0f4ff;
  height: 85vh;
}

.left-section {
  width: 20%; /* 更宽的宽度 */
  height: 80%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.right-section {
  width: 60%; /* 较窄的宽度 */
  height: 80%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 18px;
  color: #1d2975;
}

select {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  margin-top: 10px;
}

.helper-section {
  margin-top: 20px;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  margin-top: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  margin-top: 10px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #1d2975;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.response-box p {
  background-color: #e0ebff;
  padding: 10px;
  border-radius: 5px;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
