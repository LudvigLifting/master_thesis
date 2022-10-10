import React, { useState } from "react";
import Extinguisher from "./Extinguisher";

function App() {
  const [extinguishers, setExtinguishers] = useState([])
  return (
    <Extinguisher />
  )
}

export default App;
