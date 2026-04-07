import {useAuth} from "../auth/useAuth";

// This hook returns a function to make authenticated requests
export const useApi = () => {
    const { getToken, isAuthenticated, login } = useAuth();

    return async (url, options = {}) => {
        if (!isAuthenticated) {
            await login();
            return;
        }

        const token = await getToken();
        return fetch(url, {
            ...options,
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
                ...options.headers,
            },
        });
    };
};