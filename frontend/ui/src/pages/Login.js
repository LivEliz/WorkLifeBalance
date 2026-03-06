import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login(){

const navigate = useNavigate();

const [user,setUser] = useState({
name:"",
password:""
})

const handleChange=(e)=>{
setUser({...user,[e.target.name]:e.target.value})
}

const login=()=>{
if(user.name && user.password){
navigate("/questionnaire")
}
}

return(

<div className="flex items-center justify-center h-screen bg-blue-50">

<div className="bg-white p-10 rounded-xl shadow-xl w-96 text-center">

<img
src="https://cdn-icons-png.flaticon.com/512/3209/3209265.png"
alt="stress"
className="w-24 mx-auto mb-4"
/>

<h1 className="text-3xl font-bold mb-6">
Work‑Life Balance AI
</h1>

<input
name="name"
placeholder="Name"
onChange={handleChange}
className="border p-3 mb-4 w-full rounded"
/>

<input
type="password"
name="password"
placeholder="Password"
onChange={handleChange}
className="border p-3 mb-6 w-full rounded"
/>

<button
onClick={login}
className="bg-blue-600 text-white px-6 py-3 rounded w-full hover:bg-blue-700"
>

Login

</button>

</div>

</div>

)

}

export default Login