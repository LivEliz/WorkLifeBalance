import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getDashboard } from "../services/api";
import bg from "../assets/bg_wlb.png"; 

export default function Home(){

  const navigate = useNavigate();
  const [hasData,setHasData] = useState(false);

  useEffect(()=>{

    async function checkUserData(){
      try{
        const res = await getDashboard();

        if(res.data && !res.data.message){
          setHasData(true);
        }
      }
      catch(err){
        console.log("Dashboard check failed");
      }
    }

    checkUserData();

  },[]);

  const goToDashboard = () => {

    if(!hasData){
      alert("Please complete the questionnaire first.");
      return;
    }

    navigate("/dashboard");
  };

  const goToQuestionnaire = () => {
    navigate("/weekly-checkin");
  };

  return(

  <div style={{
    height:"100vh",
    display:"flex",
    justifyContent:"center",
    alignItems:"center",
    background:"linear-gradient(135deg,#EAF4FF,#D6E8FF)",
    backgroundImage: `url(${bg})`,
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
  Choose where you want to go
  </p>

  <button
  onClick={goToQuestionnaire}
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
  Go to Questionnaire
  </button>

  <button
  onClick={goToDashboard}
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
  Go to Dashboard
  </button>

  </div>
  </div>

  );
}