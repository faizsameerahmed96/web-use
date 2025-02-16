import * as React from "react";
import { createRoot } from "react-dom/client";
// import logo from "./bumblebee.png";

// const imagePath = `file://${path.join(__dirname, "bumblebee.png")}`;

const App = () => {
  const [state, setState] = React.useState({ state: "INITIAL_STATE" });

  React.useEffect(() => {
    let ws = new WebSocket("ws://127.0.0.1:8765");

    ws.onmessage = (event) => {
      setState(JSON.parse(event.data));
    };

    ws.onerror = (error) => {
      console.log("Error:", error);
    };

    return () => {
      ws.close();
    };
  }, []);

  const Waveform = () => {
    return (
      <div style={styles.container}>
        <div style={{ ...styles.line, animationDelay: "0s" }} />
        <div style={{ ...styles.line, animationDelay: "0.2s" }} />
        <div style={{ ...styles.line, animationDelay: "0.4s" }} />
      </div>
    );
  };

  const styles = {
    container: {
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100px",
      gap: "10px",
    },
    line: {
      width: "10px",
      height: "30px",
      backgroundColor: "#FFBD59",
      borderRadius: "5px",
      animation: "wave 1s infinite ease-in-out",
    },
  };

  const render = () => {
    if (
      state.state === "WAITING_FOR_WAKEWORD" ||
      state.state === "INITIAL_STATE"
    ) {
      let logo_size = 75;
      if (state.state?.data?.question) {
        logo_size = 30;
      }

      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: logo_size,
              height: logo_size,
              backgroundColor: "#FFBD59",
              borderRadius: "50%",
              animation: "pulse 1.5s infinite ease-in-out",
            }}
          ></div>

          {state.state?.data?.question && (
            <h3>Question: {state.state.data.question}</h3>
          )}

          <h2 style={{ textAlign: "center" }}>
            Say <span style={{ color: "#FFBD59" }}>"BumbleBee"</span> to{" "}
            {state.state?.data?.question ? "answer" : "get started"}
          </h2>
        </div>
      );
    } else if (state.state == "RECORDING_AUDIO") {
      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Waveform />

          <h4 style={{ textAlign: "center" }}>Listening...</h4>
        </div>
      );
    } else if (state.state == "PERFORMING_TASK") {
      return (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: 100,
              height: 100,
              backgroundColor: "#FFBD59",
              borderRadius: "50%",
              animation: "pulse 0.5s infinite ease-in-out",
            }}
          ></div>

          <h4 style={{ textAlign: "center" }}>Performing task...</h4>
        </div>
      );
    }
    return <p>{state.state}</p>;
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
        width: "100%",
      }}
    >
      <style>
        {`
          @keyframes pulse {
            0%, 100% {
              transform: scale(1);
              opacity: 1;
            }
            50% {
              transform: scale(1.1);
              opacity: 0.9;
            }
          }
        `}
      </style>
      <style>
        {`
            @keyframes wave {
    0%, 100% { transform: scaleY(1); }
    50% { transform: scaleY(1.5); }
  }`}
      </style>
      {render()}
    </div>
  );
};

const root = createRoot(document.body);
root.render(<App />);
