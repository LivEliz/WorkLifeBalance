import { Link } from "react-router-dom";

export default function Welcome() {
  return (
    <div className="container">
      <h1>LifeBalance AI</h1>
      <p>
        AI powered system that analyzes your work habits and lifestyle
        to provide personalized work-life balance insights.
      </p>

      <Link to="/login">
        <button>Login</button>
      </Link>

      <Link to="/signup">
        <button>Signup</button>
      </Link>
    </div>
  );
}