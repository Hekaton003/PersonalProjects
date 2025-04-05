import listofgames from "../listofgames";
import {useEffect, useState} from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faWindows, faPlaystation, faXbox} from '@fortawesome/free-brands-svg-icons';
import { faHeart } from "@fortawesome/free-solid-svg-icons";
import HoverVideoPlayer from 'react-hover-video-player';
import videoArray from "./video";
export function Games(){
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [selectGameId,setSelectedGame]=useState(null);
    const array=['Windows','PlayStation','Xbox'];
    const [liked,setLiked]=useState({});
    function addBlock(e){
        setSelectedCategory(e.target.value);
        if(selectGameId!==null){
        setSelectedGame(null);
        localStorage.setItem("game"," ");}
    }
    useEffect(() => {
        addBlock({ target: { value: 'all' } });
    }, []);
    useEffect(()=>{
        const SelectedGame=localStorage.getItem("game");
        setSelectedGame(parseInt(SelectedGame));
    },[selectGameId])
    const filteredGames = listofgames.filter(item => selectedCategory === 'all' || item.category === selectedCategory);
    function Likebutton(e){
        setLiked((prev)=>({
            ...prev,[e]:!liked[e],
        }));
    }
    return (
        <div id="game">
            <h1>Games</h1>
            <select onChange={(e)=>addBlock(e)} id="selectMenu">
                <option></option>
                <option value="all">All Games</option>
                <option value="action">Action</option>
                <option value="adventure">Adventure</option>
                <option value="casual">Casual</option>
                <option value="multiplayer">Multiplayer games</option>
                <option value="sport">Sport</option>
                <option value="strategy">Strategy</option>
                <option value="racing">Racing</option>
            </select>
            <div id="mainblock">
                {selectGameId?
                    <div className="block" >
                        <HoverVideoPlayer className="videos"
                           videoSrc={videoArray[selectGameId-1]}
                           style={{width:"400px",height:"200px"}}
                           pausedOverlay={
                               <img src={listofgames[selectGameId-1].image} style={{objectFit:"cover"}} alt='game-picture' width='400px' height='200px'/>
                           }
                            loop={true}
                            muted={false}
                        />
                        <h3>{listofgames[selectGameId-1].name}</h3>
                        <div className="platform-icons">
                            {array.map(platform => (
                                <FontAwesomeIcon key={platform} icon={getPlatformIcon(platform)} className="platform-icon"/>
                            ))}
                        </div>
                        <div className="likedbutton">
                        <button onClick={()=>Likebutton(listofgames[selectGameId-1].id)} className="likebutton">
                            <FontAwesomeIcon icon={faHeart} style={{color:liked[selectGameId]?'red':'black'}} className="heart"/>
                        </button>
                        </div>
                    </div>
                    :filteredGames.map(item => (
                    <div key={item.id} className="block">
                        <HoverVideoPlayer
                            className="videos"
                            videoSrc={videoArray[item.id-1]}
                            style={{width:"400px",height:"200px"}}
                            pausedOverlay={
                            <img src={item.image} style={{objectFit:"cover"}} alt='game-picture' width='400px' height='200px'/>
                            }
                            loop={true}
                            muted={false}
                        />
                        <h3>{item.name}</h3>
                        <div className="platform-icons">
                            {array.map(platform => (
                                <FontAwesomeIcon key={platform} icon={getPlatformIcon(platform)} className="platform-icon"/>
                            ))}
                        </div>
                        <div className="likedbutton">
                        <button onClick={()=>Likebutton(item.id)}>
                            <FontAwesomeIcon icon={faHeart} style={{color:liked[item.id]?'red':'black'}}  className="heart"/>
                        </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
function getPlatformIcon(platform) {
    switch (platform) {
        case 'Windows':
            return faWindows;
        case 'PlayStation':
            return faPlaystation;
        case 'Xbox':
            return faXbox;
        default:
            return null;
    }
}