import { useAuth0 } from "@auth0/auth0-react";

// decouple auth provider, using auth0 atm
export const useAuth = () => {
    const {
        isAuthenticated,
        isLoading,
        user,
        loginWithRedirect,
        logout,
        getAccessTokenSilently,
    } = useAuth0();

    return {
        isAuthenticated,
        isLoading,
        user,
        login: loginWithRedirect,
        logout: () =>
            logout({ logoutParams: { returnTo: window.location.origin } }),
        getToken: getAccessTokenSilently,
    };
};