import React from "react";

function ProgressBars() {

  const data = [
    { label: "Workload", value: 60 },
    { label: "Recovery", value: 70 },
    { label: "Health", value: 55 },
    { label: "Personal Life", value: 65 }
  ];

  return (

    <div>

      {data.map((item) => (

        <div key={item.label} className="mb-4">

          <p>{item.label}</p>

          <div className="w-full bg-gray-200 rounded">

            <div
              className="bg-green-500 text-white text-xs p-1 rounded"
              style={{ width: `${item.value}%` }}
            >
              {item.value}%
            </div>

          </div>

        </div>

      ))}

    </div>
  );
}

export default ProgressBars;