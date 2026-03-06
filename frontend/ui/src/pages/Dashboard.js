import { useEffect,useState } from "react";

function Dashboard(){

const [data,setData]=useState(null)

useEffect(()=>{

const result=localStorage.getItem("result")

if(result){
setData(JSON.parse(result))
}

},[])

if(!data) return <h2>Loading...</h2>

return(

<div className="p-10">

<h1 className="text-3xl font-bold mb-6">
Stress Prediction Result
</h1>

<div className="grid grid-cols-3 gap-6">

<div className="bg-red-100 p-6 rounded">
<h2>Stress Level</h2>
<p className="text-2xl">{data.stress_level}</p>
</div>

<div className="bg-blue-100 p-6 rounded">
<h2>Risk Score</h2>
<p className="text-2xl">{data.score}</p>
</div>

</div>

<div className="mt-8 bg-green-100 p-6 rounded">

<h2 className="text-xl font-bold mb-3">
AI Suggestions
</h2>

<p>{data.suggestions}</p>

</div>

</div>

)

}

export default Dashboard