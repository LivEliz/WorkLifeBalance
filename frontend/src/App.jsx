import { BrowserRouter, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Profile from "./pages/Profile";
import ProfileSetup from "./pages/ProfileSetup";
import Signup from "./pages/Signup";
import Home from "./pages/home";
import WeeklyCheckin from "./pages/WeeklyCheckin";
import Welcome from "./pages/Welcome";
import Chatbot from "./pages/Chatbot";
import FloatingChatbot from "./components/FloatingChatbot";

function App() {
  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Welcome />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/profile-setup" element={<ProfileSetup />} />

        <Route path="/home" element={<Home />} />

        <Route path="/weekly-checkin" element={<WeeklyCheckin />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>

      {/* Floating AI Assistant visible on all pages */}
      <FloatingChatbot />

    </BrowserRouter>
  );
}

export default App;