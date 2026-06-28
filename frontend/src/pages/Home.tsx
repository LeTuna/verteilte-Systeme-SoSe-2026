import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BASE_URL = import.meta.env.VITE_API_URL;

export default function Home() {
  const [polls, setPolls] = useState<any[]>([]);
  const navigate = useNavigate();

  const load = async () => {
    const res = await fetch(`${BASE_URL}/polls/`);
    const data = await res.json();
    setPolls(data);
  };

  useEffect(() => {
    load();
  }, []);

  useEffect(() => {
    document.title = "Polls | Voting App";
  }, []);

  return (
    <div>
      <button onClick={() => navigate("/create")}>
        + Create Poll
      </button>

      <h2>Public Polls</h2>

      {polls.length === 0 && <p>No polls yet 😶</p>}

      {polls.map((p) => (
        <div
          key={p.id}
          style={{ padding: 10, border: "1px solid #ddd", margin: 10 }}
        >
          <h3>{p.title}</h3>
          <p>{p.description}</p>

          <button onClick={() => navigate(`/poll/${p.id}`)}>
            Open
          </button>
        </div>
      ))}
    </div>
  );
}