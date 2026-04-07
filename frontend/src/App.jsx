import { useEffect } from "react";
import CustomerManager from "./components/CustomerManager";
import { useAuth } from "./auth/useAuth";
import { jwtDecode } from "jwt-decode";

function App() {
  const { login, logout, getToken, isAuthenticated, isLoading } = useAuth();

  // Auto login
  useEffect(() => {
    if (isLoading) return;
    if (!isAuthenticated) login();
  }, [isLoading, isAuthenticated, login]);

  // log token when logged in
  useEffect(() => {
    if (isLoading || !isAuthenticated) return;
    (async () => {
      const token = await getToken();
      console.log("ACCESS TOKEN:", token);
      const decoded = jwtDecode(token);
      console.log("DECODED TOKEN:", decoded);
    })();
  }, [isAuthenticated, isLoading, getToken]);

  return (
      <div>
        <button onClick={logout}>Logout</button>
        {(isAuthenticated ? <CustomerManager /> : null)}
      </div>
  );
}

export default App;
