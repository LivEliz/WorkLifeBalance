import { Link } from "react-router-dom";

export default function Welcome() {
  return (

    <div className="welcome-container">

      <div className="welcome-card">

        <div className="welcome-icon">
          ⚖️
        </div>

        <h1 className="welcome-title">
          LifeBalance AI
        </h1>

        <p className="welcome-text">
          AI powered system that analyzes your work habits and lifestyle
          to provide personalized work-life balance insights.
        </p>

        <div className="welcome-buttons">

          <Link to="/login">
            <button className="primary-btn">Login</button>
          </Link>

          <Link to="/signup">
            <button className="secondary-btn">Signup</button>
          </Link>

        </div>

      </div>

    </div>
  );
}