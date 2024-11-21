
import './App.css';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';



function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path = "/" component= {Home} />
          <Route path = "/login" component= {Login} />
          <Route path = "/register" component= {Register} />
          <Route path = "/admin" component= {AdminDashboard} />

        </Switch>
      </Router>
    </div>
  );
}

export default App;
