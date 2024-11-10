import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "bootswatch/dist/litera/bootstrap.css";

import App from "./App.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
