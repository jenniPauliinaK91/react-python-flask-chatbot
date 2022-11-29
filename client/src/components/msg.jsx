
import '../App.css';
export const Message=(props)=>{
    return(
        <div className= {props.from=="user"? "message you":"message chatbot"}>
            <p>{props.msg}</p>
        </div>
    )


}