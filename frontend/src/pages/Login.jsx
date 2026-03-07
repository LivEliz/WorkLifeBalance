import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/api";

export default function Login(){

  const navigate = useNavigate();

  const [data,setData] = useState({
    email:"",
    password:""
  });

  const handleSubmit = async(e)=>{
    e.preventDefault();

    const res = await login(data);

    localStorage.setItem("token",res.data.token);

    navigate("/weekly-checkin");
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Login</h2>

      <input
        placeholder="Email"
        onChange={(e)=>setData({...data,email:e.target.value})}
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>setData({...data,password:e.target.value})}
      />

      <button type="submit">Login</button>
    </form>
  );
}