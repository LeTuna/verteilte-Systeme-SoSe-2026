import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getPoll, vote } from "../api/polls";
import Toast from "../components/Toast";
import { useToast } from "../components/useToast";
import { useNavigate } from "react-router-dom";

type Option = {
  id: string;
  text: string;
  votes: number;
};

type Poll = {
  id: string;
  title: string;
  description?: string;
  options: Option[];
};

export default function PollView() {
  const navigate = useNavigate();

  const { id } = useParams();
  const pollId = id!;

  const [poll, setPoll] = useState<Poll | null>(null);
  const [voted, setVoted] = useState(false);

  const storageKey = `voted_${pollId}`;

  const load = async () => {
    const data = await getPoll(pollId);
    setPoll(data);
  };
  
  const { message, showToast } = useToast();

  useEffect(() => {
    load();

    if (localStorage.getItem(storageKey)) {
      setVoted(true);
    }
  }, [pollId]);

  useEffect(() => {
    load();

    const interval = setInterval(() => {
        load();
    }, 3000);

    return () => clearInterval(interval);
  }, [pollId]);

  useEffect(() => {
    if (poll?.title) {
      document.title = `${poll.title} | Voting App`;
    } else {
      document.title = "Poll | Voting App";
    }
  }, [poll]);

  const handleVote = async (optionId: string) => {
    if (voted) return;

    await vote(pollId, optionId);

    localStorage.setItem(storageKey, "true");
    setVoted(true);

    load();
  };

  const copyLink = () => {
    navigator.clipboard.writeText(window.location.href);
    showToast("Link copied!");
  };

  if (!poll) return <div>Loading...</div>;

  return (
    <div>
      <button onClick={() => navigate("/")}>
        ← Back to Polls
      </button>
      <h2>{poll.title}</h2>
      <p>{poll.description}</p>

      <button onClick={copyLink}>🔗 Copy Share Link</button>

      {voted && <p style={{ color: "green" }}>✔ Already voted</p>}

      {poll.options.map((opt) => (
        <div key={opt.id}>
          <button disabled={voted} onClick={() => handleVote(opt.id)}>
            {opt.text} — {opt.votes}
          </button>
        </div>
      ))}

      {message && <Toast message={message} />}
    </div>
  );
}