export default function Toast({ message }: { message: string }) {
  return (
    <div
      style={{
        position: "fixed",
        bottom: 20,
        right: 20,
        background: "#333",
        color: "white",
        padding: "10px 15px",
        borderRadius: 8,
      }}
    >
      {message}
    </div>
  );
}