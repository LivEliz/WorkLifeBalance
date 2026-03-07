import { useEffect, useState } from "react";
import { saveProfile } from "../services/api";

function ProfileSetup(){

  const [profile,setProfile] = useState({

    email:"",

    age_group:"",
    marital_status:"",
    children:"",

    department:"",
    role_level:"",

    work_mode:"",
    official_work_hours:"",
    commute_time:""
  });

  useEffect(()=>{

    const email = localStorage.getItem("email");

    if(email){
      setProfile(prev => ({...prev, email}));
    }

  },[]);


  const handleSubmit = async(e)=>{

    e.preventDefault();

    await saveProfile(profile);

    alert("Profile saved");

    window.location.href="/weekly-checkin";
  };


  return(

  <form onSubmit={handleSubmit}>

    <h2>Profile Setup</h2>

    <p>Email: {profile.email}</p>

    <h3>Personal Context</h3>

    <select onChange={(e)=>setProfile({...profile,age_group:e.target.value})}>
      <option value="">Select Age Group</option>
      <option value="18-25">18-25</option>
      <option value="26-35">26-35</option>
      <option value="36-45">36-45</option>
      <option value="46-55">46-55</option>
      <option value="55+">55+</option>
    </select>


    <select onChange={(e)=>setProfile({...profile,marital_status:e.target.value})}>
      <option value="">Marital Status</option>
      <option value="Single">Single</option>
      <option value="Married">Married</option>
      <option value="Divorced / Separated">Divorced / Separated</option>
      <option value="Widowed">Widowed</option>
      <option value="Prefer not to say">Prefer not to say</option>
    </select>


    <select onChange={(e)=>setProfile({...profile,children:e.target.value})}>
      <option value="">Children</option>
      <option value="No children">No children</option>
      <option value="1 child">1 child</option>
      <option value="2 children">2 children</option>
      <option value="3 or more children">3 or more children</option>
    </select>


    <h3>Work Context</h3>

    <input
      placeholder="Department"
      onChange={(e)=>setProfile({...profile,department:e.target.value})}
    />

    <input
      placeholder="Role Level"
      onChange={(e)=>setProfile({...profile,role_level:e.target.value})}
    />


    <h3>Work Structure</h3>

    <select onChange={(e)=>setProfile({...profile,work_mode:e.target.value})}>
      <option value="">Work Mode</option>
      <option value="Work From Home">Work From Home</option>
      <option value="Hybrid">Hybrid</option>
      <option value="Office Only">Office Only</option>
    </select>


    <select onChange={(e)=>setProfile({...profile,official_work_hours:e.target.value})}>
      <option value="">Work Hours</option>
      <option value="8 AM – 4 PM">8 AM – 4 PM</option>
      <option value="9 AM – 5 PM">9 AM – 5 PM</option>
      <option value="10 AM – 6 PM">10 AM – 6 PM</option>
      <option value="11 AM – 7 PM">11 AM – 7 PM</option>
      <option value="Rotational Shift">Rotational Shift</option>
      <option value="Night Shift">Night Shift</option>
    </select>


    <h3>Commute</h3>

    <select onChange={(e)=>setProfile({...profile,commute_time:e.target.value})}>
      <option value="">Commute Time</option>
      <option value="No commute (Work From Home)">No commute (Work From Home)</option>
      <option value="Less than 30 minutes">Less than 30 minutes</option>
      <option value="30 – 60 minutes">30 – 60 minutes</option>
      <option value="1 – 2 hours">1 – 2 hours</option>
      <option value="More than 2 hours">More than 2 hours</option>
    </select>

    <button type="submit">Save Profile</button>

  </form>

  );
}

export default ProfileSetup;