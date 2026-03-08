import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../services/api";

export default function Signup() {

  const navigate = useNavigate();

  const [form,setForm] = useState({
    name:"",
    age:0,
    email:"",
    password:""
  });

  const handleSubmit = async(e)=>{

    e.preventDefault();

    const res = await signup(form);

    localStorage.setItem("token", res.data.access_token);
    localStorage.setItem("email", form.email);

    navigate("/profile-setup");
  };

  return (

  <div className="page-container">

    <div className="form-card">

      <h2 className="page-title">Create Your Account</h2>

      <form onSubmit={handleSubmit} className="form-layout">

        <input
          placeholder="Name"
          onChange={(e)=>setForm({...form,name:e.target.value})}
        />

        <input
          type="number"
          placeholder="Age"
          onChange={(e)=>setForm({...form,age:parseInt(e.target.value)})}
        />

        <input
          placeholder="Email"
          onChange={(e)=>setForm({...form,email:e.target.value})}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e)=>setForm({...form,password:e.target.value})}
        />

        <button type="submit">
          Create Account
        </button>

      </form>

    </div>

  </div>

  );
}