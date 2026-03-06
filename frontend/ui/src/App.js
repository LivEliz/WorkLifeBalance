import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Questionnaire from "./pages/Questionnaire";
import WeeklyCheckin from "./pages/WeeklyCheckin";

function App() {
  return (
    <BrowserRouter>

      <Routes>

        {/* Login page (first page) */}
        <Route path="/" element={<Login />} />

        {/* Pages after login */}
        <Route
          path="/questionnaire"
          element={
            <>
              <Navbar />
              <Questionnaire />
            </>
          }
        />

        <Route
          path="/dashboard"
          element={
            <>
              <Navbar />
              <Dashboard />
            </>
          }
        />

        <Route
          path="/weekly"
          element={
            <>
              <Navbar />
              <WeeklyCheckin />
            </>
          }
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;