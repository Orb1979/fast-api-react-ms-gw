import { Auth0Provider } from "@auth0/auth0-react";

const AuthProvider = ({ children }) => {
    return (
        <Auth0Provider
            domain="dev-lc6vtcbv5ll7xa31.eu.auth0.com"
            clientId="qqMWmwUb9F8MaBo6zwcjgzyzVP0NqcR8"
            authorizationParams={{
                redirect_uri: window.location.origin,
                audience: "https://dev-lc6vtcbv5ll7xa31.eu.auth0.com/api/v2/",
            }}
            cacheLocation="localstorage"
            useRefreshTokens={true}
        >
            {children}
        </Auth0Provider>
    );
};

export default AuthProvider;