import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AuthProvider } from "./auth/AuthContext";
import ProtectedRoute from "./auth/ProtectedRoute";
import Dashboard from "./pages/Dashboard";
import ForgotPassword from "./pages/ForgotPassword";
import Login from "./pages/Login";
import ResetPassword from "./pages/ResetPassword";

function App() {
  const publicUrl = (process.env.PUBLIC_URL || "").replace(/\/$/, "");
  const isHostedAtPublicUrl =
    publicUrl &&
    (window.location.pathname === publicUrl ||
      window.location.pathname.startsWith(`${publicUrl}/`));

  return (
    <AuthProvider>
      <BrowserRouter basename={isHostedAtPublicUrl ? publicUrl : undefined}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App;
