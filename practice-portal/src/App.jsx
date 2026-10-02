import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import Layout from "./components/Layout";
import { RequireAuth, RequireAdmin, RedirectIfAuthed } from "./components/RouteGuards";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import TopicPage from "./pages/TopicPage";
import QuestionPage from "./pages/QuestionPage";
import Leaderboard from "./pages/Leaderboard";
import Profile from "./pages/Profile";
import AdminLayout from "./pages/admin/AdminLayout";
import AdminQuestions from "./pages/admin/AdminQuestions";
import AdminStudents from "./pages/admin/AdminStudents";

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route element={<Layout />}>
              <Route
                path="/login"
                element={
                  <RedirectIfAuthed>
                    <Login />
                  </RedirectIfAuthed>
                }
              />
              <Route
                path="/signup"
                element={
                  <RedirectIfAuthed>
                    <Signup />
                  </RedirectIfAuthed>
                }
              />

              <Route element={<RequireAuth />}>
                <Route path="/" element={<Dashboard />} />
                <Route path="/topics/:slug" element={<TopicPage />} />
                <Route path="/topics/:slug/questions/:questionId" element={<QuestionPage />} />
                <Route path="/leaderboard" element={<Leaderboard />} />
                <Route path="/profile" element={<Profile />} />

                <Route element={<RequireAdmin />}>
                  <Route path="/admin" element={<AdminLayout />}>
                    <Route index element={<AdminQuestions />} />
                    <Route path="students" element={<AdminStudents />} />
                  </Route>
                </Route>
              </Route>

              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </AuthProvider>
      </BrowserRouter>
    </ThemeProvider>
  );
}

function NotFound() {
  return (
    <div className="mx-auto max-w-lg px-4 py-20 text-center">
      <h1 className="text-3xl font-bold">404</h1>
      <p className="mt-2 text-slate-500 dark:text-slate-400">Page not found.</p>
    </div>
  );
}
