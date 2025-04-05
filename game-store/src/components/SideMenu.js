import "./components.css";
export function SideMenu(){

    return (
        <div id="Side">
        <h2>Genres</h2>
        <ul id="sideMenu">
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/6162/6162583.png" width="30px" height="30px"/></span><span className="text">Action</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/2790/2790402.png" width="30px" height="30px"/></span><span className="text">Adventure</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/3175/3175163.png" width="30px" height="30px"/></span><span className="text">Casual</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/5564/5564944.png" width="30px" height="30px"/></span><span className="text">Sport</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/5894/5894904.png" width="30px" height="30px"/></span><span className="text">Strategy</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/8028/8028014.png" width="30px" height="30px"/></span><span className="text">Multiplayer games</span></li>
            <li><span><img src="https://cdn-icons-png.flaticon.com/512/2665/2665513.png" width="30px" height="30px"/></span><span className="text">Racing</span></li>
        </ul>
        </div>
    );
}