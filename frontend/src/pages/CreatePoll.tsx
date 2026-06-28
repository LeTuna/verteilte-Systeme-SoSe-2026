import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BASE_URL = import.meta.env.VITE_API_URL;

export default function CreatePoll() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [options, setOptions] = useState<string[]>(["", ""]);
  const [visibility, setVisibility] = useState("public");

  const addOption = () => setOptions([...options, ""]);

  const submit = async () => {
    const res = await fetch(`${BASE_URL}/polls/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title,
        description,
        visibility,
        options: options.map((t) => ({ text: t })),
      }),
    });

    const data = await res.json();

    navigate(`/poll/${data.id}`);
  };

  useEffect(() => {
    document.title = "Create Poll | Voting App";
  }, []);

  return (
    <div>
      <button onClick={() => navigate("/")}>
         ← Back to Polls
      </button>
      <h2>Create Poll</h2>

      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <div style={{ marginTop: "1rem" }}>
        <label>Visibility</label>

        <div>
          <label>
            <input
              type="radio"
              value="public"
              checked={visibility === "public"}
              onChange={(e) => setVisibility(e.target.value)}
            />
            Public
          </label>
        </div>

        <div>
          <label>
            <input
              type="radio"
              value="unlisted"
              checked={visibility === "unlisted"}
              onChange={(e) => setVisibility(e.target.value)}
            />
            Unlisted
          </label>
        </div>
      </div>

      <h3>Options</h3>

      {options.map((o, i) => (
        <input
          key={i}
          value={o}
          placeholder={`Option ${i + 1}`}
          onChange={(e) => {
            const copy = [...options];
            copy[i] = e.target.value;
            setOptions(copy);
          }}
        />
      ))}

      <button onClick={addOption}>Add option</button>

      <button onClick={submit}>Create</button>
    </div>
  );
}