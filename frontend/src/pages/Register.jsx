import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/client";
import "../styles/Login.css";

export default function Register() {
    const navigate = useNavigate();
    const [form, setForm] = useState({ full_name: "", email: "", student_id: "", password: "", confirm: "" });
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);
    const update = (key) => (event) => setForm(current => ({ ...current, [key]: event.target.value }));

    async function handleSubmit(event) {
        event.preventDefault(); setError("");
        if (form.password !== form.confirm) { setError("The passwords do not match."); return; }
        setBusy(true);
        try {
            await registerUser({ full_name: form.full_name.trim(), email: form.email.trim(), student_id: form.student_id.trim() || null, password: form.password });
            navigate("/login", { replace: true, state: { message: "Account created. Sign in to continue." } });
        } catch (err) {
            const detail = err.response?.data?.detail;
            setError(typeof detail === "string" ? detail : "Unable to create your account. Check your details and try again.");
        } finally { setBusy(false); }
    }

    return <main className="login"><section className="panel">
        <div className="brand"><span className="input-icon">🎓</span><span>Degree Progress Tracker</span></div>
        <h1>Create account</h1>
        <p className="subtitle">Create your account to track your degree progress.</p>
        <form className="form" onSubmit={handleSubmit}>
            {error && <p className="error" role="alert">{error}</p>}
            <label htmlFor="full-name">Full name</label><div className="input-shell"><input id="full-name" autoComplete="name" value={form.full_name} onChange={update("full_name")} minLength={2} maxLength={120} required /></div>
            <label htmlFor="register-email">Email</label><div className="input-shell"><input id="register-email" type="email" autoComplete="email" value={form.email} onChange={update("email")} required /></div>
            <label htmlFor="student-id">Student ID (optional)</label><div className="input-shell"><input id="student-id" value={form.student_id} onChange={update("student_id")} maxLength={40} /></div>
            <label htmlFor="register-password">Password</label><div className="input-shell"><input id="register-password" type="password" autoComplete="new-password" value={form.password} onChange={update("password")} minLength={12} maxLength={72} required /></div>
            <label htmlFor="register-confirm">Confirm password</label><div className="input-shell"><input id="register-confirm" type="password" autoComplete="new-password" value={form.confirm} onChange={update("confirm")} minLength={12} maxLength={72} required /></div>
            <p className="password-hint">Use 12+ characters with uppercase and lowercase letters, a number, and a special character (maximum 72 UTF-8 bytes).</p>
            <button type="submit" disabled={busy}>{busy ? "Creating account…" : "Create account"}</button>
        </form>
        <p className="form-footer">Already have an account? <Link to="/login">Sign in</Link></p>
    </section></main>;
}
