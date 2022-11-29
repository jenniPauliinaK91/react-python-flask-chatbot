
import '../App.css';
import { useState, useRef, useEffect } from 'react';
import { Message } from './msg';
import axios from 'axios'

export const Home=()=>{


    const [chatstate, setChatstate]=useState({
        chat:[],
        msg:'',
      })
    const viestienLoppu= useRef(null)
    const scrollToBottom =()=>{
        viestienLoppu.current.scrollIntoView({behaviour:"smooth"})
    }
    useEffect(scrollToBottom, [chatstate])

    const inputChange=(e)=>{
        setChatstate({...chatstate, msg:e.target.value})      
      }
   
     const lahetaViesti=(e)=>{   
       e.preventDefault() 
       if(chatstate.msg!==''){
          axios.post('http://127.0.0.1:5000/getReply', {'msg':chatstate.msg})
          .then(res=>{
            let chats=chatstate.chat
            chats.push({from:'user', message:chatstate.msg})
            chats.push({from:'bot', message:res.data})
           setChatstate({chat:chats, msg:''})
            console.log(chatstate)
    
          })
          .catch(err=>{
            console.log(err);
        })
       }
       let interval = window.setInterval(function(){
        var elem = document.getElementById('ch');
        elem.scrollTop = elem.scrollHeight;
        window.clearInterval(interval);
    },1000)

      }
      
        return(
       
          <div className="container">
           <div id="otsikko">Proto chatbot</div>
          
           <div id="ch" className="chatContainer">
             <div className='iconcontainer'><div id="icon"></div><div className={chatstate.chat==''?'robotmesg':'robotmesg hide'}>Hi! Ask me anything about our ski center!</div></div>
            <div className='messagesContainer'>
              {
                chatstate.chat.map((m, k)=>{
                  return  <Message key={k} msg={m.message} from={m.from}/>
                })
               
              }
           <div id="tyhja" ref={viestienLoppu} />
          
            </div>
           
              <div className="myInput">
                
                  <input value={chatstate.msg} placeholder='Kirjoita viesti..' name="mess" onChange={inputChange}></input>
                  <button id='sendBtn' onClick={lahetaViesti}>SEND</button>
                
              </div>
       
          </div>
        </div>
           )
  
}
