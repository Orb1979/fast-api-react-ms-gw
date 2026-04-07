package com.example.msf.gateway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(
                auth -> auth
                    .requestMatchers("/public/**").permitAll()
                    .anyRequest().authenticated()
                )
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }
}

/*
Configure HTTP security for the gateway
1 Authorize requests:
  - Any request matching /public/** is allowed without authentication
  - All other requests require a valid JWT token
2 Enable OAuth2 Resource Server support:
  - Validates incoming JWTs,
      - Discover the authorization server metadata through this OpenID Connect discovery endpoint
        application.properties > security.oauth2.resourceserver.jwt.issuer-uri
        For every request:
          - Verify signature using the public key (with private key on auth0 server)
          - Check iss matches your issuer-uri
          - Validate exp, nbf, etc.
3 Populates Spring Security context with Authentication object
4 Makes the JWT available in controllers via @AuthenticationPrincipal Jwt jw

Incoming request
      ↓
SecurityFilterChain
      ↓
[JWT filter]
      ↓
[Authentication filter]
      ↓
[Authorization filter]
      ↓
Controller
*/




