import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import CreatePoll from "./pages/CreatePoll";
import PollView from "./pages/PollView";

export default function App() {
  return (
    <div className="container">
      <h1>🗳 Voting App</h1>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<CreatePoll />} />
        <Route path="/poll/:id" element={<PollView />} />
      </Routes>
    </div>
  );
}