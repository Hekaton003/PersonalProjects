
import './App.css';
import {useEffect, useState} from "react";

function App() {
  const ClientId="5ef2df401d05453ebd83de63be1d5e6b";
  const ClientSecret="2dbdafae1b854d88be2d81e0d2084d64";
  const [tokenAccess,setTokenAccess]=useState(" ");
  const [inputSearch,setInputSearch]=useState(" ");
  const [albums,setAlbums]=useState([]);
  const [isFull,setIsFull]=useState(false);
  const [songs,setSongs]=useState([]);
  const [val,setVal]=useState(false);
  const [favSongs,setFavSongs]=useState([])
  useEffect(function (){
    let params={
      method:"POST",
      headers: {
        'Content-type':'application/x-www-form-urlencoded'
      },
      body:'grant_type=client_credentials&client_id='+ClientId+'&client_secret='+ClientSecret
    }
     fetch('https://accounts.spotify.com/api/token',params).then(response=>response.json())
        .then(data=>setTokenAccess(data.access_token));
  },[]);
  async function search(){
    console.log("Search for "+ inputSearch);
    let Searchparams={
        method: "GET",
        headers: {
            'Content-type':'application/json',
            'Authorization':'Bearer '+tokenAccess,
        },
    }
    let artistID= await fetch("https://api.spotify.com/v1/search?q="+inputSearch+"&type=artist",Searchparams).then(response=>response.json())
        .then((data)=>{return data.artists.items[0].id});
    let par1=await fetch("https://api.spotify.com/v1/artists/"+artistID+"/albums"+"?include_groups=album&market=US&limit=20",Searchparams).then(response=>response.json())
        .then((data)=>{setAlbums(data.items)});
    setIsFull(true)

  }
  async function getSongs(id){
      let params={
          method: "GET",
          headers: {
              'Content-type':'application/json',
              'Authorization':'Bearer '+tokenAccess,
          },
      }
      let par2=await fetch("https://api.spotify.com/v1/albums/"+id+"/tracks",params).then(response=>response.json())
          .then((data)=>setSongs(data.items));
     setVal(true)
  }
  function addFavoriteSongs(song){
      for (let i = 0; i <favSongs.length ; i++) {
          if(favSongs[i]===song){
              return null;
          }
      }
      setFavSongs((prev)=>[...prev,song])
  }
  return (
    <div className='App'>
        {console.log(albums)}
        <header>
            <h1>Spotify Playlist</h1>
        </header>
        <main>
            <input type="text" placeholder="Insert your favourite artist" onKeyPress={(event)=>{if(event.key=="Enter")search()}} onChange={(event)=>setInputSearch(event.target.value)}/>
            <button onClick={()=>search()}>Search</button>
        </main>
        { isFull?
            <>

                <ul id="container">
                    <h2>List of Albums</h2>
                    {albums.map((album,i)=>{
                        return (
                            <li key={i} id={album.id} onClick={()=>getSongs(album.id)}>
                                <h3>{album.name}</h3><img src={album.images[1].url}/>
                            </li>
                        );
                    })}
                </ul>
                { val?
                    <ul id="songs">
                    <h2>List of Songs</h2>
                    {songs.map((item,i)=>{
                        return(
                            <li key={i} onClick={()=>addFavoriteSongs(item.name)} >{item.name}</li>
                        )
                     })
                    }
                    </ul>
                    :
                    null
                }
                {
                    favSongs.length>0?
                        <ul id="fav">
                            <h2>List of Favourite Songs</h2>
                            {
                                favSongs.map((item,i)=>{
                                    return(
                                        <li key={i}>{item}</li>
                                    )
                                })
                            }
                        </ul>
                        :
                        null
                }
            </>
            :null
        }
    </div>
  );
}

export default App;
