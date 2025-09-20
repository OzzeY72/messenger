import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function GoogleCallback() {
  const navigate = useNavigate();
  const { loginOAuth } = useAuth();

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      (async () => {
        try {
          await loginOAuth("google", code);
          navigate("/chat");
        } catch (err) {
          console.error("OAuth login error:", err);
          navigate("/login");
        }
      })();
    } else {
      navigate("/login");
    }
  }, [navigate, loginOAuth]);

  return <p>Загрузка... Авторизация через Google</p>;
}