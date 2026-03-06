import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000"
});

export const submitQuestionnaire = (data) =>
  API.post("/questionnaire", data);

export const getDashboardData = () =>
  API.get("/dashboard");

export const submitWeeklyCheckin = (data) =>
  API.post("/weekly", data);