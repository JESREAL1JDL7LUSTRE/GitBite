import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // Update with your backend URL

const AXIOS_API = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default AXIOS_API;
