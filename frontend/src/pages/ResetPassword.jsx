import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { confirmPasswordReset } from "../api/client";
import "../styles/Login.css";

export default function ResetPassword() {
    const [params] = useSearchParams();
    const navigate = useNavigate();
    const token = params.get("token") || "";
    const [password, setPassword] = useState("");
    const [confirm, setConfirm] = useState("");
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);

    async function handleSubmit(event) {
        event.preventDefault(); setError("");
        if (!token) { setError("This reset link is missing its token. Request a new link."); return; }
        if (password !== confirm) { setError("The passwords do not match."); return; }
        setBusy(true);
        try {
            await confirmPasswordReset(token, password);
            navigate("/login", { replace: true, state: { message: "Password reset successfully. Sign in with your new password." } });
        } catch (err) {
            setError(err.response?.data?.detail || "The reset link is invalid or expired. Request a new link.");
        } finally { setBusy(false); }
    }

    return <main className="login"><section className="panel">
        <div className="brand"><span className="input-icon">🎓</span><span>Degree Progress Tracker</span></div>
        <h1>Choose a new password</h1>
        <p className="subtitle">Use at least 12 characters with uppercase and lowercase letters, a number, and a special character.</p>
        <form className="form" onSubmit={handleSubmit}>
            {error && <p className="error" role="alert">{error}</p>}
            <label htmlFor="new-password">New password</label>
            <div className="input-shell"><span className="input-icon">🔒</span><input id="new-password" type="password" autoComplete="new-password" minLength={12} maxLength={72} value={password} onChange={e => setPassword(e.target.value)} required /></div>
            <label htmlFor="confirm-password">Confirm new password</label>
            <div className="input-shell"><span className="input-icon">🔒</span><input id="confirm-password" type="password" autoComplete="new-password" minLength={12} maxLength={72} value={confirm} onChange={e => setConfirm(e.target.value)} required /></div>
            <button type="submit" disabled={busy}>{busy ? "Resetting…" : "Reset password"}</button>
        </form>
        <p className="form-footer"><Link to="/forgot-password">Request another reset link</Link></p>
    </section></main>;
}
