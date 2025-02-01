// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth"; // Firebase Authをインポート

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: process.env.VUE_APP_FIREBASE_API_KEY as string,
  authDomain: process.env.VUE_APP_FIREBASE_AUTH_DOMAIN as string,
  projectId: process.env.VUE_APP_FIREBASE_PROJECT_ID as string,
  storageBucket: process.env.VUE_APP_FIREBASE_STORAGE_BUCKET as string,
  messagingSenderId: process.env.VUE_APP_FIREBASE_MESSAGING_SENDER_ID as string,
  appId: process.env.VUE_APP_FIREBASE_APP_ID as string
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);

const auth = getAuth(app); // Firebase Authenticationを初期化

export { auth };
