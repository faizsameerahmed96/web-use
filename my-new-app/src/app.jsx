import * as React from "react";
import { createRoot } from "react-dom/client";


const ws = new WebSocket("ws://127.0.0.1:8765");


ws.onmessage = (event) => {
    console.log('Message from server:', event.data);
};

ws.onerror = (error) => {
    console.log('Error:', error);
};

const App = () => {
  const [message, setMessage] = React.useState(""); // Store Python messages

  return (
    <div>
      <h2>Hello from React! {message} </h2>
    </div>
  );
};

const root = createRoot(document.body);
root.render(<App />);
