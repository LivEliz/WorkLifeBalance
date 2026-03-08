import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";
import { FaUserAlt, FaLock } from "react-icons/fa";

export default function Login(){

  const navigate = useNavigate();

  const [data,setData] = useState({
    email:"",
    password:""
  });

  const handleSubmit = async(e)=>{
    e.preventDefault();

    const res = await login(data);

    localStorage.setItem("token",res.data.access_token);
    localStorage.setItem("email",data.email);

    navigate("/weekly-checkin");
  }

  return (

<div style={{
display:"flex",
height:"100vh",
fontFamily:"Segoe UI"
}}>


{/* LEFT SIDE DESIGN PANEL */}

<div style={{
flex:1,
background:"linear-gradient(135deg,#0A4D8C,#2F80ED)",
color:"white",
display:"flex",
flexDirection:"column",
justifyContent:"center",
alignItems:"center",
padding:"40px"
}}>

<h1 style={{
fontSize:"42px",
marginBottom:"10px",
textAlign:"center"
}}>
WorkLife Balance
</h1>

<p style={{
fontSize:"18px",
textAlign:"center",
maxWidth:"350px"
}}>
AI powered system to monitor employee well-being and maintain a healthy work-life balance.
</p>

<div style={{
marginTop:"40px",
fontSize:"80px"
}}>
💼
</div>

</div>


{/* RIGHT SIDE LOGIN FORM */}

<div style={{
flex:1,
display:"flex",
justifyContent:"center",
alignItems:"center",
background:"#EAF4FF"
}}>

<form
onSubmit={handleSubmit}
style={{
background:"white",
padding:"40px",
borderRadius:"12px",
width:"350px",
boxShadow:"0 10px 25px rgba(0,0,0,0.15)"
}}
>

<h2 style={{
textAlign:"center",
marginBottom:"30px",
color:"#0A4D8C"
}}>
Login
</h2>


{/* EMAIL */}

<div style={{
display:"flex",
alignItems:"center",
border:"1px solid #ccc",
borderRadius:"8px",
padding:"8px",
marginBottom:"20px"
}}>

<FaUserAlt style={{marginRight:"8px",color:"#0A4D8C"}}/>

<input
placeholder="Email"
style={{
border:"none",
outline:"none",
width:"100%"
}}
onChange={(e)=>setData({...data,email:e.target.value})}
/>

</div>


{/* PASSWORD */}

<div style={{
display:"flex",
alignItems:"center",
border:"1px solid #ccc",
borderRadius:"8px",
padding:"8px",
marginBottom:"25px"
}}>

<FaLock style={{marginRight:"8px",color:"#0A4D8C"}}/>

<input
type="password"
placeholder="Password"
style={{
border:"none",
outline:"none",
width:"100%"
}}
onChange={(e)=>setData({...data,password:e.target.value})}
/>

</div>


{/* BUTTON */}

<button
type="submit"
style={{
width:"100%",
padding:"12px",
background:"#2F80ED",
border:"none",
borderRadius:"8px",
color:"white",
fontSize:"16px",
cursor:"pointer"
}}
>
Login
</button>

</form>

</div>

</div>

  );
}