<script setup>
import { ref } from "vue";
const buttonDisabled = ref(true);
const file = ref(null);
const fileEvent = ref(null);
const result = ref(null);

const onClick = async () => {
  const formData = new FormData();
  formData.append("file", fileEvent.value);
  const response = await fetch("http://localhost:5180/predict", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  result.value = data;
};

const onUpload = (event) => {
  result.value = null;
  fileEvent.value = event.target.files[0];
  if (!fileEvent.value) {
    return;
  }
  const reader = new FileReader();
  reader.readAsDataURL(fileEvent.value);
  reader.onload = (event) => {
    file.value = event.target.result;
    buttonDisabled.value = false;
    result.value = null;
  };
};
</script>

<template>
  <div class="home">
    <div class="home-title">
      <h1>Fake Landscape Detector</h1>
      <p>
        This is a simple web app that uses a machine learning model to detect
        whether an image is a real landscape or not.
      </p>
    </div>
    <div class="home-instructions">
      <p>
        <strong>Instructions:</strong> Upload an image and click the button to
        see if it is a real landscape or not.
      </p>
      <div class="home-buttons">
        <input
          class="file-input"
          type="file"
          accept="image/*"
          @change="onUpload"
        />
        <button
          v-show="!buttonDisabled"
          @click="onClick"
          class="predict-button"
        >
          Predict
        </button>
      </div>
      <div class="home-image">
        <img
          v-if="file"
          :src="file"
          style="max-height: 500px; margin-top: 1rem"
        />
      </div>
    </div>
    <div v-if="result" class="home-result" style="font-size: 1.25rem">
      <p>
        <strong>Result:</strong>
        <span
          :style="{
            color: result.prediction === 'FAKE' ? 'red' : 'green',
            marginLeft: '0.5rem',
          }"
          >{{ result.prediction }}</span
        >
        ({{ result.probability }})
      </p>
    </div>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.home-title {
  text-align: center;
  margin-bottom: 2rem;
}

.home-instructions {
  text-align: center;
  margin-bottom: 2rem;
}

.home-buttons {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.file-input {
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  border: 1px solid #686de0;
  cursor: pointer;
}

.predict-button {
  margin-left: 1rem;
  background-color: #686de0;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
}
</style>
