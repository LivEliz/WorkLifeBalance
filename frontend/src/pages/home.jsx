import { useNavigate } from "react-router-dom";

export default function Home(){

  const navigate = useNavigate();

  const result = localStorage.getItem("latest_result");

  const openDashboard = () => {

    if(!result){
      alert("Please complete the weekly questionnaire first.");
      navigate("/weekly-checkin");
    }
    else{
      navigate("/dashboard");
    }

  };

  return(

  <div style={{
    height:"100vh",
    display:"flex",
    justifyContent:"center",
    alignItems:"center",
    background:"linear-gradient(135deg,#EAF4FF,#D6E8FF)",
    fontFamily:"Segoe UI"
  }}>

  <div style={{
    background:"white",
    padding:"50px",
    borderRadius:"16px",
    boxShadow:"0 10px 30px rgba(0,0,0,0.15)",
    textAlign:"center",
    width:"420px"
  }}>

  <h1 style={{color:"#0A4D8C"}}>
  LifeBalance AI
  </h1>

  <p style={{marginBottom:"30px",color:"#555"}}>
  Choose what you would like to do
  </p>

  <button
  onClick={()=>navigate("/weekly-checkin")}
  style={{
    width:"100%",
    padding:"12px",
    marginBottom:"15px",
    background:"#2F80ED",
    color:"white",
    border:"none",
    borderRadius:"8px",
    cursor:"pointer",
    fontSize:"16px"
  }}
  >
  Start Weekly Questionnaire
  </button>

  <button
  onClick={openDashboard}
  style={{
    width:"100%",
    padding:"12px",
    background:"#0A4D8C",
    color:"white",
    border:"none",
    borderRadius:"8px",
    cursor:"pointer",
    fontSize:"16px"
  }}
  >
  View Dashboard
  </button>

  </div>
  </div>

  );
}