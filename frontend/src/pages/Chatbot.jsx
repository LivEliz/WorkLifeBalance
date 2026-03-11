import { useState } from "react";
import axios from "axios";

function Chatbot(){

const [messages,setMessages] = useState([]);
const [input,setInput] = useState("");
const [typing,setTyping] = useState(false);

const sendMessage = async () => {

if(!input.trim()) return;

const userMessage = {role:"user", text:input};

setMessages(prev => [...prev,userMessage]);
setInput("");
setTyping(true);

try{

const res = await axios.post(
"http://localhost:8000/chatbot",
{message: userMessage.text},
{
headers:{
Authorization:`Bearer ${localStorage.getItem("token")}`
}
}
);

const aiMessage = {
role:"ai",
text:res.data.reply
};

setMessages(prev => [...prev, aiMessage]);

}
catch(err){

setMessages(prev => [...prev,{
role:"ai",
text:"Sorry, something went wrong."
}]);

}

setTyping(false);

};

return(

<div style={{maxWidth:"700px",margin:"auto"}}>

<h2 style={{textAlign:"center"}}>AI Work-Life Assistant</h2>

<div style={{
height:"400px",
overflowY:"auto",
border:"1px solid #ccc",
padding:"15px",
borderRadius:"10px"
}}>

{messages.map((msg,index)=>(

<div
key={index}
style={{
textAlign: msg.role==="user" ? "right" : "left",
marginBottom:"10px"
}}
>

<span
style={{
display:"inline-block",
background: msg.role==="user" ? "#0A4D8C" : "#eee",
color: msg.role==="user" ? "white" : "black",
padding:"10px 15px",
borderRadius:"15px"
}}
>

{msg.text}

</span>

</div>

))}

{typing && (
<p style={{color:"gray"}}>AI is typing...</p>
)}

</div>

<div style={{display:"flex",marginTop:"10px"}}>

<input
value={input}
onChange={(e)=>setInput(e.target.value)}
placeholder="Type your message..."
style={{flex:1,padding:"10px"}}
/>

<button
onClick={sendMessage}
style={{
padding:"10px 20px",
background:"#0A4D8C",
color:"white",
border:"none"
}}
>

Send

</button>

</div>

</div>

);

}

export default Chatbot;