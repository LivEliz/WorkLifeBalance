import { useState } from "react";
import { questions } from "../data/questions";
import axios from "axios";

function Questionnaire() {

  const [step, setStep] = useState(0);
  const [answers, setAnswers] = useState({});
  const [selected, setSelected] = useState(null);

  const current = questions[step];

  const selectOption = (value) => {
    setSelected(value); // highlight selected option
    setAnswers({
      ...answers,
      [current.id]: value
    });
  };

  const next = () => {

    if (!selected) {
      alert("Please select an option");
      return;
    }

    setSelected(null);

    if (step < questions.length - 1) {
      setStep(step + 1);
    } else {
      submitAnswers();
    }
  };

  const submitAnswers = async () => {
    try {
      const res = await axios.post(
        "http://localhost:5000/predict",
        answers
      );

      localStorage.setItem("result", JSON.stringify(res.data));
      window.location = "/dashboard";

    } catch (err) {
      console.error(err);
      alert("Backend connection failed");
    }
  };

  return (

    <div className="flex justify-center items-center h-screen bg-gray-100">

      <div className="bg-white p-10 rounded-xl shadow-xl w-2/3 text-center">

        <h2 className="text-xl font-bold mb-6">
          Question {step + 1} / {questions.length}
        </h2>

        <p className="text-lg mb-8">{current.question}</p>

        {current.options.map((opt) => (

          <button
            key={opt}
            onClick={() => selectOption(opt)}
            className={`block w-full p-3 mb-3 border rounded-lg transition 
            ${selected === opt ? "bg-blue-500 text-white" : "hover:bg-blue-100"}`}
          >
            {opt}
          </button>

        ))}

        <button
          onClick={next}
          className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          Next →
        </button>

      </div>

    </div>

  );
}

export default Questionnaire;