import { useState } from "react";
import { Link } from "react-router-dom";
import { requestPasswordReset } from "../api/client";
import "../styles/Login.css";

export default function ForgotPassword() {
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault();
        setBusy(true); setError(""); setMessage("");
        try {
            const result = await requestPasswordReset(email.trim());
            setMessage(result.message || "If an account exists for that email, a password reset link will be sent.");
        } catch {
            setError("We couldn't process the request right now. Please try again shortly.");
        } finally { setBusy(false); }
    }

    return <main className="login"><section className="panel">
        <div className="brand"><span className="input-icon">🎓</span><span>Degree Progress Tracker</span></div>
        <h1>Forgot your password?</h1>
        <p className="subtitle">Enter the email associated with your account. If it exists, we'll send a reset link that expires in 30 minutes.</p>
        <form className="form" onSubmit={handleSubmit}>
            {message && <p className="success" role="status">{message}</p>}
            {error && <p className="error" role="alert">{error}</p>}
            <label htmlFor="reset-email">Email</label>
            <div className="input-shell"><span className="input-icon">✉</span><input id="reset-email" type="email" autoComplete="email" value={email} onChange={e => setEmail(e.target.value)} required /></div>
            <button type="submit" disabled={busy}>{busy ? "Sending…" : "Send reset link"}</button>
        </form>
        <p className="form-footer"><Link to="/login">Back to sign in</Link></p>
    </section></main>;
}
