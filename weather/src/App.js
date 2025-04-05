
import './App.css';
import {useEffect, useState} from "react";
import { DateTime } from 'luxon';
function App() {
    const [city,setCity]=useState(" ");
    const [temp,setTemp]=useState(" ");
    const [desc,setDesc]=useState(" ");
    const [subdesc,setSubdesc]=useState(" ");
    const [loading,setLoading]=useState(false);
    const [source,setSrc]=useState(" ");
    const [weatherForecast, setWeatherForecast] = useState([]);
    let apiKey="0e1b89f829f61ea774f59b340fb67b69";
    useEffect(() => {
        // This effect will run whenever subdesc or source changes
        console.log("sdesc:", subdesc);
        console.log("Image Source:", source);
        if (subdesc !== " " && source !== " ") {
            setLoading(true);
        }
    }, [subdesc, source]);

// Function to get the current time in the timezone of a given city

    async function search(){
        let response=await fetch("https://api.openweathermap.org/data/2.5/forecast?q="+city+"&appid="+apiKey).then((data)=>data.json());
        const timezone=response.city.timezone/3600;
        const localDateTime = DateTime.local();
        const cityDateTime = localDateTime.plus({ hours: timezone });
        const currentDate = new Date(cityDateTime.toJSDate());
        let closestDataPoint = response[0];
        console.log(currentDate)// Initialize with the first data point
        let minTimeDifference = Infinity;
        for (let i = 0; i < response.list.length; i++) {
            const currentDataPoint = response.list[i];
            const currentDateTime = new Date(currentDataPoint.dt_txt);
                const timeDifference = Math.abs(currentDateTime - currentDate);
                if (timeDifference < minTimeDifference) {
                    closestDataPoint = currentDataPoint;
                    minTimeDifference = timeDifference;
                }
            
        }
        console.log(closestDataPoint)
        const array=Next(new Date(),response.list);
        setWeatherForecast(array);
        // Now use the closest data point
        setTemp((closestDataPoint.main.temp - 273.15).toFixed(0).toString());
        setDesc(closestDataPoint.weather[0].description);
        let chour = new Date(closestDataPoint.dt_txt).getHours();
        console.log(chour)
        setSubdesc(closestDataPoint.weather[0].main);
        if (subdesc === "Rain") {
            setSrc("https://cdn-icons-png.flaticon.com/512/3520/3520675.png"); // Adjust the path as needed
        }else if (desc === "scattered clouds" || desc==="overcast clouds") {
            if (chour >= 6 && chour < 18) {
                setSrc("https://cdn-icons-png.flaticon.com/512/5904/5904053.png");
            } else {
                setSrc("https://cdn-icons-png.flaticon.com/512/2387/2387889.png");
            }
        }else if (subdesc === "Clear"){
            if(chour>=6 && chour<18) {
                setSrc("https://cdn-icons-png.flaticon.com/512/869/869869.png");
            }else {
                setSrc("https://cdn-icons-png.flaticon.com/512/581/581601.png");
            }
        } else if (subdesc === "Snow") {
            setSrc("https://cdn-icons-png.flaticon.com/512/9755/9755252.png"); // Adjust the path as needed
        }else if(subdesc=="Clouds") {
            setSrc("https://cdn-icons-png.flaticon.com/512/704/704845.png"); // Adjust the path as needed
        }

    }
    function Next(currentDate,array){
        const next5DaysForecast = [];

        for (let i = 0; i < array.length; i++) {
            const dataPoint = array[i];
            const dataPointDate = new Date(dataPoint.dt_txt);
            // Check if the data point is for the next day
            if (dataPointDate.getDate() !== currentDate.getDate() && dataPointDate.getHours()===12) {
                next5DaysForecast.push({
                    date: dataPointDate.toLocaleDateString(),
                    temperature: (dataPoint.main.temp - 273.15).toFixed(0),
                    description: dataPoint.weather[0].description,
                    icon: getWeatherIcon(dataPoint.weather[0].description,dataPoint.weather[0].main),
                });

                // Move to the next day
                currentDate.setDate(currentDate.getDate() + 1);
            }

            // Break the loop when we have data for the next 5 days
            if (next5DaysForecast.length === 5) {
                break;
            }
        }

        return next5DaysForecast;
    }
    function getWeatherIcon(subdesc,desc){
        if (desc === 'Rain') {
            return "https://cdn-icons-png.flaticon.com/512/3520/3520675.png"; // Adjust the path as needed
        }else if (subdesc === 'scattered clouds' || subdesc==='overcast clouds') {
            return "https://cdn-icons-png.flaticon.com/512/5904/5904053.png";

        }else if (desc === 'Clear'){
            return "https://cdn-icons-png.flaticon.com/512/869/869869.png";
        } else if (desc === 'Snow') {
            return "https://cdn-icons-png.flaticon.com/512/9755/9755252.png"; // Adjust the path as needed
        }else if(desc==='Clouds') {
            return "https://cdn-icons-png.flaticon.com/512/704/704845.png"; // Adjust the path as needed
        }
    }
    function getDay(date){
        let format=new Date(date);
        let ind=format.getDay();
        let arr=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        return arr[ind];
    }
  return (
    <div className="App">
       <header>
           <h1>Online Weather App</h1>
           <input type="text" placeholder="Enter a city" key="city" onKeyPress={(event)=>{if(event.key==="Enter"){setSrc(" ");search()}}} onChange={(event)=>{setSrc(" ");setLoading(false); setCity(event.target.value)}}/>
       </header>
        <main>
            { loading && city!==" "?
                <div>
                    <div id="MainDiv">
                        <img src={source} title="weather" width="200" height="200"/>
                        <div>
                            <h3>Today</h3>
                            <h2>{city}</h2>
                            <h4>Temperature: {temp} &#8451;</h4>
                            <p>{desc}</p>
                        </div>
                    </div>
                    <div id="par2">
                        {
                           weatherForecast.map((forecast,index)=>(
                               <div key={index} className="blocks">
                                   <h3>{getDay(forecast.date)}</h3>
                                   <img src={forecast.icon} width="50px" height="50px" alt="w"/>
                                   <h3>{forecast.temperature} &#8451;</h3>
                               </div>
                           ))
                        }
                    </div>
                </div>
           :
               <></>
            }
        </main>
    </div>
  );
}

export default App;
