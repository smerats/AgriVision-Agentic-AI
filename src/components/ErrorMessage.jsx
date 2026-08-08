export default function ErrorMessage({ message }) {
  return (
    <div className="error-card">
      <p>⚠️ {message}</p>
    </div>
  );
}
