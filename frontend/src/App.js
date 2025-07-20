import React from "react";
import "./App.css";
import PredictionForm from "./PredictionForm";


function App() {
  return (
    <div className="app" >
      <header className="navbar">
        <div className="logo">WineInsight</div>
        <nav>
          <ul>
            <li><a href="/#">Home</a></li>
            <li><a href="/#">About</a></li>
            <li><a href="/#">Contact</a></li>
          </ul>
        </nav>
      </header>

      <main className="main-content">
        <h1>Red Wine Quality Prediction</h1>
        <PredictionForm />
      </main>

      <footer className="footer">
        <p>&copy; {new Date().getFullYear()} WineInsight. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
