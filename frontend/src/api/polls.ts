const BASE_URL = "http://localhost:8000";

export async function createPoll(data: any) {
  const res = await fetch(`${BASE_URL}/polls/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function getPoll(id: string) {
  const res = await fetch(`${BASE_URL}/polls/${id}`);
  return res.json();
}

export async function vote(pollId: string, optionId: string) {
  const res = await fetch(
    `${BASE_URL}/polls/${pollId}/vote/${optionId}`,
    {
      method: "POST",
      credentials: "include",
    }
  );

  return res.json();
}