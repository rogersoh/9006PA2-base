const video = document.getElementById("video");
const fpsEl = document.getElementById("fps");
const modelStatusEl = document.getElementById("model-status");
const alertsEl = document.getElementById("alerts");
const errorEl = document.getElementById("error");

let socket;
let reconnectDelay = 250;
let lastObjectUrl = null;

function setError(message) {
  if (!message) {
    errorEl.textContent = "";
    errorEl.classList.add("hidden");
    return;
  }
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
}

function renderAlerts(alerts) {
  alertsEl.innerHTML = "";
  for (const alert of alerts || []) {
    const div = document.createElement("div");
    div.className = `alert ${alert.severity || "low"}`;
    div.textContent = `${alert.type || "alert"}: ${alert.message || ""}`;
    alertsEl.appendChild(div);
  }
}

function connect() {
  socket = new WebSocket(`ws://${window.location.host}/ws`);
  socket.binaryType = "blob";

  socket.onopen = () => {
    reconnectDelay = 250;
    setError("");
  };

  socket.onmessage = async (event) => {
    if (typeof event.data === "string") {
      const payload = JSON.parse(event.data);
      if (payload.type === "status") {
        fpsEl.textContent = Number(payload.fps || 0).toFixed(1);
        modelStatusEl.textContent = payload.model_status || "loading";
        if (payload.model_status === "error") {
          setError("Backend entered an error state.");
          if (lastObjectUrl) {
            URL.revokeObjectURL(lastObjectUrl);
            lastObjectUrl = null;
          }
          video.removeAttribute("src");
        } else {
          setError("");
        }
      } else if (payload.type === "alerts") {
        renderAlerts(payload.alerts);
      }
      return;
    }

    const blob = event.data instanceof Blob ? event.data : new Blob([event.data]);
    const nextUrl = URL.createObjectURL(blob);
    if (lastObjectUrl) {
      URL.revokeObjectURL(lastObjectUrl);
    }
    lastObjectUrl = nextUrl;
    video.src = nextUrl;
  };

  socket.onclose = () => {
    setTimeout(connect, reconnectDelay);
    reconnectDelay = Math.min(reconnectDelay * 2, 5000);
  };

  socket.onerror = () => {
    socket.close();
  };
}

connect();
