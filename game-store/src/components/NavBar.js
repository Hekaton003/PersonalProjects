import "./components.css";
import listofgames from "../listofgames";
export function NavBar(){
    function Autocomplete(data){
       const value=data.target.value;
        const autocomplete=document.getElementById("autocomplete");
       const filterArray=listofgames.filter((item)=>{
           return item.name.toLowerCase().includes(value.toLowerCase())
       })
       autocomplete.innerHTML=" ";
        for (let i = 0; i <filterArray.length ; i++) {
            const list=document.createElement("li");
            list.innerHTML=filterArray[i].name;
            list.onclick=()=>SelectGame(filterArray[i]);
            autocomplete.append(list);
            if(i===8){
               break;
            }
        }
       if(filterArray.length>0){
           autocomplete.style.display="block";
       }else{
           autocomplete.style.display="none";
       }

    }
    function SelectGame(data){
       localStorage.setItem("game",data.id.toString());
       document.getElementById("searchbar").value = data.name;
       document.getElementById("autocomplete").style.display="none";
        window.location.reload();
    }
    return(
        <div id="nav">
          <img src="https://3.bp.blogspot.com/-0bhjBzXmO28/VDxl-TLPE_I/AAAAAAAAFlY/dBNYzvK7iaE/s1600/Logo%2BGames.png" width="200px" height="150px"/>
          <input type="text" id="searchbar" placeholder="search for games" onChange={(e)=>Autocomplete(e)}/>
            <ul id="autocomplete"></ul>
        </div>
    );
}