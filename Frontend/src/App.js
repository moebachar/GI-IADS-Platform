import { Route, Routes } from "react-router-dom";
import React from "react";
// import "./App.css";
import Home from "./Home/index";
import Regression from "./Regression";
import Classification from "./Classification/index";
import OD from "./ObjectDetection/OD";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/regression" exact element={<Regression />} />
      <Route path="/classification" exact element={<Classification />} />
      <Route path="/object_detection" exact element={<OD />} />
    </Routes>
  );
}

export default App;
