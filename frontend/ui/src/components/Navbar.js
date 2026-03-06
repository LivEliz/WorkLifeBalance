import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="bg-blue-600 text-white p-4 flex justify-between">

      <h1 className="text-xl font-bold">
        WorkLife Balance
      </h1>

      <div className="space-x-4">
        <Link to="/">Questionnaire</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/weekly">Weekly Check‑in</Link>
      </div>

    </div>
  );
}

export default Navbar;