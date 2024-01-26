<template>
    <div>
    <h2>Predictor Component</h2>
    <div>
      <input v-model="userInputPAQ605" placeholder="PAQ605" />
      <input v-model="userInputBMXBMI" placeholder="BMXBMI" />
      <input v-model="userInputLBXGLU" placeholder="LBXGLU" />
      <input v-model="userInputDIQ010" placeholder="DIQ010" />
      <input v-model="userInputLBXGLT" placeholder="LBXGLT" />
      <input v-model="userInputLBXIN" placeholder="LBXIN" />
      <button @click="runPrediction">Run Prediction</button>
    </div>
    <button @click="chooseModel">Choose Model</button>
    <button @click="uploadData">Upload Data</button>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" placeholder="Password" />

    <div v-if="predictionResult">
      <h3>Prediction Result</h3>
      <p>{{ predictionResult.message }}</p>
    </div>

    <div v-if="chosenModelMessage">
      <h3>Choose Model Result</h3>
      <p>{{ chosenModelMessage.message }}</p>
    </div>

    <div v-if="uploadDataMessage">
      <h3>Upload Data Result</h3>
      <p>{{ uploadDataMessage.message }}</p>
    </div>

    <div>
      <h3>Get Prediction Result</h3>
      <input v-model="predictionId" placeholder="Prediction ID" />
      <button @click="getPredictionResult">Get Prediction Result</button>
      <div v-if="predictionResultById">
        <p>{{ predictionResultById.message }}</p>
      </div>
    <div>
      <h3>Models</h3>
      <button @click="getAvailableModels">Get Available Models</button>
      <div v-if="availableModels">
        <h4>Available Models</h4>
        <ul>
          <li v-for="model in availableModels" :key="model.model_id">{{ model.description }}</li>
        </ul>
      </div>

      <button @click="getUserBalance">Get User Balance</button>
      <div v-if="userBalance">
        <h4>User Balance</h4>
        <p>{{ userBalance.message }}</p>
      </div>

      <button @click="getUserTransactionHistory">Get User Transaction History</button>
      <div v-if="userTransactionHistory">
        <h4>User Transaction History</h4>
        <ul>
          <li v-for="transaction in userTransactionHistory" :key="transaction.transaction_id">{{ transaction.amount }}</li>
        </ul>
      </div>
   <div>
      <h3>Authentication</h3>
      <button @click="signIn">Sign In</button>
      <div v-if="signInResponse">
        <h4>Sign In Response</h4>
        <p>{{ signInResponse.access_token }}</p>
      </div>

      <button @click="signUp">Sign Up</button>
      <div v-if="signedUpUser">
        <h4>Signed Up User</h4>
        <p>{{ signedUpUser.login }}</p>
      </div>

      <button @click="getMe">Get User Information</button>
      <div v-if="userInfo">
        <h4>User Information</h4>
        <p>{{ userInfo.login }}</p>
      </div>
    </div>
  </div>
</template>      

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      userInputPAQ605: '',
      userInputBMXBMI: '',
      userInputLBXGLU: '',
      userInputDIQ010: '',
      userInputLBXGLT: '',
      userInputLBXIN: '',
      predictionResult: null,
      chosenModelMessage: null,
      uploadDataMessage: null,
      predictionId: '',
      predictionResultById: null,
      availableModels: null,
      userBalance: null,
      userTransactionHistory: null,
      signInResponse: null,
      signedUpUser: null,
      userInfo: null,
    };
  },


methods: {
  async signIn() {
    try {
      const response = await axios.post('YOUR_BACKEND_URL/auth/sign-in', {
        username: this.username,
        password: this.password,
      });
      this.signInResponse = response.data;

      // Save the token in local storage
      localStorage.setItem('access_token', this.signInResponse.access_token);
    } catch (error) {
      console.error('Error signing in:', error);
      // Display a user-friendly error message to the user
      this.signInResponse = { error: 'Failed to sign in. Please check your credentials and try again.' };
    }
  },

  async signUp() {
    try {
      const response = await axios.post('YOUR_BACKEND_URL/auth/sign-up', {
        username: this.username,
        password: this.password,
      });
      this.signedUpUser = response.data;

      // Save the token in local storage
      localStorage.setItem('access_token', this.signedUpUser.access_token);
    } catch (error) {
      console.error('Error signing up:', error);
      // Display a user-friendly error message to the user
      this.signedUpUser = { error: 'Failed to sign up. Please try again.' };
    }
  },

  async runPrediction() {
    try {
      const token = localStorage.getItem('access_token');
      const userInputData = {
        PAQ605: this.userInputPAQ605,
        BMXBMI: this.userInputBMXBMI,
        LBXGLU: this.userInputLBXGLU,
        DIQ010: this.userInputDIQ010,
        LBXGLT: this.userInputLBXGLT,
        LBXIN: this.userInputLBXIN,
      };

      const response = await axios.post('YOUR_BACKEND_URL/predictor/run_prediction', {
        input_data: userInputData,
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      this.predictionResult = response.data;
    } catch (error) {
      console.error('Error running prediction:', error);
      // Display a user-friendly error message to the user
      this.predictionResult = { error: 'Failed to run prediction. Please try again.' };
    }
  },

  async chooseModel() {
    try {
      const response = await axios.post('YOUR_BACKEND_URL/predictor/choose_model', {
        // Include any necessary data for the choose_model endpoint
        model_id: 1, // Replace with the actual model ID
      });

      this.chosenModelMessage = response.data;
    } catch (error) {
      console.error('Error choosing model:', error);
      // Display a user-friendly error message to the user
      this.chosenModelMessage = { error: 'Failed to choose model. Please try again.' };
    }
  },

  async uploadData() {
    try {
      const response = await axios.post('YOUR_BACKEND_URL/predictor/upload-data', {
        model_id: 1, // Replace with the actual model ID
        data: {
          // Include your data properties here
        },
      });

      this.uploadDataMessage = response.data;
    } catch (error) {
      console.error('Error uploading data:', error);
      // Display a user-friendly error message to the user
      this.uploadDataMessage = { error: 'Failed to upload data. Please try again.' };
    }
  },

  async getPredictionResult() {
    try {
      const response = await axios.get(
        `YOUR_BACKEND_URL/predictor/get-prediction-result/${this.predictionId}`
      );

      this.predictionResultById = response.data;
    } catch (error) {
      console.error('Error getting prediction result:', error);
      // Display a user-friendly error message to the user
      this.predictionResultById = { error: 'Failed to get prediction result. Please try again.' };
    }
  },

  async getAvailableModels() {
    try {
      const response = await axios.get('YOUR_BACKEND_URL/models/info');
      this.availableModels = response.data;
    } catch (error) {
      console.error('Error getting available models:', error);
      // Display a user-friendly error message to the user
      this.availableModels = { error: 'Failed to get available models. Please try again.' };
    }
  },

  async getUserBalance() {
    try {
      const response = await axios.get('YOUR_BACKEND_URL/models/balance');
      this.userBalance = response.data;
    } catch (error) {
      console.error('Error getting user balance:', error);
      // Display a user-friendly error message to the user
      this.userBalance = { error: 'Failed to get user balance. Please try again.' };
    }
  },

  async getUserTransactionHistory() {
    try {
      const response = await axios.get('YOUR_BACKEND_URL/models/history');
      this.userTransactionHistory = response.data;
    } catch (error) {
      console.error('Error getting user transaction history:', error);
      // Display a user-friendly error message to the user
      this.userTransactionHistory = { error: 'Failed to get user transaction history. Please try again.' };
    }
  },

  async getMe() {
    try {
      const response = await axios.get('YOUR_BACKEND_URL/auth/me');
      this.userInfo = response.data;
    } catch (error) {
      console.error('Error getting user information:', error);
      // Display a user-friendly error message to the user
      this.userInfo = { error: 'Failed to get user information. Please try again.' };
    }
  },
},

</script>

<style scoped>
/* Add your component styles here */
</style>

