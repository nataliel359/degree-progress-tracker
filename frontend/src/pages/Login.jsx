import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";
import "../styles/Login.css";

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await login(email, password);
            navigate("/dashboard");
        } catch (error) {
            setError("Invalid email or password");
        }
    };

    return (
        <main className="login">
            <section className="panel">
                <div className="brand">
                    <span className="input-icon">🎓</span>
                    <span>Degree Progress Tracker</span>
                </div>

                <h1>Sign In</h1>
                <p className="subtitle">
                    Use your student credentials to continue.
                </p>

                <form className="form" onSubmit={handleSubmit}>
                    {error && <p className="error">{error}</p>}

                    <label htmlFor="email">Email</label>
                    <div className="input-shell">
                        <span className="input-icon">✉</span>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <label htmlFor="password">Password</label>
                    <div className="input-shell">
                        <span className="input-icon">🔒</span>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    <button type="submit">Sign In</button>
                </form>
            </section>
        </main>
    );
}