
import './App.css';
import {NavBar} from "./components/NavBar";
import {SideMenu} from "./components/SideMenu";
import {Games} from "./components/Games";

function App() {
  return (
    <div className="App">
      <NavBar/>
      <SideMenu/>
      <Games/>
    </div>
  );
}

export default App;
