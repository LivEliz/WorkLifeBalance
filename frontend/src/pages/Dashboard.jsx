import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";

function Dashboard(){

  const [trend,setTrend] = useState(null);
  const [result,setResult] = useState(null);
  const [loading,setLoading] = useState(true);

  useEffect(()=>{

    const saved = localStorage.getItem("latest_result");

    if(saved){
      setResult(JSON.parse(saved));
    }

    async function loadTrend(){

      try{
        const res = await getDashboard();
        setTrend(res.data);
      }
      catch(err){
        console.log("Trend API failed:",err);
      }

      setLoading(false);
    }

    loadTrend();

  },[]);


  if(loading){
    return <p style={{padding:"30px"}}>Loading dashboard...</p>;
  }


  return(

    <div style={{padding:"30px"}}>

      <h2>Work Life Balance Dashboard</h2>


      {/* ---------------- ML RESULT ---------------- */}

      {result ? (

        <div style={{marginTop:"20px"}}>

          <h3>Work Life Balance Score</h3>

          <h1>{result.wlb_score}</h1>

          <p>Status: {result.wlb_label}</p>

          <p>Confidence: {result.confidence}%</p>

        </div>

      ) : (

        <p>No weekly check-in data yet.</p>

      )}



      {/* ---------------- AI RECOMMENDATIONS ---------------- */}

      {result?.recommendations?.length > 0 && (

        <div style={{marginTop:"30px"}}>

          <h3>AI Recommendations</h3>

          <ul>
            {result.recommendations.map((r,i)=>(
              <li key={i}>{r}</li>
            ))}
          </ul>

        </div>

      )}



      {/* ---------------- WEEKLY CHECKLIST ---------------- */}

      {result?.weekly_checklist?.length > 0 && (

        <div style={{marginTop:"30px"}}>

          <h3>Suggested Weekly Checklist</h3>

          <ul>
            {result.weekly_checklist.map((item,i)=>(
              <li key={i}>{item}</li>
            ))}
          </ul>

        </div>

      )}



      {/* ---------------- TREND ANALYSIS ---------------- */}

      <div style={{marginTop:"40px"}}>

        <h3>Trend Analysis</h3>

        {trend?.message ? (

          <p>{trend.message}</p>

        ) : (

          <>
            <p>Current Score: {trend?.current_wlb_score ?? "N/A"}</p>
            <p>Previous Score: {trend?.previous_wlb_score ?? "N/A"}</p>
            <p>Trend: {trend?.trend ?? "N/A"}</p>
            <p>Change: {trend?.change ?? "N/A"}</p>
          </>

        )}

      </div>



      {/* ---------------- LAST 5 WEEKS ---------------- */}

      {trend?.last_5_weeks?.length > 0 && (

        <div style={{marginTop:"30px"}}>

          <h3>Last 5 Weeks Scores</h3>

          <ul>
            {trend.last_5_weeks.map((score,index)=>(
              <li key={index}>{score}</li>
            ))}
          </ul>

        </div>

      )}

    </div>

  );

}

export default Dashboard;