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
    <form onSubmit={handleSubmit}>
      <h2>Signup</h2>

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

      <button type="submit">Create Account</button>
    </form>
  );
}

