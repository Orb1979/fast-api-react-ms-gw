import { useAuth } from "../auth/useAuth";

export default function LoginButton() {
    const { login } = useAuth();

    return <button onClick={login}>Login</button>;
}