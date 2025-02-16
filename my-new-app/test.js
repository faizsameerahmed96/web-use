const WebSocket = require("ws");

const ws = new WebSocket("ws://localhost:8765");

ws.on("open", () => {
    console.log("Connected to WebSocket server");
    ws.send("Hello Server!");
});

ws.on("message", (data) => {
    console.log("Message from server:", data.toString());
});

ws.on("error", (error) => {
    console.error("WebSocket error:", error);
});


setTimeout(() => {
    console.log("Exiting WebSocket test...");
    process.exit(0);
}, 10000);