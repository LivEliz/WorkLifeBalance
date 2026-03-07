import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { submitWeekly } from "../services/api";

function WeeklyCheckin() {

  const navigate = useNavigate();

  const [data, setData] = useState({
    email: "",

    hours_worked: "",
    overtime_hours: "",
    projects_handled: "",
    meetings_count: "",

    workload_rating: 1,
    deadline_pressure: 1,

    productivity_rating: 1,
    task_delay: "Never",

    breaks: "",
    break_duration: "",

    sick_days: "",
    leave_days: "",
    exhaustion_rating: 1,

    travel: "No travel",
    travel_enjoyment: 3,

    family_time: "",
    social_satisfaction: 3
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const email = localStorage.getItem("email");
    if (email) {
      setData(prev => ({ ...prev, email }));
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const res = await submitWeekly(data);

    localStorage.setItem("latest_result", JSON.stringify(res.data));

    navigate("/dashboard");
  };

  return (
    <form onSubmit={handleSubmit}>

      <h2>Weekly Check-In</h2>

      <p>Email: {data.email}</p>

      <h3>Workload</h3>

      <select onChange={(e) => setData({ ...data, hours_worked: e.target.value })}>
        <option value="">Total Hours Worked</option>
        <option value="<35">Less than 35 hours</option>
        <option value="35-40">35 – 40 hours</option>
        <option value="40-45">40 – 45 hours</option>
        <option value="45-50">45 – 50 hours</option>
        <option value=">50">More than 50 hours</option>
      </select>

      <select onChange={(e) => setData({ ...data, overtime_hours: e.target.value })}>
        <option value="">Overtime Hours</option>
        <option value="None">None</option>
        <option value="1-5">1 – 5 hours</option>
        <option value="6-10">6 – 10 hours</option>
        <option value="11-15">11 – 15 hours</option>
        <option value=">15">More than 15 hours</option>
      </select>

      <select onChange={(e) => setData({ ...data, projects_handled: e.target.value })}>
        <option value="">Projects Handled</option>
        <option value="1">1 project</option>
        <option value="2-3">2 – 3 projects</option>
        <option value="4-5">4 – 5 projects</option>
        <option value="6-8">6 – 8 projects</option>
        <option value=">8">More than 8 projects</option>
      </select>

      <select onChange={(e) => setData({ ...data, meetings_count: e.target.value })}>
        <option value="">Meetings Attended</option>
        <option value="0-5">0 – 5 meetings</option>
        <option value="6-10">6 – 10 meetings</option>
        <option value="11-15">11 – 15 meetings</option>
        <option value="16-20">16 – 20 meetings</option>
        <option value=">20">More than 20 meetings</option>
      </select>

      <h3>Work Pressure</h3>

      <label>Workload Felt Excessive</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, workload_rating: Number(e.target.value) })
        }
      />

      <label>Unrealistic Deadlines</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, deadline_pressure: Number(e.target.value) })
        }
      />

      <h3>Productivity</h3>

      <label>Productivity During Work</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, productivity_rating: Number(e.target.value) })
        }
      />

      <select onChange={(e) => setData({ ...data, task_delay: e.target.value })}>
        <option value="Never">Never</option>
        <option value="Rarely">Rarely</option>
        <option value="Sometimes">Sometimes</option>
        <option value="Often">Often</option>
        <option value="Always">Always</option>
      </select>

      <h3>Breaks</h3>

      <select onChange={(e) => setData({ ...data, breaks: e.target.value })}>
        <option value="">Breaks per day</option>
        <option value="None">No breaks</option>
        <option value="1">1 break</option>
        <option value="2">2 breaks</option>
        <option value="3">3 breaks</option>
        <option value="4+">4 or more breaks</option>
      </select>

      <select onChange={(e) => setData({ ...data, break_duration: e.target.value })}>
        <option value="">Break Duration</option>
        <option value="<10">Less than 10 minutes</option>
        <option value="10-20">10 – 20 minutes</option>
        <option value="20-30">20 – 30 minutes</option>
        <option value="30-45">30 – 45 minutes</option>
        <option value=">45">More than 45 minutes</option>
      </select>

      <h3>Health</h3>

      <select onChange={(e) => setData({ ...data, sick_days: e.target.value })}>
        <option value="">Sick Days</option>
        <option value="None">None</option>
        <option value="1">1 day</option>
        <option value="2">2 days</option>
        <option value="3">3 days</option>
        <option value="4+">4 or more days</option>
      </select>

      <select onChange={(e) => setData({ ...data, leave_days: e.target.value })}>
        <option value="">Leave Days</option>
        <option value="None">None</option>
        <option value="1">1 day</option>
        <option value="2">2 days</option>
        <option value="3">3 days</option>
        <option value="4+">4 or more days</option>
      </select>

      <label>Exhaustion Level</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, exhaustion_rating: Number(e.target.value) })
        }
      />

      <h3>Work Travel</h3>

      <select onChange={(e) => setData({ ...data, travel: e.target.value })}>
        <option value="No travel">No travel</option>
        <option value="1 trip">1 trip</option>
        <option value="2 trips">2 trips</option>
        <option value="3 trips">3 trips</option>
        <option value=">3 trips">More than 3 trips</option>
      </select>

      <label>Travel Experience</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, travel_enjoyment: Number(e.target.value) })
        }
      />

      <h3>Personal Life</h3>

      <select onChange={(e) => setData({ ...data, family_time: e.target.value })}>
        <option value="">Family Time</option>
        <option value="<3">Less than 3 hours</option>
        <option value="3-5">3 – 5 hours</option>
        <option value="6-10">6 – 10 hours</option>
        <option value="11-15">11 – 15 hours</option>
        <option value=">15">More than 15 hours</option>
      </select>

      <label>Social Satisfaction</label>
      <input
        type="range"
        min="1"
        max="5"
        onChange={(e) =>
          setData({ ...data, social_satisfaction: Number(e.target.value) })
        }
      />

      <br /><br />

      <button type="submit">
        {loading ? "Analyzing..." : "Submit Weekly Check-In"}
      </button>

    </form>
  );
}

export default WeeklyCheckin;