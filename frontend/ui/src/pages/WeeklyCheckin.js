import { useState } from "react";
import { submitWeeklyCheckin } from "../services/api";

function WeeklyCheckin() {

  const [stress, setStress] = useState("");

  const submit = async () => {

    await submitWeeklyCheckin({ stress });

    alert("Weekly check-in submitted");
  };

  return (

    <div className="p-10">

      <h1 className="text-3xl font-bold mb-5">
        Weekly Check‑in
      </h1>

      <input
        placeholder="Stress level this week"
        onChange={(e) => setStress(e.target.value)}
        className="border p-2 mb-3 block"
      />

      <button
        onClick={submit}
        className="bg-green-500 text-white px-5 py-2 rounded"
      >
        Submit
      </button>

    </div>
  );
}

export default WeeklyCheckin;